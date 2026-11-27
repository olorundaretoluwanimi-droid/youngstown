#!/usr/bin/env python3
"""Score, foley and narration for "What Happened to Youngstown? The Day the Steel Mills Closed" → out/mix.wav (48 kHz stereo).
Timing from ../film.json.

THE SCORE: low brass and piano, slow (56 BPM), C minor — a slow-burning sense of injustice that never turns into a cartoon.
One four-bar idea, "the docket" (piano: C–E♭–G–F | E♭–D–C), over Cm – A♭ – Fm – G.
  the charge      — a distant mill whistle on black; a tuba pedal and the docket on solo piano; stops dead at the title cut
  1 opening       — piano and low strings; the horn states the docket in E♭ major (the town being built)
  2 exhibit A     — the warmest part: horn and trombones in A♭/E♭, piano in eighths (the good years)
  3 exhibit B     — darker: trombones and tuba; on Black Monday everything drops to one low piano note and a tuba pedal
  4 witnesses     — a brass chorale (the churches); after the Commerce letter, silence, then the chorale in minor
  5 exhibit C     — a hopeful piano ostinato in E♭ (survival, revival); the car radio cuts it; the occupation: a slow timpani pulse under low brass
  6 trial         — courtroom room tone; contrabass and a single piano note like a clock; violas under the judge's words
  7 defence       — the same restraint, a different colour (cellos and clarinet, G minor): the company gets a fair hearing
  8 verdict       — after the ruling, the full low-brass chorale in C minor; under "Jenny" a single tuba note and a soft gong
  9 jury          — the lift: the docket in A♭ major on horn and strings; at the question it thins to one unresolved piano chord
  end             — the whistle from across town again, then piano alone under the credits
Device sounds: one low WOODEN KNOCK on every case card (no gavel), quiet COURTROOM ROOM TONE under parts 6–8, the series foley
(soft shutter on picture cut-ins, paper for cards and documents, low thump on stamps), a paper slap for exhibit stickers, a phone
click and line hiss for the hot line. Music ducks ≈ 8 dB under the voice."""
import json, os, sys
import numpy as np, soundfile as sf, soxr
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.environ.get('LIB') or os.path.expanduser('~/lemo-opuscar'); sys.path.insert(0, LIB)
from core.audio import sampler as S
from core.audio.sfx import SR, add, bp, hp, lp, noise, env_exp, t_, thump, norm, limit, brown, click
F = json.load(open(os.path.join(D, 'film.json'), encoding='utf-8')); DUR = F['dur']; SC = F['scenes']; VO = {v['id']: v for v in F['voice']}
N = int(DUR * SR); S.seed(6); np.random.seed(6)
BPM = 56; BEAT = 60 / BPM; BAR = 4 * BEAT
ev = []
def E(t, inst, p, d, v=.6, pan=0, g=.3, **k): ev.append(dict(t=t, inst=inst, pitch=p, dur=d, vel=v, pan=pan, gain=g, **k))
def oc(n, k): return n[:-1] + str(int(n[-1]) + k)
CH = {'Cm': ('C2', ['G3', 'C4', 'D#4']), 'Ab': ('G#1', ['G#3', 'C4', 'D#4']), 'Fm': ('F1', ['G#3', 'C4', 'F4']), 'G': ('G1', ['G3', 'B3', 'D4']),
      'Eb': ('D#2', ['G3', 'A#3', 'D#4']), 'Bb': ('A#1', ['A#3', 'D4', 'F4']), 'Gm': ('G1', ['A#3', 'D4', 'G4']), 'Dm7b5': ('D2', ['G#3', 'C4', 'F4']),
      'Db': ('C#2', ['G#3', 'C#4', 'F4']), 'Gsus': ('G1', ['G3', 'C4', 'D4']), 'Cmaj': ('C2', ['G3', 'C4', 'E4']), 'D7': ('D2', ['F#3', 'C4', 'D4'])}
DOCKET = [(0, 'C4', 1), (1, 'D#4', 1), (2, 'G4', 2), (4, 'F4', 2), (6, 'D#4', 1), (7, 'D4', 1), (8, 'C4', 4)]   # beats
def docket(t0, inst, tr=0, v=.5, g=.25, pan=0, tempo=1.0, shift=None):
    for b, p, n in DOCKET:
        pp = oc(p, tr) if not shift else shift.get(p, p)
        E(t0 + b * BEAT / tempo, inst, pp, n * BEAT / tempo * .95, v, pan, g)
def low(bb): return oc(bb, 1) if bb[-1] == '1' else bb
def bars_in(a, b, length=BAR):
    t, i = a, 0
    while t < b - .5: yield t, i; t += length; i += 1
def line(i): return VO[i]['t'], VO[i]['t'] + VO[i]['d']

cards = [s for s in SC if s['type'] == 'case']; title = next(s for s in SC if s['type'] == 'title'); endcard = next(s for s in SC if s['type'] == 'end')
spans = [('hook', 0.0, title['t0'])] + [(f"p{c['n']}", c['t0'], (cards[i + 1]['t0'] if i + 1 < len(cards) else endcard['t0'])) for i, c in enumerate(cards)] + [('end', endcard['t0'], DUR)]

for name, a, b in spans:
    m0 = a + 2.3
    if name == 'hook':
        m0 = 3.2
        E(m0, 'tuba', 'C2', title['t0'] - m0 - .3, .35, 0, .16, attack=2.0)
        E(m0, 'cellos', 'C3', title['t0'] - m0 - .3, .3, -.2, .1, attack=3.0)
        for t, i in bars_in(m0 + BAR, title['t0'] - 2, BAR * 2):
            ch = ['Cm', 'Ab', 'Fm', 'G'][i % 4]; bb, cc = CH[ch]
            E(t, 'piano', low(bb), BAR * 2, .38, -.15, .2)
            for k, p in enumerate(cc): E(t + BEAT * (1 + k), 'piano', p, BAR, .28, .1 * k, .12)
        docket(line('h04')[0], 'piano', 1, v=.42, g=.18, pan=.15)
        E(line('h06')[0], 'horn', 'G3', 6, .38, -.1, .14, attack=1.5); E(line('h06')[0], 'trombone', 'C3', 6, .35, .1, .14, attack=1.5)
    elif name == 'p1':
        for t, i in bars_in(m0, b - .5):
            ch = ['Cm', 'Ab', 'Eb', 'Bb'][i % 4] if i < 8 else ['Eb', 'Ab', 'Cm', 'G'][i % 4]; bb, cc = CH[ch]
            E(t, 'cellos', low(bb), BAR + .3, .42, -.2, .18, attack=.6); E(t, 'violas', cc[0], BAR + .3, .36, .15, .09, attack=.8)
            for k in range(4): E(t + k * BEAT, 'piano', cc[k % 3] if k else low(bb)[:-1] + '3', 1.6, .3, .1, .12)
        docket(m0 + BAR * 4, 'horn', -1, v=.48, g=.22, shift=None)
        docket(m0 + BAR * 12, 'horn', -1, v=.45, g=.2, shift={'C4': 'D#3', 'D#4': 'G3', 'G4': 'A#3', 'F4': 'G#3', 'D4': 'F3'})
    elif name == 'p2':
        for t, i in bars_in(m0, b - .5):
            ch = ['Ab', 'Eb', 'Fm', 'Bb'][i % 4]; bb, cc = CH[ch]
            E(t, 'trombone', cc[0][:-1] + '3', BAR + .3, .36, -.25, .12, attack=.5); E(t, 'tuba', low(bb), BAR + .3, .38, 0, .12, attack=.4)
            for k in range(8): E(t + k * BEAT / 2, 'piano', ([low(bb)[:-1] + '3'] + cc + [oc(cc[1], 1)])[k % 5], .9, .28, .15, .11)
        docket(m0 + BAR * 2, 'horn', -1, v=.5, g=.22, shift={'C4': 'D#3', 'D#4': 'G3', 'G4': 'C4', 'F4': 'A#3', 'D4': 'G#3'})
        docket(m0 + BAR * 10, 'horn', -1, v=.48, g=.2, shift={'C4': 'G#3', 'D#4': 'C4', 'G4': 'D#4', 'F4': 'C#4', 'D4': 'A#3'})
    elif name == 'p3':
        bm = line('c07')[0]; bm1 = line('c10')[1] + .8
        for t, i in bars_in(m0, b - .5):
            if bm - .5 < t + BAR and t < bm1: continue
            ch = ['Cm', 'Fm', 'Ab', 'G'][i % 4]; bb, cc = CH[ch]
            E(t, 'trombone', cc[0][:-1] + '3', BAR + .3, .36, -.2, .13, attack=.6); E(t, 'tuba', low(bb), BAR + .3, .4, 0, .14, attack=.5)
            for k in (0, 2): E(t + k * BEAT, 'piano', cc[1], 1.8, .28, .2, .1)
        E(bm - .2, 'piano', 'C2', bm1 - bm, .45, 0, .28); E(bm - .2, 'tuba', 'C2', bm1 - bm, .35, 0, .14, attack=1.2)
        docket(line('c11')[0], 'piano', 0, v=.4, g=.16)
    elif name == 'p4':
        lt = line('d09')[0]; no = line('d10')[1] + .8
        for t, i in bars_in(m0, b - .5, BAR):
            if lt - .5 < t + BAR and t < no: continue
            minor = t >= no; ch = (['Eb', 'Ab', 'Bb', 'Eb'] if not minor else ['Cm', 'Fm', 'G', 'Cm'])[i % 4]; bb, cc = CH[ch]
            E(t, 'trombone', cc[0][:-1] + '3', BAR, .38, -.3, .14, attack=.3); E(t, 'horn', cc[1], BAR, .36, .1, .13, attack=.3)
            E(t, 'horn', cc[2], BAR, .34, .3, .11, attack=.3); E(t, 'tuba', low(bb), BAR, .38, 0, .14, attack=.3)
        E(lt, 'piano', 'C2', no - lt, .4, 0, .2)
    elif name == 'p5':
        rad = line('e11')[0]; occ = line('e13')[0]
        for t, i in bars_in(m0, b - .5):
            if t + BAR > rad - .3 and t < occ: continue
            if t < rad:
                ch = ['Eb', 'Bb', 'Cm', 'Ab'][i % 4]; bb, cc = CH[ch]
                for k in range(8): E(t + k * BEAT / 2, 'piano', ([low(bb)[:-1] + '3'] + cc + [oc(cc[0], 1)])[k % 5], .8, .27 + .04 * (k % 2 == 0), .1, .11)
                E(t, 'cellos', low(bb), BAR + .3, .36, -.2, .12, attack=.6)
            else:
                ch = ['Cm', 'Ab', 'Fm', 'G'][i % 4]; bb, cc = CH[ch]
                E(t, 'tuba', low(bb), BAR + .2, .42, 0, .15, attack=.6); E(t, 'trombone', cc[0][:-1] + '3', BAR + .2, .4, -.2, .14, attack=.8)
                for k in range(4): E(t + k * BEAT, 'timpani', 'C2' if k % 2 == 0 else 'G1', 1.2, .3 + .05 * (k == 0), 0, .2)
        E(rad - .1, 'piano', 'G#1', 3.5, .4, 0, .2)
        docket(line('e07')[0] + .5, 'horn', -1, v=.42, g=.17, shift={'C4': 'D#3', 'D#4': 'G3', 'G4': 'A#3', 'F4': 'G#3', 'D4': 'F3'})
    elif name in ('p6', 'p7'):
        for t, i in bars_in(m0, b - .5, BAR * 2):
            ch = (['Cm', 'Ab', 'Fm', 'G'] if name == 'p6' else ['Gm', 'Cm', 'D7', 'Gm'])[i % 4]; bb, cc = CH[ch]
            E(t, 'contrabass' if name == 'p6' else 'cellos', low(bb), BAR * 2 + .3, .34, -.1, .12, attack=1.2)
            for k in range(0, 8, 2): E(t + k * BEAT, 'piano', cc[1] if name == 'p6' else oc(cc[2], 0), 1.5, .22, .2, .08)
        if name == 'p6':
            j0, j1 = line('f08')[0], line('f09')[1]
            E(j0, 'violas', 'D#4', j1 - j0 + 2, .3, .2, .08, attack=2.0); E(j0, 'violins', 'G4', j1 - j0 + 2, .28, .35, .06, attack=2.5)
        else:
            for t in (line('g06')[0], line('g12')[0]): E(t, 'clarinet', 'D4', 5, .35, .2, .12, attack=.8)
    elif name == 'p8':
        rul = line('h15')[1]
        for t, i in bars_in(m0, rul - .5, BAR * 2):
            E(t, 'contrabass', 'C2', BAR * 2 + .3, .32, 0, .1, attack=1.0); E(t + BAR, 'piano', 'G3', 2, .22, .2, .07)
        for t, i in bars_in(rul + .3, b - .5):
            jen = line('h20');
            if jen[0] - 1 < t + BAR and t < jen[1] + .5: continue
            ch = ['Cm', 'Ab', 'Fm', 'G'][i % 4]; bb, cc = CH[ch]
            E(t, 'tuba', low(bb), BAR + .3, .45, 0, .16, attack=.4); E(t, 'trombone', cc[0][:-1] + '3', BAR + .3, .42, -.3, .15, attack=.4)
            E(t, 'horn', cc[1], BAR + .3, .4, .1, .13, attack=.4); E(t, 'horn', cc[2], BAR + .3, .38, .3, .11, attack=.4)
        jen = line('h20'); E(jen[0] - .3, 'tuba', 'C2', jen[1] - jen[0] + 1.5, .45, 0, .16, attack=.5); E(jen[0] + .2, 'gong', None, None, .25, 0, .15)
    elif name == 'p9':
        q = line('j12')[0]
        for t, i in bars_in(m0, q - .5):
            ch = ['Ab', 'Eb', 'Fm', 'Bb'][i % 4] if t < line('j09')[0] else ['Ab', 'Fm', 'Cm', 'G'][i % 4]; bb, cc = CH[ch]
            E(t, 'cellos', low(bb), BAR + .3, .38, -.2, .14, attack=.6); E(t, 'violas', cc[0], BAR + .3, .34, .1, .09, attack=.8); E(t, 'violins', cc[2], BAR + .3, .3, .3, .07, attack=1.0)
            for k in range(4): E(t + k * BEAT, 'piano', cc[k % 3] if k else low(bb)[:-1] + '3', 1.6, .28, .1, .11)
        docket(m0 + BAR * 2, 'horn', -1, v=.5, g=.22, shift={'C4': 'G#3', 'D#4': 'C4', 'G4': 'D#4', 'F4': 'C#4', 'D4': 'A#3'})
        # the question: one unresolved chord, held
        for p in ('F2', 'G#3', 'C4', 'D4'): E(q, 'piano', p, 9, .34, .1, .14)
    elif name == 'end':
        te = endcard['t0'] + 3.0
        docket(te, 'piano', 0, v=.4, g=.18, tempo=.85)
        for p in ('C2', 'G3', 'C4', 'D#4'): E(te + 12 * BEAT / .85, 'piano', p, 6, .32, .1, .14)

spans_t = [(a, b) for _, a, b in spans]
def inside(t):
    for a, b in spans_t:
        if a <= t < b: return b
    return DUR
ev = [e for e in ev if e['t'] < DUR - 1]
for e in ev: b = inside(e['t']); e['dur'] = None if e['dur'] is None else max(.1, min(e['dur'], b - e['t'] - .15))
mus = S.render(ev, dur=DUR, master=False)[:N]
if len(mus) < N: mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
mus = S.room(mus, size=.75, mix=.28)
# the cold open stops dead at the title cut; each part's music starts with its narrator line on the card
i0 = int((title['t0'] - .02) * SR); mus[i0:int((title['t0'] + 8.0) * SR)] = 0
for c in cards:
    a_, b_ = int((c['t0'] - .4) * SR), int((c['t0'] + 2.2) * SR); n = b_ - a_; env = np.zeros(n); k = int(.4 * SR); env[:k] = np.linspace(1, 0, k); mus[a_:b_] *= env[:, None]

fx = np.zeros((N, 2), np.float32)
def knock():   # a low wooden knock: a body thump plus a short wood click and a hollow resonance
    d = .9; tt = t_(d)
    body = np.sin(2 * np.pi * 92 * tt) * env_exp(d, .12) + np.sin(2 * np.pi * 184 * tt) * env_exp(d, .05) * .4
    wood = bp(noise(d), 700, 2400) * env_exp(d, .012) * 1.4 + bp(noise(d), 300, 700) * env_exp(d, .06) * .5
    return norm(body * .9 + wood).astype(np.float32)
def shutter(v=1.0):
    d = .09; a_ = hp(noise(d), 2000) * env_exp(d, .006); b_ = np.pad(hp(noise(.05), 1500) * env_exp(.05, .005), (int(.045 * SR), 0))[:len(a_)]; return norm(a_ + b_ * .8) * v
def paper(v=1.0):
    d = .25; return bp(noise(d), 1200, 6000) * env_exp(d, .05) * (1 - np.exp(-t_(d) / .01)) * v
def slap(): d = .18; return (bp(noise(d), 500, 4000) * env_exp(d, .02) + np.sin(2 * np.pi * 140 * t_(d)) * env_exp(d, .03) * .5).astype(np.float32)
def phone(): d = .12; return (hp(noise(d), 1200) * env_exp(d, .008) + bp(noise(d), 300, 900) * env_exp(d, .02) * .5).astype(np.float32)
W_, wsr = sf.read(os.path.join(D, '../title-sequence/audio/whistle.wav')); W_ = soxr.resample(W_, wsr, SR) if wsr != SR else W_
W_ = W_.astype(np.float32) if W_.ndim == 2 else np.repeat(W_[:, None], 2, 1).astype(np.float32)
def far(y): return np.stack([lp(y[:, c], 1800) for c in range(2)], 1).astype(np.float32)
# the title's whistle (the clip's own sound, at −16 LUFS-ish relative), the distant whistle on the open and the close
add(fx, W_[:, 0], title['t0'], .55, -.1); add(fx, W_[:, 1], title['t0'], .55, .1)
fw = far(W_); add(fx, fw[:, 0], .3, .22, -.3); add(fx, fw[:, 1], .3, .22, -.1)
add(fx, fw[:, 0], endcard['t0'] + .2, .2, .2); add(fx, fw[:, 1], endcard['t0'] + .2, .2, .3)
def at_(s, v): return s['t0'] + .4 if v is None else s['t0'] + (-v) * s.get('vd', s['t1'] - s['t0']) if v < 0 else s['t0'] + v
for s in SC:
    ty = s['type']
    if ty == 'case': add(fx, knock(), s['t0'] + .02, .5, 0); add(fx, paper(.6), s['t0'] + .4, .12, .2)
    if ty in ('hero', 'clip', 'pano') and not s.get('noflash') and not s.get('fadeIn'): add(fx, shutter(.6), s['t0'], .13, -.2)
    if ty in ('doc', 'witness', 'passbook'): add(fx, paper(.8), s['t0'] + .2, .2, .2)
    if ty == 'doc':   # a few soft typewriter keys while the page types
        a0, a1 = at_(s, s.get('at', .25)), at_(s, s.get('until', -.92)); n = int((a1 - a0) * 6)
        for i in range(n): add(fx, click(1.4, .35), a0 + i / 6 + np.random.rand() * .05, .012, .2)
    if ty == 'hotline':
        add(fx, phone(), s['t0'] + .1, .25, -.2); d = s['t1'] - s['t0']
        add(fx, (bp(noise(d), 300, 3000) * .05 * np.minimum(1, t_(d) / .3) * np.minimum(1, (d - t_(d)) / .3)).astype(np.float32), s['t0'], .4, -.1)
    for it in s.get('items', []):
        if it['k'] == 'stamp': add(fx, thump(.25, 140), at_(s, it.get('at', .4)), .06, .2)
        if it['k'] == 'ex': add(fx, slap(), at_(s, it.get('at', .4)), .25, .3)
    if ty == 'scale':
        for p in s.get('pans', []): add(fx, thump(.3, 110), at_(s, p.get('at', 0)) + .35, .07, .3 if p['side'] > 0 else -.3)
# room tone: the series' quiet tone everywhere; a courtroom room tone (air handling, a faint hum) under parts 6–8
fx += np.repeat(lp(brown(DUR), 400)[:N, None] * .008, 2, axis=1).astype(np.float32)
for c in cards:
    if c['n'] in (6, 7, 8):
        b = next((x['t0'] for x in cards if x['n'] == c['n'] + 1), DUR); d = b - c['t0']
        y = lp(noise(d), 260) * .5 + bp(noise(d), 900, 2200) * .05 + np.sin(2 * np.pi * 60 * t_(d)) * .02
        y *= np.minimum(1, t_(d) / 2) * np.minimum(1, (d - t_(d)) / 1.5); add(fx, (y * .06).astype(np.float32), c['t0'], 1.0, 0)
# ── narration ──
voc = np.zeros((N, 2), np.float32); spans_v = []
for k, v in VO.items():
    y, sr = sf.read(os.path.join(D, f'audio/vo/{k}.wav')); y = y if y.ndim == 1 else y.mean(1)
    y = soxr.resample(y, sr, SR); y = y / (np.sqrt(np.mean(y[np.abs(y) > .01] ** 2)) + 1e-9) * .11
    add(voc, y.astype(np.float32), v['t'], 1.0, 0); spans_v.append((v['t'], v['t'] + len(y) / SR))
g = np.ones(N)
for a, b in spans_v: g[int(a * SR):int(b * SR)] = np.minimum(g[int(a * SR):int(b * SR)], .4)
from scipy.ndimage import uniform_filter1d
g = uniform_filter1d(g, int(.5 * SR)); mus *= g[:, None]
out = mus * 6.0 + fx * .7 + voc
tail = int(3.0 * SR); out[-tail:] *= np.linspace(1, 0, tail)[:, None]
def tp_limit(x, ceil):
    from scipy.signal import resample_poly
    from scipy.ndimage import maximum_filter1d, minimum_filter1d
    up = resample_poly(x, 4, 1); n = int(.004 * SR * 4)
    gg = np.minimum(1, ceil / np.maximum(maximum_filter1d(np.abs(up), 2 * n + 1), 1e-9)); gg = uniform_filter1d(minimum_filter1d(gg, 2 * n + 1), n)
    return resample_poly(up * gg, 1, 4)[:len(x)]
out = np.stack([tp_limit(limit(out[:, c], .5), .45) for c in range(2)], 1)
os.makedirs(os.path.join(D, 'out'), exist_ok=True); sf.write(os.path.join(D, 'out/mix.wav'), out.astype(np.float32), SR)
def db(a): return 20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-12)
vm = np.zeros(N, bool)
for a, b in spans_v: vm[int(a * SR):int(b * SR)] = True
print('mix', round(DUR, 1), 's | voice', round(db(voc[vm]), 1), 'bed under voice', round(db((mus * 6 + fx * .7)[vm]), 1), "music alone", round(db((mus * 6)[~vm]), 1))
