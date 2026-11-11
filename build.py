import asyncio, json, pathlib, re
import jieba
from pypinyin import lazy_pinyin, Style, load_phrases_dict
import edge_tts

root=pathlib.Path(__file__).parent
items=json.loads((root/'sentences.json').read_text(encoding='utf-8'))
load_phrases_dict({'角马':[['jiǎo'],['mǎ']], '迁徙':[['qiān'],['xǐ']], '繁衍':[['fán'],['yǎn']], '横亘':[['héng'],['gèn']], '干涸':[['gān'],['hé']], '优胜劣汰':[['yōu'],['shèng'],['liè'],['tài']]})
for w in ['角马','塞伦盖蒂','马赛马拉','坦桑尼亚','肯尼亚','横亘','繁衍','干涸','休养生息','长途跋涉','优胜劣汰','气势磅礴','生存法则','死亡之角']:
 jieba.add_word(w, freq=100000)
(root/'audio').mkdir(exist_ok=True)
(root/'audio'/'words').mkdir(exist_ok=True)
sem=asyncio.Semaphore(5)
async def make_audio(text,path):
 if path.exists() and path.stat().st_size>1000: return
 async with sem:
  for attempt in range(5):
   try:
    await edge_tts.Communicate(text,voice='zh-CN-XiaoxiaoNeural',rate='-12%').save(str(path))
    if path.stat().st_size>1000:return
   except Exception:
    pass
   await asyncio.sleep(2+attempt*3)
  raise RuntimeError('音频生成失败: '+text)
async def main():
 tasks=[]
 words={}
 for i,x in enumerate(items):
  tasks.append(make_audio(x['text'],root/'audio'/f'{i+1:03d}.mp3'))
  x['audio']=f'audio/{i+1:03d}.mp3'
  x['units']=[]
  for w in jieba.cut(x['text'],HMM=False):
   if not w.strip():continue
   if re.fullmatch(r'[^\u3400-\u9fff]+',w):
    x['units'].append({'text':w,'pinyin':'','audio':None})
    continue
   if w not in words:words[w]=len(words)+1
   x['units'].append({'text':w,'pinyin':' '.join(lazy_pinyin(w,style=Style.TONE)),'audio':f'audio/words/{words[w]:04d}.mp3'})
  x['pinyin']=' '.join(u['pinyin'] for u in x['units'] if u['pinyin'])
 for w,n in words.items():
  tasks.append(make_audio(w,root/'audio'/'words'/f'{n:04d}.mp3'))
 await asyncio.gather(*tasks)
 (root/'site_data.json').write_text(json.dumps(items,ensure_ascii=False),encoding='utf-8')
 print('Generated',len(items),'sentences and',len(words),'word clips')
asyncio.run(main())
