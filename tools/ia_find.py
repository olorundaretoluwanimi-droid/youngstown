# ia_find.py <identifier> <query...>: pages (leaf index) in an Internet Archive book that match each query (full-text search inside)
import sys; sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import json, sys, urllib.request, urllib.parse, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ident = sys.argv[1]; m = json.load(open(os.path.join(D, 'research', 'ia', ident + '.json'), encoding='utf-8'))
doc = next(f['name'][:-len('_djvu.txt')] for f in m['files'] if f['name'].endswith('_djvu.txt'))
for q in sys.argv[2:]:
    u = f"https://{m['server']}/fulltext/inside.php?" + urllib.parse.urlencode({'item_id': ident, 'doc': doc, 'path': m['dir'], 'q': q})
    try: r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'documentary-research/1.0'}), timeout=90))
    except Exception as e: print(q, 'ERR', e); continue
    hits = r.get('matches', [])
    print(f"## {q}: {len(hits)}")
    for h in hits[:12]:
        p = h['par'][0]; print('  leaf', p.get('page'), '|', h['text'].replace('\n', ' ')[:110])
