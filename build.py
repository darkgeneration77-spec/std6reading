import asyncio, json, pathlib, html
from pypinyin import lazy_pinyin, Style, load_phrases_dict
import edge_tts
root=pathlib.Path(__file__).parent
items=json.loads((root/'sentences.json').read_text(encoding='utf-8'))
# 重要：拼音是自动生成的初稿；出版前须逐句人工核对多音字和专有名词。
load_phrases_dict({'角马':[['jiǎo'],['mǎ']], '迁徙':[['qiān'],['xǐ']], '繁衍':[['fán'],['yǎn']], '横亘':[['héng'],['gèn']], '干涸':[['gān'],['hé']], '优胜劣汰':[['yōu'],['shèng'],['liè'],['tài']]})
async def main():
 (root/'audio').mkdir(exist_ok=True)
 for i,x in enumerate(items):
  out=root/'audio'/f'{i+1:03d}.mp3'
  if not out.exists() or out.stat().st_size<1000:
   for attempt in range(3):
    try:
     await edge_tts.Communicate(x['text'],voice='zh-CN-XiaoxiaoNeural',rate='-10%').save(str(out))
     break
    except Exception:
     if attempt==2: raise
     await asyncio.sleep(3)
  x['audio']=f'audio/{i+1:03d}.mp3'
  x['pinyin']=' '.join(lazy_pinyin(x['text'],style=Style.TONE,errors=lambda s:list(s)))
 (root/'site_data.json').write_text(json.dumps(items,ensure_ascii=False),encoding='utf-8')
 print('已生成',len(items),'个 MP3；请人工试听核对发音和拼音。')
asyncio.run(main())
