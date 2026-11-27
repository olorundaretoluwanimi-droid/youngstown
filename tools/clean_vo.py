#!/usr/bin/env python3
"""Clean narration lines: remove breaths, shorten long pauses, trim the ends, soft fades at every cut.

  clean_vo.py <in_dir> <out_dir> [--report]      # every <id>.wav → <out_dir>/<id>.wav + <out_dir>/clean.json (what was cut)

How: 10 ms frames → level (dB re the line's loud speech) and "voicing" (share of energy below 1 kHz). The line splits into
islands of sound separated by silence (≥ 60 ms below −48 dB). An island is a BREATH when it is short (0.08–0.9 s), quiet
(peak below −12 dB) and unvoiced (low-band share < 0.45) — or anything quiet before the first word / after the last one.
Breaths are replaced by silence of the same length, then every silence inside the line is capped: ≥ 0.42 s → 0.34 s
(sentence breaks keep a natural beat; commas, under 0.42 s, are left alone). Cuts get 12 ms equal-power fades; the last word keeps 120 ms of
tail with an 80 ms fade (no sudden stop); 25 ms pad at both ends. Run with the library's Python (numpy + soundfile)."""
import sys, os, json, glob
import numpy as np, soundfile as sf

FR = 0.010
def analyse(y, sr):
    n = int(FR * sr); m = len(y) // n; f = y[:m * n].reshape(m, n)
    rms = np.sqrt((f ** 2).mean(1) + 1e-12); db = 20 * np.log10(rms)
    spec = np.abs(np.fft.rfft(f * np.hanning(n), axis=1)) ** 2; fr = np.fft.rfftfreq(n, 1 / sr)
    low = spec[:, (fr > 70) & (fr < 1000)].sum(1) / (spec[:, fr > 70].sum(1) + 1e-12)
    ref = np.percentile(db[db > db.max() - 40], 90) if (db > db.max() - 40).any() else db.max()
    return db - ref, low, n

def islands(rel, thr=-48, gap=6):
    on = rel > thr; out = []; i = 0; m = len(on)
    while i < m:
        if not on[i]: i += 1; continue
        j = i
        while j < m:
            if on[j]: j += 1; continue
            k = j
            while k < m and not on[k]: k += 1
            if k - j >= gap or k >= m: break
            j = k
        out.append([i, j]); i = j
    return out

def clean(y, sr):
    rel, low, n = analyse(y, sr); isl = islands(rel); cut = []
    voiced = lambda a, b: low[a:b][rel[a:b] > rel[a:b].max() - 12].mean()
    speech = [(a, b) for a, b in isl if voiced(a, b) > .45 or rel[a:b].max() > -12 or (b - a) * FR > .9]
    if not speech: return y, {'breaths': [], 'pauses': []}
    first, last = speech[0][0], speech[-1][1]
    keep = np.ones(len(rel), bool); keep[:max(0, first - 2)] = False; keep[min(len(rel), last + 12):] = False
    prev_end = {}; pe = 0
    for a, b in isl: prev_end[a] = pe; pe = b
    for a, b in isl:
        if (a, b) in speech or b <= first - 2 or a >= last + 12: continue
        if (a - prev_end[a]) * FR < .15 and rel[a:b].max() > -30: continue   # right after a word: a final s, t or k, not a breath
        # short loud islands are consonant releases (kept); breaths are longer or very quiet
        d = (b - a) * FR; pk = rel[a:b].max(); v = low[a:b][rel[a:b] > pk - 12].mean()
        if (0.12 <= d <= 0.9 or (d >= 0.05 and pk < -35)) and v < .45: keep[a:b] = False; cut.append(('breath', round(a * FR, 2), round(d, 2), round(float(pk), 1)))
    # silences inside the line (frames not in a speech island) → cap long ones
    sil = np.ones(len(rel), bool)
    for a, b in isl:   # every island that isn't a breath is sound to keep (final s, t, k included)
        if keep[a:b].all(): sil[a:b] = False
    segs = []; i = first
    while i < last:
        if sil[i]:
            j = i
            while j < last and sil[j]: j += 1
            segs.append((i, j)); i = j
        else: i += 1
    out = []; pos = max(0, first - 2) * n; pauses = []
    for a, b in segs:
        out.append(('keep', pos, a * n)); d = (b - a) * FR
        tgt = 0.34 if d >= 0.42 else d
        if d >= 0.42: pauses.append((round(a * FR, 2), round(d, 2)))
        out.append(('sil', int(tgt * sr))); pos = b * n
    out.append(('keep', pos, min(len(y), (last + 12) * n)))
    fd = int(.012 * sr); pieces = [np.zeros(int(.025 * sr))]
    for o in out:
        if o[0] == 'sil': pieces.append(np.zeros(o[1])); continue
        s = y[o[1]:o[2]].copy()
        # silence any breath frames that fall inside a kept stretch
        for k in range(o[1] // n, (o[2] + n - 1) // n):
            if k < len(keep) and not keep[k]: a0, b0 = max(o[1], k * n) - o[1], min(o[2], (k + 1) * n) - o[1]; s[a0:b0] = 0
        if len(s) > 2 * fd:
            r = np.sin(np.linspace(0, np.pi / 2, fd)) ** 2; s[:fd] *= r; s[-fd:] *= r[::-1]
        pieces.append(s)
    t = pieces[-1]; fo = min(len(t), int(.08 * sr)); t[-fo:] *= np.cos(np.linspace(0, np.pi / 2, fo)) ** 2   # natural tail, no sudden stop
    pieces.append(np.zeros(int(.025 * sr)))
    return np.concatenate(pieces), {'breaths': cut, 'pauses': pauses, 'in': round(len(y) / sr, 2)}

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True); rep = {}
    for f in sorted(glob.glob(os.path.join(src, '*.wav'))):
        y, sr = sf.read(f, dtype='float32')
        if y.ndim > 1: y = y.mean(1)
        z, info = clean(y, sr); info['out'] = round(len(z) / sr, 2); rep[os.path.basename(f)[:-4]] = info
        sf.write(os.path.join(dst, os.path.basename(f)), z, sr, subtype='PCM_16')
        if '--report' in sys.argv: print(os.path.basename(f), info)
    json.dump(rep, open(os.path.join(dst, 'clean.json'), 'w'), indent=1)
    b = sum(len(v['breaths']) for v in rep.values()); p = sum(len(v['pauses']) for v in rep.values())
    print(len(rep), 'lines;', b, 'breaths removed;', p, 'long pauses shortened;', round(sum(v['in'] - v['out'] for v in rep.values()), 1), 's saved')
