# commons_info.py <titles file>: licence, size, author, date, description for each Commons file title (one per line)
import json,urllib.request,urllib.parse,re,sys,time
import sys; sys.stdout.reconfigure(encoding="utf-8", errors="replace")
T=[l.strip() for l in open(sys.argv[1],encoding='utf-8') if l.strip()]
for i in range(0,len(T),20):
    p={"action":"query","titles":"|".join(T[i:i+20]),"prop":"imageinfo","iiprop":"extmetadata|size","format":"json"}
    for a in range(6):
        try: d=json.load(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(p),headers={"User-Agent":"lemo-film-research/1.0 (documentary research)"}))); break
        except Exception: time.sleep(6)
    for pg in d["query"]["pages"].values():
        ii=(pg.get("imageinfo") or [{}])[0]; m=ii.get("extmetadata",{})
        g=lambda k: re.sub("<[^>]+>","",m.get(k,{}).get("value",""))[:150].replace("\n"," ")
        print(pg["title"][5:90],"|",ii.get("width"),"x",ii.get("height"),"|",g("LicenseShortName"),"|",g("Artist")[:50],"|",g("DateTimeOriginal")[:25],"|",g("ImageDescription"))
    time.sleep(1.5)
