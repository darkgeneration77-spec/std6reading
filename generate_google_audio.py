import json,re,pathlib,time
from gtts import gTTS
from pypinyin import pinyin,Style
s=pathlib.Path('index.html').read_text()
a=json.loads(re.search(r'const EMBEDDED=(\[.*?\]);',s,re.S).group(1))
b=json.loads(re.search(r'const paragraphs2=(\[.*?\]);',s,re.S).group(1))
b=[dict(text=m.group(),para=i) for i,p in enumerate(b) for m in re.finditer(r'[^。！？]+[。！？]+[”]?|[^。！？]+$',p)]
def save(t,path):
 p=pathlib.Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and p.stat().st_size>100:return
 for attempt in range(4):
  try:
   gTTS(t,lang='zh-CN').save(str(p));return
  except Exception:
   if attempt==3:raise
   time.sleep(5*(attempt+1))
for unit,items in enumerate([a,b],1):
 for i,item in enumerate(items):
  save(item['text'],f'google-audio/{unit}/{i}.mp3')
  for c in set(item['text']):
   if '\u3400'<=c<='\u9fff':save(c,f'google-audio/char/{ord(c)}.mp3')
