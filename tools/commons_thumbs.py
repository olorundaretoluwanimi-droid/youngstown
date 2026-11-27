# commons_thumbs.py <titles file> <out dir> [px]: download a small thumbnail of each Commons file (numbered k001.jpg …) + index.txt
import json, urllib.request, urllib.parse, sys, os, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
T = [l.strip() for l in open(sys.argv[1], encoding='utf-8') if l.strip() and not l.startswith('#')]
out = sys.argv[2]; px = int(sys.argv[3]) if len(sys.argv) > 3 else 360; os.makedirs(out, exist_ok=True)
H = {"User-Agent": "lemo-film-research/1.0 (documentary research)"}
idx = open(os.path.join(out, 'index.txt'), 'a', encoding='utf-8'); n0 = len(os.listdir(out))
for i in range(0, len(T), 20):
    p = {"action": "query", "titles": "|".join(t if t.startswith('File:') else 'File:' + t for t in T[i:i + 20]), "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": px, "format": "json"}
    for a in range(6):
        try: d = json.load(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p), headers=H), timeout=60)); break
        except Exception: time.sleep(6)
    for pg in d["query"]["pages"].values():
        ii = (pg.get("imageinfo") or [{}])[0]; u = ii.get("thumburl")
        if not u: print('no thumb', pg.get('title')); continue
        n0 += 1; f = os.path.join(out, f'k{n0:03d}.jpg')
        for a in range(4):
            try: open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read()); break
            except Exception: time.sleep(4)
        lic = ii.get('extmetadata', {}).get('LicenseShortName', {}).get('value', '')
        idx.write(f"k{n0:03d}\t{ii.get('width')}x{ii.get('height')}\t{lic}\t{pg['title'][5:]}\n"); time.sleep(.4)
    time.sleep(1)
