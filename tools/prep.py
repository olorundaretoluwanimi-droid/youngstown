#!/usr/bin/env python3
"""raw/* → assets/ for the page (run with the library's Python, which has PIL):
photos → <name>.jpg (longest side capped); National Archives 1918 photo cards (n_*) → the photograph only (auto-cropped);
line drawings (patents, cutaway, Sasson sketch) → <name>.png as ink on transparent (drawn cream on the dark ground);
the 1963 film and the 2012-era tower time-lapse → assets/film/<clip>/NNN.jpg at 12 fps; assets/sizes.json."""
import os, glob, json, subprocess
from PIL import Image, ImageOps, ImageFilter
Image.MAX_IMAGE_PIXELS = None
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); A = os.path.join(D, 'assets'); os.makedirs(A, exist_ok=True)
INK = set()
CROP = {'panorama1910': (.05, .41, .95, .535), 'ohioworks1905': (.01, .04, .99, .93)}
def fresh(out, src): return os.path.exists(out) and os.path.getmtime(out) > max(os.path.getmtime(src), os.path.getmtime(__file__))
def ink(im, lo=215, span=150):
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=(1, 1))
    a = g.point(lambda v: max(0, min(255, int((lo - v) * 255 / span)))).filter(ImageFilter.GaussianBlur(.5))
    o = Image.new('RGBA', im.size, (42, 32, 24, 255)); o.putalpha(a); bb = a.point(lambda v: 255 if v > 40 else 0).getbbox()
    return o.crop(bb) if bb else o
def photo_box(im):   # the darkest large rectangle on a cream page: rows/cols where most pixels are darker than the paper
    g = ImageOps.grayscale(im).resize((400, int(400 * im.height / im.width))); w, h = g.size; px = g.load()
    paper = sorted(px[x, y] for x in range(0, w, 7) for y in range(0, h, 7))[-len(range(0, w, 7)) * len(range(0, h, 7)) // 5]
    dark = lambda v: v < paper - 38
    rows = [sum(dark(px[x, y]) for x in range(w)) / w for y in range(h)]; cols = [sum(dark(px[x, y]) for y in range(h)) / h for x in range(w)]
    ys = [y for y, r in enumerate(rows) if r > .45]; xs = [x for x, c in enumerate(cols) if c > .35]
    if not ys or not xs: return None
    s = im.width / w; return (int(xs[0] * s) + 6, int(ys[0] * s) + 6, int((xs[-1] + 1) * s) - 6, int((ys[-1] + 1) * s) - 6)
for f in sorted(glob.glob(os.path.join(D, 'raw', '*'))):
    name, ext = os.path.splitext(os.path.basename(f))
    if ext.lower() not in ('.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif'): continue
    out = os.path.join(A, name + ('.png' if name in INK else '.jpg'))
    if fresh(out, f): continue
    im = Image.open(f).convert('RGB')
    if name in INK: im = ink(im); im.thumbnail((2400, 2400), Image.LANCZOS); im.save(out); print('ink', name, im.size); continue
    if name in CROP: W_, H_ = im.size; f = CROP[name]; im = im.crop((int(W_ * f[0]), int(H_ * f[1]), int(W_ * f[2]), int(H_ * f[3])))
    if name.startswith('n_'):
        b = photo_box(im)
        if b: im = im.crop(b)
    if max(im.size) > 2600: im.thumbnail((2600, 2600), Image.LANCZOS)
    im.save(out, quality=90); print(name, im.size)
# ── film clips: (clip, source, start s, end s, width) ──
CLIPS = [('c_houses', 'film_steeltown', 44, 56, 640),
         ('c_shift', 'film_steeltown', 62, 92, 640),
         ('c_bridge', 'film_steeltown', 108, 126, 640),
         ('c_mill', 'film_steeltown', 126, 142, 640),
         ('c_furnace', 'film_steeltown', 150, 170, 640),
         ('c_pour', 'film_steeltown', 196, 214, 640),
         ('c_iron', 'film_steeltown', 222, 238, 640),
         ('c_goggles', 'film_steeltown', 238, 252, 640),
         ('c_face', 'film_steeltown', 268, 278, 640),
         ('c_home', 'film_steeltown', 278, 300, 640),
         ('c_family', 'film_steeltown', 300, 318, 640),
         ('c_ohfloor', 'film_steeltown', 330, 372, 640),
         ('c_tapper', 'film_steeltown', 428, 446, 640),
         ('c_hats', 'film_steeltown', 446, 454, 640),
         ('c_football', 'film_steeltown', 456, 480, 640),
         ('c_oldman', 'film_steeltown', 492, 502, 640),
         ('c_school', 'film_steeltown', 512, 560, 640),
         ('c_leave', 'film_steeltown', 560, 568, 640),
         ('c_sparks', 'film_steeltown', 574, 590, 640),
         ('c_orch', 'film_steeltown', 620, 652, 640),
         ('c_tap', 'film_steeltown', 700, 724, 640),
         ('c_bfext', 'film_steeltown', 750, 758, 640),
         ('c_slab', 'film_steeltown', 804, 816, 640),
         ('c_committee', 'film_steeltown', 828, 842, 640),
         ('c_gate', 'film_steeltown', 890, 926, 640),
         ('c_skyline', 'film_steeltown', 926, 958, 640)]
NCLIP = {}
for c, src, a, b, w in CLIPS:
    d = os.path.join(A, 'film', c); s = os.path.join(D, 'raw', src + '.mp4')
    if not (os.path.isdir(d) and os.listdir(d)):
        os.makedirs(d, exist_ok=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-i', s, '-t', str(b - a), '-vf', f'fps=12,crop=972:704:154:8,scale={w}:-2', '-q:v', '3', os.path.join(d, '%03d.jpg')], check=True)
    NCLIP[c] = len(os.listdir(d))
sizes = {}
for p in glob.glob(os.path.join(A, '*.jpg')) + glob.glob(os.path.join(A, '*.png')):
    im = Image.open(p); sizes[os.path.splitext(os.path.basename(p))[0]] = list(im.size)
json.dump(sizes, open(os.path.join(A, 'sizes.json'), 'w'), indent=0); json.dump(NCLIP, open(os.path.join(A, 'clips.json'), 'w'))
print(len(sizes), 'pictures,', NCLIP)
