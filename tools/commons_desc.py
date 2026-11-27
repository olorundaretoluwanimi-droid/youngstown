# commons_desc.py <search> [pattern]: Commons file search; print size, licence and the caption text near "Text Appearing Before Image" (IA book images)
import json,urllib.request,urllib.parse,re,sys,time
def api(**p):
    p.update(format="json")
    return json.load(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(p),headers={"User-Agent":"documentary-research/1.0"}),timeout=60))
q=sys.argv[1]; pat=sys.argv[2] if len(sys.argv)>2 else ''
d=api(action="query",generator="search",gsrsearch=q,gsrnamespace=6,gsrlimit=50,prop="imageinfo",iiprop="extmetadata|size")
for p in (d.get("query",{}).get("pages",{}) or {}).values():
    ii=(p.get("imageinfo") or [{}])[0]; m=ii.get("extmetadata",{})
    t=re.sub("<[^>]+>"," ",m.get("ImageDescription",{}).get("value","")); t=re.sub(r"\s+"," ",t)
    b=re.search(r"Text Appearing Before Image:(.*?)Text Appearing After Image:(.{0,120})",t)
    cap=(b.group(1)[-160:]+" || "+b.group(2)) if b else t[:200]
    if pat and not re.search(pat,cap,re.I): continue
    sys.stdout.buffer.write(f"{p['title'][5:]} | {ii.get('width')}x{ii.get('height')} | {m.get('LicenseShortName',{}).get('value','')} | {cap}\n".encode('utf-8','replace'))
