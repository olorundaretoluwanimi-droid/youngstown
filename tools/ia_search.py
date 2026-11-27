# ia_search.py <query...>: Internet Archive advanced search (identifier | title | year | mediatype | licence)
import sys, json, urllib.request, urllib.parse, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for q in sys.argv[1:]:
    u = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode({"q": q, "fl[]": ["identifier", "title", "year", "mediatype", "licenseurl", "collection"], "rows": 40, "output": "json"}, doseq=True)
    try: d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "documentary-research/1.0"}), timeout=60))
    except Exception as e: print(q, "ERR", e); continue
    r = d["response"]; print("##", q, r["numFound"])
    for x in r["docs"]: print("  ", x["identifier"], "|", str(x.get("title"))[:90], "|", x.get("year"), "|", x.get("mediatype"), "|", x.get("licenseurl", ""), "|", ",".join(x.get("collection", []))[:50] if isinstance(x.get("collection"), list) else x.get("collection"))
    time.sleep(1)
