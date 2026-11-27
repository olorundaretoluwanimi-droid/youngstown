# commons_list.py cats|search <items...>: list Commons category members or file-search results
import json,urllib.request,urllib.parse,time,sys
import sys; sys.stdout.reconfigure(encoding="utf-8", errors="replace")
def api(**p):
    p.update(format="json")
    for a in range(6):
        try: return json.load(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(p),headers={"User-Agent":"lemo-film-research/1.0 (documentary research)"})))
        except Exception: time.sleep(6)
mode=sys.argv[1]
for c in sys.argv[2:]:
    if mode=="cats":
        d=api(action="query",list="categorymembers",cmtitle="Category:"+c,cmlimit=200); m=d["query"]["categorymembers"] if d else []
    else:
        d=api(action="query",list="search",srsearch=c,srnamespace=6,srlimit=25); m=d["query"]["search"] if d else []
    print("##",c,len(m)); [print("   ",x["title"]) for x in m]; time.sleep(1.5)
