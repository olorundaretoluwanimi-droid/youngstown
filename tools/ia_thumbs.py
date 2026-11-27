# ia_thumbs.py <identifier> <first> <last> [w]: page thumbnails of an IA book → research/thumbs/<id>_nK.jpg, then a contact sheet
import sys, os, urllib.request, subprocess, time
ident, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); w = sys.argv[4] if len(sys.argv) > 4 else '260'
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); out = []
for k in range(a, b + 1):
    f = os.path.join(D, 'research', 'thumbs', f'{ident}_n{k}.jpg')
    if not os.path.exists(f):
        for t in range(3):
            try: open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(f'https://archive.org/download/{ident}/page/n{k}_w{w}.jpg', headers={'User-Agent': 'documentary-research/1.0'}), timeout=60).read()); break
            except Exception as e: time.sleep(3)
    if os.path.exists(f): out.append(f)
subprocess.run([sys.executable, os.path.join(D, 'tools', 'sheet.py'), os.path.join(D, 'research', f'sheet_{ident}_{a}.jpg'), '8', '240'] + out)
