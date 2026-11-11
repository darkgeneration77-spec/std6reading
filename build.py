import asyncio,json,pathlib,re
from pypinyin import pinyin,Style,load_phrases_dict
import edge_tts
root=pathlib.Path(__file__).parent
items=json.loads((root/'sentences.json').read_text(encoding='utf-8'))
load_phrases_dict({'角马':[['jiǎo'],['mǎ']], '迁徙':[['qiān'],['xǐ']], '繁衍':[['fán'],['yǎn']], '横亘':[['héng'],['gèn']], '干涸':[['gān'],['hé']]})
(root/'audio').mkdir(exist_ok=True)
(root/'audio'/'chars').mkdir(exist_ok=True)
sem=asyncio.Semaphore(4)
async def make(text,path,marks=False):
 if path.exists() and path.stat().st_size>1000 and not marks:return []
 async with sem:
  for attempt in range(5):
   try:
    chunks=[];bound=[]
    async for m in edge_tts.Communicate(text,voice='zh-CN-XiaoxiaoNeural',rate='-15%').stream():
     if m['type']=='audio':chunks.append(m['data'])
     elif m['type']=='WordBoundary':bound.append({'text':m['text'],'start':m['offset']/10000000,'duration':m['duration']/10000000})
    if not chunks:raise RuntimeError('empty audio')
    path.write_bytes(b''.join(chunks))
    return bound
   except Exception:
    if attempt==4:raise
    await asyncio.sleep(2+attempt*3)
async def main():
 chars={};tasks=[]
 for i,x in enumerate(items):
  txt=x['text'];reads=pinyin(txt,style=Style.TONE,errors=lambda s:list(s))
  x['characters']=[]
  for j,ch in enumerate(txt):
   sound=None
   if re.match(r'[\u3400-\u9fff]',ch):
    if ch not in chars:chars[ch]=len(chars)+1
    sound=f'audio/chars/{chars[ch]:04d}.mp3'
   x['characters'].append({'char':ch,'py':reads[j][0] if sound else '', 'audio':sound})
  x['audio']=f'audio/{i+1:03d}.mp3'
 for ch,num in chars.items():tasks.append(make(ch,root/'audio'/'chars'/f'{num:04d}.mp3'))
 async def sentence(i,x):
  boundaries=await make(x['text'],root/'audio'/f'{i+1:03d}.mp3',True)
  timeline=[];cursor=0
  for b in boundaries:
   start=x['text'].find(b['text'],cursor)
   if start<0:start=x['text'].find(b['text'])
   if start<0:continue
   cursor=start+len(b['text'])
   indices=[j for j in range(start,cursor) if x['characters'][j]['audio']]
   for k,j in enumerate(indices):timeline.append({'index':j,'time':round(b['start']+b['duration']*k/max(1,len(indices)),3)})
  x['timing']=sorted(timeline,key=lambda v:v['time'])
 await asyncio.gather(*(sentence(i,x) for i,x in enumerate(items)),*tasks)
 (root/'site_data.json').write_text(json.dumps(items,ensure_ascii=False),encoding='utf-8')
 print('Generated',len(items),'sentence audios and',len(chars),'character audios')
asyncio.run(main())
