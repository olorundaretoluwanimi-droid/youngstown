# loc_find.py <query...>: Library of Congress photos search (title | date | id | rights)
import sys, json, urllib.request, urllib.parse, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for q in sys.argv[1:]:
    u = "https://www.loc.gov/photos/?" + urllib.parse.urlencode({"q": q, "fo": "json", "c": 40})
    try: d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "documentary-research/1.0"}), timeout=60))
    except Exception as e: print(q, "ERR", e); continue
    print("##", q, d.get("pagination", {}).get("of"))
    for r in d.get("results", []):
        print("  ", (r.get("title") or "")[:110], "|", r.get("date"), "|", r.get("id"), "|", (r.get("rights_advisory") or [""])[0][:40] if isinstance(r.get("rights_advisory"), list) else r.get("rights_advisory"))
    time.sleep(2)
