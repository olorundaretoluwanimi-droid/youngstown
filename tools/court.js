
// ════════════════════════════════════════════════════════════════════════════════════════════════════════
// Episode 6 · Youngstown — the courtroom device. Case caption cards (a pleading's caption box draws itself), exhibit stickers
// (plaintiffs' yellow, defendant's blue, as in a real courtroom), witness cards, court-record pages with line numbers, the hot-line
// recording, the Save Our Valley passbook, the Commerce letter, the scales, the Mahoning River map, the jury box.
// ════════════════════════════════════════════════════════════════════════════════════════════════════════
function town(p, name, o = {}) { x.save(); x.globalAlpha *= o.a ?? 1; x.fillStyle = o.c || C.red; x.beginPath(); x.arc(p[0], p[1], o.r || 8, 0, 7); x.fill();
  x.strokeStyle = C.cream; x.lineWidth = 1.5; x.stroke(); if (name) txt(name, p[0] + (o.dx ?? 16), p[1] + (o.dy ?? 9), { s: o.s || 30, w: 500, c: C.cream, al: o.al || 'left', id: o.id, sh: 'rgba(0,0,0,.8)' }); x.restore(); }
const PL_Y = '#E3C04B', DF_B = '#86A9C8', INK = '#1d1712';
const PARTS = ['The Charge', 'Opening Statement', 'Exhibit A', 'Exhibit B', 'The Witnesses', 'Exhibit C', 'The Trial', 'The Defence', 'The Verdict', 'The Jury'];

// exhibit sticker: slaps on (1.3× → 1, tiny bounce), slight tilt
function sticker(label, no, X, Y, t, t0, side = 'p', o = {}) {
  const k = seg(t, t0, t0 + .16); if (k <= 0) return; const sc = lerp(1.35, 1, eback(k)), w = o.w || 330, h = o.h || 128;
  x.save(); x.translate(X, Y); x.rotate((o.rot ?? -3.5) * Math.PI / 180); x.scale(sc, sc); x.globalAlpha *= clamp(k * 3);
  x.shadowColor = 'rgba(0,0,0,.55)'; x.shadowBlur = 18; x.shadowOffsetY = 6; x.fillStyle = side === 'd' ? DF_B : PL_Y; rr(-w / 2, -h / 2, w, h, 10); x.fill();
  x.shadowColor = 'transparent'; x.strokeStyle = 'rgba(20,15,10,.55)'; x.lineWidth = 2; rr(-w / 2 + 8, -h / 2 + 8, w - 16, h - 16, 6); x.stroke();
  txt(label, 0, -h / 2 + 40, { s: 19, f: 'Mono', w: 600, ls: 2, c: INK, al: 'center' }); hair(-w / 2 + 30, -h / 2 + 54, w / 2 - 30, -h / 2 + 54, 'rgba(20,15,10,.45)', 1.5);
  txt(no, 0, h / 2 - 22, { s: 50, w: 700, c: INK, al: 'center', id: 'ex' + no });
  x.restore();
}
// a court-record page: line numbers in the margin, a double rule, typed text revealed word by word, red underlines on key phrases
function wrapWords(words, maxW, o) { const lines = [[]]; let w = 0; const sp = measure(' ', o);
  for (const wd of words) { const m = measure(wd.replace(/[*_]/g, ''), o); if (w + m > maxW && lines[lines.length - 1].length) { lines.push([]); w = 0; } lines[lines.length - 1].push(wd); w += m + sp; } return lines; }
function recordPage(s, t, X, Y, w, h, o = {}) {
  paperCard(X, Y, w, h, t);
  // line numbers + margin rules
  const LH = o.lh || 50, n = Math.floor((h - 150) / LH);
  for (let i = 0; i < n; i++) txt(String(i + 1), X + 50, Y + 140 + i * LH, { s: 18, f: 'Mono', w: 400, c: '#9b8c74', al: 'right' });
  hair(X + 70, Y + 20, X + 70, Y + h - 20, '#c98478', 1.5); hair(X + 76, Y + 20, X + 76, Y + h - 20, '#c98478', 1.5); hair(X + w - 50, Y + 20, X + w - 50, Y + h - 20, '#c9b9a0', 1);
  txt(s.head || '', X + 100, Y + 64, { s: 20, f: 'Mono', w: 600, ls: 2, c: '#5a4b3a', id: 'rh' }); if (s.head2) txt(s.head2, X + 100, Y + 92, { s: 18, f: 'Mono', w: 400, ls: 1, c: '#7a6a55', id: 'rh2' });
  hair(X + 100, Y + 108, X + w - 70, Y + 108, '#b9a888', 1);
  // body
  const fo = { s: o.fs || 31, f: 'Mono', w: 400 }, words = s.text.split(/\s+/), lines = wrapWords(words, w - 200, fo), total = words.length;
  const a0 = AT(s, s.at ?? .25), a1 = AT(s, s.until ?? -.92), shown = Math.floor(total * seg(t, a0, a1)); let k = 0;
  lines.forEach((ln, li) => { let cx = X + 100; const yy = Y + 140 + li * LH; ln.forEach(wd => { const hl = wd.includes('*'), clean = wd.replace(/[*_]/g, ''), m = measure(clean, fo);
      if (k < shown) { txt(clean, cx, yy, { ...fo, c: hl ? '#7a1f12' : INK, w: hl ? 600 : 400, id: 'rb' + k });
        if (hl) { const kk = seg(t, a0 + (a1 - a0) * (k + 1) / total, a0 + (a1 - a0) * (k + 1) / total + .35); hair(cx - 4, yy + 9, cx - 4 + (m + measure(' ', fo) + 4) * kk, yy + 9, C.red, 3); } }
      cx += m + measure(' ', fo); k++; }); });
  if (k > shown && Math.floor(t * 3) % 2 === 0) { const li = lines.findIndex((_, i) => lines.slice(0, i + 1).flat().length > shown); }
  if (s.cite) txt(s.cite, X + 100, Y + h - 36, { s: 17, f: 'Mono', w: 600, ls: 1, c: '#7a6a55', id: 'rc', a: seg(t, a1, a1 + .4) });
}
function sDoc(t, s) {   // a page from the court record, the hot line, or a letter
  if (s.img) { cover(IM[s.img], 0, 0, W, H, { z: lerp(1.08, 1.16, LK(t, s)), fx: s.fx, fy: s.fy, grade: s.grade }); shade(0, 0, W, H, .82); }
  else if (s.clip) { clipFrame(s.clip, 0, 0, W, H, t - s.t0, { z: 1.1 }); shade(0, 0, W, H, .82); }
  const w = s.w || 1300, h = s.h || 860, X = (W - w) / 2 + (s.dx || 0), Y = 70, k = seg(t, s.t0, s.t0 + .45), z = lerp(1, 1.035, LK(t, s));
  x.save(); x.globalAlpha = k; x.translate(W / 2, H / 2); x.scale(z, z); x.translate(-W / 2, -H / 2 + (1 - eo(k)) * 50); recordPage(s, t, X, Y, w, h, s); x.restore();
  if (s.stamp) stamp(s.stamp, s.sx ?? X + w - 220, s.sy ?? Y + h - 110, t, AT(s, s.stampAt ?? -.75), { s: s.ss || 58, rot: -6, seed: 3, id: 'ds' });
  if (s.tag) srcTag(s.tag, X, Y + h + 34, 1, 'dt');
  items(t, s, s.items);
}

// the case caption: the start of every part
function sCase(t, s) {
  const l = t - s.t0; ground();
  // faint paper texture panel
  x.save(); x.globalAlpha = .06; x.fillStyle = GRAIN[Math.floor(t * 30) % 6]; x.fillRect(0, 0, W, H); x.restore();
  const X = 250, Y = 150, cw = 1420;
  const head = 'UNITED STATES DISTRICT COURT · NORTHERN DISTRICT OF OHIO';
  typed(head, W / 2, Y, t, s.t0 + .05, .45, { s: 24, c: C.dim, al: 'center' });
  const L1 = ['LOCAL 1330, UNITED STEEL WORKERS', 'OF AMERICA, et al.,', '            Plaintiffs,', 'v.', 'UNITED STATES STEEL CORPORATION,', '            Defendant.'];
  L1.forEach((ln, i) => typed(ln, X + 40, Y + 90 + i * 44, t, s.t0 + .35 + i * .12, .22, { s: 28, w: ln.startsWith(' ') || ln === 'v.' ? 400 : 600, c: C.cream }));
  // the ) column and the right box
  const kc = seg(l, .3, 1.1); for (let i = 0; i < 7; i++) if (kc > i / 7) txt(')', X + 760, Y + 90 + i * 40, { s: 28, f: 'Mono', c: C.dim });
  hair(X + 20, Y + 360, X + 20 + 740 * eo(seg(l, .5, 1.1)), Y + 360, C.dim, 2);
  typed('CASE NO. C 79-2337 Y', X + 830, Y + 150, t, s.t0 + .9, .3, { s: 28, c: C.cream });
  typed('JUDGE THOMAS D. LAMBROS', X + 830, Y + 200, t, s.t0 + 1.05, .3, { s: 24, c: C.dim });
  stamp(s.n === 0 ? 'THE CHARGE' : 'PART ' + s.n, X + 1080, Y + 300, t, s.t0 + 1.0, { s: 54, rot: -4, seed: s.n + 2, id: 'cp' });
  drop(s.title, W / 2, 720, t, s.t0 + 1.35, { s: 92, al: 'center', id: 'ct' });
  if (s.sub) txt(s.sub, W / 2, 790, { s: 36, it: 1, c: C.dim, al: 'center', a: seg(l, 1.9, 2.3), id: 'cs' });
  docket(t, s.n, 880, seg(l, .2, .6));
}
function docket(t, n, Y, a = 1) {   // ten parts on the docket, this one lit
  const w = 150, g = 8, X0 = W / 2 - (10 * w + 9 * g) / 2;
  x.save(); x.globalAlpha *= a;
  for (let i = 0; i < 10; i++) { const X = X0 + i * (w + g), cur = i === n, done = i < n;
    x.fillStyle = cur ? C.red : done ? '#4a3d30' : '#241d17'; x.fillRect(X, Y, w, 10);
    txt(i === 0 ? '·' : String(i), X, Y + 40, { s: 18, f: 'Mono', w: 600, c: cur ? C.cream : C.faint });
    txt(PARTS[i].toUpperCase(), X, Y + 64, { s: 13, f: 'Mono', w: 600, ls: 1, c: cur ? C.cream : C.faint }); }
  x.restore();
}

// witness card: a person's own words appear in silence (the narrator never speaks as a worker)
function sWitness(t, s) {
  const a0 = s.t0;
  if (s.img) { cover(IM[s.img], 60, 60, 700, 860, { z: lerp(1.05, 1.1, LK(t, s)), fy: s.fy ?? .35, grade: 'b' }); shade(60, 60, 700, 860, .3); if (s.imgTag) srcTag(s.imgTag, 60, 46, 1, 'wi'); }
  else if (s.clip) { clipFrame(s.clip, 60, 60, 700, 860, t - s.t0, { z: 1.08 }); shade(60, 60, 700, 860, .3); if (s.imgTag) srcTag(s.imgTag, 60, 46, 1, 'wi'); }
  const k = seg(t, a0 + .1, a0 + .35), X = (s.img || s.clip) ? 820 : 300, w = (s.img || s.clip) ? 1040 : 1320;
  x.save(); x.globalAlpha = k; x.translate(0, (1 - eo(k)) * 40); paperCard(X, 60, w, 860, t);
  x.fillStyle = INK; x.fillRect(X, 60, w, 58); txt('WITNESS · FOR THE PLAINTIFFS', X + 40, 99, { s: 22, f: 'Mono', w: 600, ls: 4, c: C.paper });
  x.restore();
  const lines = s.q, LH = 88, y0 = 60 + (860 - (lines.length - 1) * LH) / 2 - 10;
  lines.forEach((q, i) => txt(q, X + 80, y0 + i * LH, { s: 62, it: 1, c: INK, a: seg(t, a0 + .45 + i * .35, a0 + .75 + i * .35), id: 'w' + i }));
  const kk = seg(t, a0 + 1.1, a0 + 1.5); x.save(); x.globalAlpha = kk; x.fillStyle = C.red; x.fillRect(X + 80, 790, 5, 84); x.restore();
  txt(s.who, X + 104, 822, { s: 36, w: 700, c: INK, a: kk, id: 'ww' }); txt(s.role, X + 104, 860, { s: 21, f: 'Mono', w: 600, c: C.ink2, a: kk, id: 'wr' });
  srcTag(s.src, X, 958, kk, 'ws');
}

// the hot line: a handset, a recording level, the message typed
function handset(X, Y, sc, a = 1) {
  x.save(); x.translate(X, Y); x.scale(sc, sc); x.globalAlpha *= a; x.strokeStyle = C.cream; x.lineWidth = 7; x.lineCap = 'round';
  x.beginPath(); x.moveTo(-150, -40); x.quadraticCurveTo(0, -130, 150, -40); x.stroke();
  for (const sx of [-1, 1]) { x.save(); x.translate(sx * 160, -20); x.rotate(sx * .5); rr(-45, -30, 90, 70, 16); x.stroke(); x.restore(); }
  x.restore();
}
function sHotline(t, s) {
  ground(); const l = t - s.t0, k = seg(l, 0, .4);
  handset(330, 360, 1.05, k);
  // level bars
  for (let i = 0; i < 28; i++) { const v = .15 + .85 * Math.abs(Math.sin(NOW * 7 + i * .9) * Math.sin(NOW * 2.3 + i * .37)), on = l < (s.vd || 99) + .3;
    x.fillStyle = on ? (i % 7 === 0 ? C.red : C.dim) : C.faint; const hh = (on ? v : .08) * 120; x.fillRect(170 + i * 12, 560 - hh / 2, 7, hh); }
  txt('U.S. STEEL · YOUNGSTOWN WORKS', 330, 690, { s: 22, f: 'Mono', w: 600, ls: 3, c: C.dim, al: 'center', a: k });
  txt('“HOT LINE” · RECORDED MESSAGE', 330, 724, { s: 22, f: 'Mono', w: 600, ls: 3, c: C.dim, al: 'center', a: k });
  if (s.date) stamp(s.date, 330, 820, t, s.t0 + .35, { s: 52, rot: -4, seed: 4, id: 'hd' });
  if (s.who) txt(s.who, 330, 910, { s: 30, w: 700, al: 'center', a: seg(l, .5, .9), id: 'hw' });
  const pg = { ...s, head: s.head || 'RECORDED MESSAGE', head2: s.head2 };
  recordPage(pg, t, 700, 90, 1120, 800, { fs: 40, lh: 64 });
  if (s.tag) srcTag(s.tag, 700, 930, 1, 'ht');
}

// Save Our Valley passbook
function sPassbook(t, s) {
  if (s.img) { cover(IM[s.img], 0, 0, W, H, { z: 1.12, grade: 'b' }); shade(0, 0, W, H, .8); }
  const X = 360, Y = 130, w = 1200, h = 760, k = seg(t, s.t0, s.t0 + .5);
  x.save(); x.globalAlpha = k; x.fillStyle = '#5b2f22'; rr(X - 14, Y - 14, w + 28, h + 28, 18); x.fill(); paperCard(X, Y, w / 2 - 6, h, t); paperCard(X + w / 2 + 6, Y, w / 2 - 6, h, t);
  txt('SAVE OUR VALLEY', X + w / 4, Y + 130, { s: 50, w: 700, c: INK, al: 'center', id: 'pb1' }); txt('SAVINGS ACCOUNT', X + w / 4, Y + 180, { s: 26, f: 'Mono', w: 600, ls: 4, c: C.ink2, al: 'center' });
  txt('MAHONING VALLEY', X + w / 4, Y + 400, { s: 24, f: 'Mono', w: 600, ls: 3, c: C.ink2, al: 'center' }); txt('“Renew the life of our valley.”', X + w / 4, Y + 470, { s: 30, it: 1, c: INK, al: 'center' });
  const R = X + w / 2 + 50; txt('DATE', R, Y + 70, { s: 18, f: 'Mono', w: 600, c: C.ink2 }); txt('DEPOSIT', R + 380, Y + 70, { s: 18, f: 'Mono', w: 600, c: C.ink2, al: 'right' }); hair(R, Y + 84, R + 480, Y + 84, '#b9a888', 1);
  const rows = [['FEB 16 1978', '25.00'], ['FEB 20 1978', '100.00'], ['MAR 03 1978', '10.00'], ['APR 11 1978', '5,000.00'], ['JUN 02 1978', '50.00'], ['AUG 19 1978', '10,000.00']];
  rows.forEach(([d, v], i) => { const a = seg(t, AT(s, .3) + i * .28, AT(s, .3) + i * .28 + .2); txt(d, R, Y + 130 + i * 48, { s: 24, f: 'Mono', c: INK, a }); txt(v, R + 380, Y + 130 + i * 48, { s: 24, f: 'Mono', c: INK, al: 'right', a }); });
  txt('ILLUSTRATIVE ENTRIES', R, Y + 440, { s: 16, f: 'Mono', w: 600, ls: 2, c: '#9b8c74' });
  x.restore();
  const a1 = AT(s, s.countAt ?? 2.2), kc = eo(seg(t, a1, a1 + 1.8));
  if (t > a1) { txt(num(Math.round(4138 * kc)) + ' ACCOUNTS', R, Y + 560, { s: 40, f: 'Mono', w: 600, c: C.red, id: 'pa' }); txt('$' + num(Math.round(4014927 * kc)), R, Y + 640, { s: 64, f: 'Mono', w: 600, c: C.red, id: 'pd' });
    txt('BY NOVEMBER 1978', R, Y + 690, { s: 20, f: 'Mono', w: 600, ls: 2, c: C.ink2, a: seg(t, a1 + 1.8, a1 + 2.2) }); }
  srcTag('FIGURES · LYND, THE FIGHT AGAINST SHUTDOWNS (1982)', X, Y + h + 50, .9);
}

// the scales: two pans, weights dropped on with labels; tilt from the weights (or forced level)
function sScale(t, s) {
  ground(); const cx = W / 2, cy = 330, P = s.pans || [];
  let wl = 0, wr = 0; P.forEach(p => { const k = seg(t, AT(s, p.at), AT(s, p.at) + .5); (p.side < 0 ? (wl += k * p.w) : (wr += k * p.w)); });
  let tilt = clamp((wr - wl) * .12, -.22, .22); if (s.level != null) tilt = lerp(tilt, 0, eio(seg(t, AT(s, s.level), AT(s, s.level) + 1.4)));
  tilt += Math.sin((t - s.t0) * 2.1) * .006 * (1 - seg(t, s.t0 + 4, s.t0 + 8));
  x.save(); x.strokeStyle = C.dim; x.lineWidth = 7; hair(cx, cy - 10, cx, 900, C.dim, 8); x.fillStyle = C.dim; rr(cx - 140, 890, 280, 24, 6); x.fill();
  x.beginPath(); x.arc(cx, cy - 26, 18, 0, 7); x.fill();
  x.translate(cx, cy); x.rotate(tilt); hair(-600, 0, 600, 0, C.cream, 8);
  for (const side of [-1, 1]) { x.save(); x.translate(side * 600, 0); x.rotate(-tilt); hair(0, 0, -170, 280, C.dim, 2.5); hair(0, 0, 170, 280, C.dim, 2.5);
    x.fillStyle = '#3a3027'; x.beginPath(); x.ellipse(0, 290, 210, 30, 0, 0, Math.PI); x.fill(); x.strokeStyle = C.dim; x.lineWidth = 2; x.beginPath(); x.ellipse(0, 290, 210, 30, 0, 0, 7); x.stroke();
    txt(side < 0 ? 'THE PLAINTIFFS' : 'THE DEFENDANT', 0, 380, { s: 24, f: 'Mono', w: 600, ls: 3, c: side < 0 ? PL_Y : DF_B, al: 'center', id: 'sp' + side });
    let stack = 0; P.filter(p => p.side === side).forEach((p, i) => { const a0 = AT(s, p.at), k = seg(t, a0, a0 + .45); if (k <= 0) return; const yy = 285 - stack - 50 - (1 - eback(k)) * 260;
      x.save(); x.globalAlpha = clamp(k * 3); x.fillStyle = side < 0 ? PL_Y : DF_B; rr(-200, yy - 46, 400, 92, 8); x.fill();
      txt(p.big, 0, yy + 4, { s: p.big.length > 9 ? 36 : 46, f: 'Mono', w: 600, c: INK, al: 'center', id: 'sb' + side + i }); txt(p.small || '', 0, yy + 34, { s: 15, f: 'Mono', w: 600, ls: 1, c: INK, al: 'center' }); x.restore(); stack += 100; });
    x.restore(); }
  x.restore();
  if (s.title) txt(s.title, cx, 120, { s: 28, f: 'Mono', w: 600, ls: 3, c: C.dim, al: 'center', id: 'stl' });
  if (s.note) txt(s.note, cx, 1000 - 20, { s: 18, f: 'Mono', w: 600, c: C.faint, al: 'center' });
  items(t, s, s.items);
}

// the Mahoning River, Warren to Lowellville (schematic, drawn from coordinates)
const RIVER = [[41.262, -80.836], [41.240, -80.815], [41.215, -80.790], [41.185, -80.768], [41.168, -80.737], [41.160, -80.718], [41.150, -80.700], [41.128, -80.676], [41.108, -80.664],
  [41.097, -80.646], [41.088, -80.625], [41.073, -80.607], [41.060, -80.600], [41.046, -80.580], [41.037, -80.556], [41.031, -80.530], [41.025, -80.505]];
const TOWNS = { Warren: [41.2376, -80.8184], Niles: [41.1828, -80.7654], McDonald: [41.1612, -80.7240], Girard: [41.1539, -80.7017], Youngstown: [41.0998, -80.6495],
  Campbell: [41.0784, -80.5992], Struthers: [41.0526, -80.6076], Lowellville: [41.0359, -80.5365] };
const MILLS = { mcd: ['McDonald Works', 41.157, -80.722, 'U.S. STEEL · 1918', [-30, 60]], ohio: ['Ohio Works', 41.112, -80.672, 'U.S. STEEL · 1901', [-40, 70]],
  brier: ['Brier Hill Works', 41.124, -80.660, 'SHEET & TUBE · “JENNY”', [30, -40]], camp: ['Campbell Works', 41.066, -80.605, 'SHEET & TUBE', [40, 50]] };
function mproj(lat, lon) { const k = Math.cos(41.15 * Math.PI / 180), sc = 3308; return [960 + (lon + 80.675) * k * sc, 110 + (41.275 - lat) * sc]; }
function sRiver(t, s) {
  const c = camAt(s, t); ground();
  withCam(c, () => {
    // Ohio / Pennsylvania line
    const pa = mproj(41.3, -80.519), pb = mproj(41.0, -80.519); x.save(); x.setLineDash([14 / c.z, 10 / c.z]); hair(pa[0], pa[1], pb[0], pb[1], C.faint, 2 / c.z); x.setLineDash([]); x.restore();
    txt('OHIO', pa[0] - 30 / c.z, 980, { s: 26 / c.z, f: 'Mono', w: 600, ls: 4, c: C.faint, al: 'right' }); txt('PENNSYLVANIA', pa[0] + 30 / c.z, 980, { s: 26 / c.z, f: 'Mono', w: 600, ls: 4, c: C.faint });
    const kr = eio(seg(t, AT(s, s.riverAt ?? 0), AT(s, s.riverAt ?? 0) + (s.riverDur ?? 2.6))), n = RIVER.length - 1, upto = kr * n;
    x.save(); x.strokeStyle = '#4f6f7a'; x.lineWidth = 16 / c.z; x.lineCap = 'round'; x.lineJoin = 'round'; x.beginPath();
    for (let i = 0; i <= Math.ceil(upto); i++) { const f = Math.min(1, upto - i + 1), p = mproj(...RIVER[i]); if (i === 0) { x.moveTo(...p); continue; }
      const q = mproj(...RIVER[i - 1]); x.lineTo(lerp(q[0], p[0], f), lerp(q[1], p[1], f)); } x.stroke(); x.restore();
    if (kr > .2) txt('MAHONING RIVER', ...mproj(41.205, -80.79), { s: 24 / c.z, f: 'Mono', w: 600, ls: 3, c: '#7c9aa4', a: seg(kr, .2, .5) });
    for (const [name, at] of s.towns || []) { const k = seg(t, AT(s, at), AT(s, at) + .3); if (k > 0) town(mproj(...TOWNS[name]), name, { a: k, r: (name === 'Youngstown' ? 11 : 7) / c.z, s: (name === 'Youngstown' ? 40 : 28) / c.z, c: C.dim, dx: 14 / c.z, dy: -10 / c.z, id: 'tw' + name }); }
    for (const [id, at, st] of s.mills || []) { const m = MILLS[id], p = mproj(m[1], m[2]), k = seg(t, AT(s, at), AT(s, at) + .35); if (k <= 0) continue;
      const off = typeof st === 'number' ? seg(t, AT(s, st), AT(s, st) + .6) : st === 'off' ? 1 : 0, col = off > .5 ? C.faint : C.red, r = 18 / c.z;
      if (off < 1) { const gl = x.createRadialGradient(p[0], p[1], 0, p[0], p[1], r * 4); gl.addColorStop(0, `rgba(229,81,47,${.45 * (1 - off) * k * (.8 + .2 * Math.sin(NOW * 5))})`); gl.addColorStop(1, 'rgba(229,81,47,0)'); x.fillStyle = gl; x.fillRect(p[0] - r * 4, p[1] - r * 4, r * 8, r * 8); }
      x.save(); x.globalAlpha = k; x.fillStyle = col; x.fillRect(p[0] - r / 2, p[1] - r / 2, r, r); x.strokeStyle = C.cream; x.lineWidth = 2 / c.z; x.strokeRect(p[0] - r / 2, p[1] - r / 2, r, r);
      const lx = p[0] + m[4][0] / c.z, ly = p[1] + m[4][1] / c.z, al = m[4][0] < 0 ? 'right' : 'left';
      txt(m[0], lx, ly, { s: 34 / c.z, w: 700, c: off > .5 ? C.dim : C.cream, al, sh: 'rgba(0,0,0,.9)', id: 'ml' + id }); txt(off > .5 && s.closed?.[id] ? s.closed[id] : m[3], lx, ly + 30 / c.z, { s: 18 / c.z, f: 'Mono', w: 600, ls: 1, c: off > .5 ? C.red : C.dim, al, id: 'ms' + id });
      x.restore(); }
  });
  if (s.note) { const k = seg(t, AT(s, s.note.at ?? .3), AT(s, s.note.at ?? .3) + .4); txt(s.note.a, 120, 150, { s: 54, w: 700, a: k, id: 'na', sh: 'rgba(0,0,0,.9)' }); if (s.note.b) txt(s.note.b, 120, 202, { s: 26, f: 'Mono', w: 600, c: C.dim, a: k, id: 'nb', ls: 1 }); }
  srcTag('MAP · SCHEMATIC, DRAWN FROM COORDINATES · MILL POSITIONS APPROXIMATE', 60, 1060 - 20, .6);
  items(t, s, s.items);
}

// ~10,000 steel jobs in three waves, each dot = 50 jobs
function sDots(t, s) {
  const N = 200, cols = 25, gap = 34, X0 = W / 2 - (cols - 1) * gap / 2, Y0 = 200, R = rnd(5);
  const W1 = [[0, 100, 'CAMPBELL WORKS · 1977', '5,000'], [100, 130, 'BRIER HILL · 1979', '1,500'], [130, 200, 'OHIO + McDONALD WORKS · 1980', '3,500']], a0 = AT(s, s.at ?? .1);
  for (let i = 0; i < N; i++) { const c = i % cols, r = Math.floor(i / cols), px = X0 + c * gap, py = Y0 + r * gap, ap = seg(t, a0 + i * .004, a0 + i * .004 + .2); if (ap <= 0) continue;
    const wv = W1.findIndex(w => i >= w[0] && i < w[1]), fa = s.falls?.[wv], d = R() * .7, f = fa == null ? 0 : clamp((seg(t, AT(s, fa), AT(s, fa) + 1.6) - d * .5) / .5);
    x.save(); x.globalAlpha = ap * (1 - f); x.fillStyle = wv === 0 ? C.red : wv === 1 ? '#d08a52' : C.cream; x.beginPath(); x.arc(px, py + f * f * 300, 12 * (1 - f * .4), 0, 7); x.fill(); x.restore(); }
  W1.forEach(([a, b, lab, n], i) => { const fa = s.falls?.[i]; const k = fa == null ? seg(t, a0 + .6, a0 + 1) : seg(t, AT(s, fa), AT(s, fa) + .4);
    txt(n, 260 + i * 520, 760, { s: 64, f: 'Mono', w: 600, c: i === 0 ? C.red : i === 1 ? '#d08a52' : C.cream, a: k, id: 'dn' + i }); txt(lab, 260 + i * 520, 800, { s: 20, f: 'Mono', w: 600, ls: 2, c: C.dim, a: k, id: 'dl' + i }); });
  txt('EACH DOT = 50 STEEL JOBS IN YOUNGSTOWN', W / 2, 150, { s: 24, f: 'Mono', w: 600, ls: 3, c: C.dim, al: 'center', id: 'dt' });
  if (s.total) stamp('≈ 10,000', W / 2, 900, t, AT(s, s.total), { s: 80, seed: 6, id: 'dtt' });
  srcTag('SOURCE · LYND, THE FIGHT AGAINST SHUTDOWNS (1982)', 60, 60, .7);
}
// Youngstown population at each census
const POP = [[1880, 15435], [1890, 33220], [1900, 44885], [1910, 79066], [1920, 132358], [1930, 170002], [1940, 167720], [1950, 168330], [1960, 166689], [1970, 139788], [1980, 115436], [1990, 95732], [2000, 82026], [2010, 66982], [2020, 60068]];
function sLine(t, s) {
  const X = 220, Y = 170, w = 1480, h = 620, px = yr => X + (yr - 1880) / 140 * w, py = v => Y + h - v / 200000 * h, k = eio(seg(t, AT(s, s.at ?? .1), AT(s, s.at ?? .1) + (s.draw || 2.4)));
  txt('YOUNGSTOWN, OHIO · POPULATION AT EACH CENSUS', X, Y - 50, { s: 26, f: 'Mono', w: 600, ls: 2, c: C.dim, id: 'lt' });
  for (const v of [50000, 100000, 150000]) { hair(X, py(v), X + w, py(v), '#2a231b', 1); txt(num(v), X - 16, py(v) + 8, { s: 20, f: 'Mono', c: C.faint, al: 'right' }); }
  for (let yr = 1880; yr <= 2020; yr += 20) txt(String(yr), px(yr), Y + h + 40, { s: 22, f: 'Mono', c: C.faint, al: 'center' });
  if (s.band) { const a = px(1977), b = px(1980); x.save(); x.globalAlpha = .25 * seg(t, AT(s, s.band), AT(s, s.band) + .5); x.fillStyle = C.red; x.fillRect(a, Y, b - a, h); x.restore();
    txt('1977–80', (a + b) / 2, Y - 12, { s: 20, f: 'Mono', w: 600, c: C.red, al: 'center', a: seg(t, AT(s, s.band), AT(s, s.band) + .5) }); }
  const yEnd = lerp(1880, 2020, k); x.save(); x.strokeStyle = C.cream; x.lineWidth = 5; x.beginPath();
  POP.forEach(([yr, v], i) => { if (yr > yEnd + 10) return; const yy = Math.min(yr, yEnd); let vv = v; if (yr > yEnd && i) { const [y0, v0] = POP[i - 1]; vv = lerp(v0, v, (yEnd - y0) / 10); }
    i ? x.lineTo(px(yy), py(vv)) : x.moveTo(px(yy), py(vv)); }); x.stroke(); x.restore();
  for (const [yr, lab] of s.marks || []) { const v = POP.find(p => p[0] === yr)[1]; if (yEnd < yr) continue; town([px(yr), py(v)], '', { r: 10 });
    txt(num(v), px(yr), py(v) - 30, { s: 40, f: 'Mono', w: 600, c: C.red, al: 'center', id: 'lm' + yr }); if (lab) txt(lab, px(yr), py(v) - 80, { s: 24, f: 'Mono', w: 600, c: C.dim, al: 'center', id: 'll' + yr }); }
  srcTag('SOURCE · U.S. CENSUS', X, Y + h + 90, .8);
}
// a wide panorama slides past in a band
function sPano(t, s) {
  const im = IM[s.img]; if (!im) return; const bh = s.bh || 520, sc = bh / im.height, bw = im.width * sc, k = eio(LK(t, s)), Y = (H - bh) / 2 - 40;
  const X = lerp(s.from ?? 0, s.to ?? -(bw - W), k);
  x.save(); x.filter = (ERAS[s.grade || 'b'] || ERAS.m).f; x.drawImage(im, X, Y, bw, bh); x.filter = 'none';
  x.globalCompositeOperation = 'overlay'; x.globalAlpha = .15; x.fillStyle = GRAIN[Math.floor(NOW * 30) % 6]; x.fillRect(0, Y, W, bh); x.restore();
  hair(0, Y, W, Y, C.line, 1); hair(0, Y + bh, W, Y + bh, C.line, 1); srcTag(s.tag, 60, Y - 16, 1, 'pt'); items(t, s, s.items);
}
// the jury box: twelve empty chairs
function chair(X, Y, sc, a) { x.save(); x.translate(X, Y); x.scale(sc, sc); x.globalAlpha *= a; x.strokeStyle = '#8a7258'; x.lineWidth = 4; x.fillStyle = '#2a2119';
  rr(-38, -110, 76, 90, 10); x.fill(); x.stroke(); rr(-46, -24, 92, 22, 6); x.fill(); x.stroke(); hair(-36, -2, -36, 46, '#8a7258', 4); hair(36, -2, 36, 46, '#8a7258', 4); x.restore(); }
function sJury(t, s) {
  ground(); const l = t - s.t0, z = lerp(1, 1.12, eio(LK(t, s)));
  x.save(); x.translate(W / 2, H / 2); x.scale(z, z); x.translate(-W / 2, -H / 2);
  const g = x.createRadialGradient(W / 2, 380, 50, W / 2, 380, 900); g.addColorStop(0, 'rgba(246,213,138,.10)'); g.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  for (let r = 0; r < 2; r++) for (let i = 0; i < 6; i++) chair(560 + i * 160 + (r ? 0 : 0), 420 + r * 190, r ? 1.1 : .95, seg(l, .2 + (r * 6 + i) * .06, .5 + (r * 6 + i) * .06));
  // the rail / box front
  x.fillStyle = '#3a2c20'; x.fillRect(420, 560, 1080, 30); x.fillRect(420, 760, 1080, 220); x.strokeStyle = '#8a7258'; x.lineWidth = 3; x.strokeRect(420, 760, 1080, 220);
  for (let i = 0; i < 6; i++) { x.strokeRect(450 + i * 175, 790, 150, 160); }
  for (let i = 0; i <= 14; i++) hair(420 + i * 77, 590, 420 + i * 77, 760, '#5a4632', 5);
  x.restore();
  txt('THE JURY', W / 2, 120, { s: 26, f: 'Mono', w: 600, ls: 8, c: C.dim, al: 'center', a: seg(l, .3, .8) });
  if (s.lines) s.lines.forEach((ln, i) => drop(ln, W / 2, 200 + i * 80, t, AT(s, s.at?.[i] ?? .2 + i), { s: 60, al: 'center', w: 700, c: i === s.lines.length - 1 && s.redLast ? C.red : C.cream, id: 'jl' + i }));
}
// the black opening: a distant whistle on black
function sBlack(t, s) { ground(); }
// title placeholder (the Mill Town title sequence is spliced in here at the finish)
function sTitle(t, s) { ground(); txt('MILL TOWN', W / 2, H / 2, { s: 60, w: 700, c: C.faint, al: 'center' }); }
// end: credits over the skyline
function sEnd(t, s) {
  const l = t - s.t0; cover(IM['skyline'], 0, 140, W, 727, { z: lerp(1, 1.04, LK(t, s)), grade: 'm' }); shade(0, 0, W, H, lerp(.35, .9, seg(l, 3, 5)));
  const L = FILM.credits || []; L.forEach((c, i) => txt(c, W / 2, 230 + i * 50, { s: i === 0 ? 42 : 23, f: i === 0 ? 'Sans' : 'Mono', w: i === 0 ? 700 : 600, c: i === 0 ? C.cream : C.dim, al: 'center', a: seg(l, 3.5 + i * .15, 4.2 + i * .15), id: 'cr' + i }));
}
// big type on the ground with an optional dim picture or clip behind
function sType(t, s) {
  if (s.img) { cover(IM[s.img], 0, 0, W, H, { z: lerp(1.08, 1.16, LK(t, s)), fx: s.fx, fy: s.fy, grade: s.grade }); shade(0, 0, W, H, s.dim ?? .78); }
  else if (s.clip) { clipFrame(s.clip, 0, 0, W, H, t - s.t0, { z: 1.1 }); shade(0, 0, W, H, s.dim ?? .78); }
  const n = s.lines.length, y0 = 540 - (n - 1) * 70, b0 = AT(s, s.at ?? .1);
  s.lines.forEach((ln, i) => drop(ln, W / 2, y0 + i * 140, t, b0 + i * (s.step ?? .5), { s: s.s || 120, al: 'center', id: 'ty' + i, c: i === s.redLine ? C.red : C.cream }));
  if (s.sub) txt(s.sub, W / 2, y0 + n * 140 - 20, { s: 38, it: 1, c: C.dim, al: 'center', a: seg(t, b0 + n * .5, b0 + n * .5 + .4), id: 'tys' });
  srcTag(s.tag, 60, 60, .8); items(t, s, s.items);
}
const SCN = { hero: sHero, pair: sPair, clip: sClip, case: sCase, doc: sDoc, witness: sWitness, hotline: sHotline, passbook: sPassbook, scale: sScale, river: sRiver,
  dots: sDots, line: sLine, pano: sPano, jury: sJury, black: sBlack, title: sTitle, end: sEnd, type: sType };

// ── frame ───────────────────────────────────────────────────────────────────────────────────────────────
function caseMark(s) {   // a quiet docket line in the top-right corner during the parts
  if (!s.part || ['case', 'black', 'title', 'end', 'jury'].includes(s.type)) return;
  txt('LOCAL 1330 v. U.S. STEEL · ' + (s.part === 0 ? 'THE CHARGE' : 'PART ' + s.part + ' · ' + PARTS[s.part].toUpperCase()), W - 40, 1068, { s: 16, f: 'Mono', w: 600, ls: 2, c: C.faint, al: 'right' });
}
function drawScene(s, t) { ERA = s.era || 'm'; ground(); (SCN[s.type] || ground)(t, s); }
function render(t) {
  NOW = t; x.setTransform(1, 0, 0, 1, 0, 0); x.globalAlpha = 1; x.filter = 'none'; ground();
  const i = FILM.scenes.findIndex(s => t >= s.t0 && t < s.t1), s = FILM.scenes[i] || FILM.scenes[FILM.scenes.length - 1]; if (!s) return;
  const p = FILM.scenes[i - 1];
  if (p && s.xf && t < s.t0 + s.xf) { drawScene(p, t); const k = seg(t, s.t0, s.t0 + s.xf); x.save(); x.globalAlpha = k; drawScene(s, t); x.restore(); }
  else drawScene(s, t);
  caseMark(s);
  // fade to the ground into each case card (the knock lands on the card)
  const nx = FILM.scenes[i + 1]; if (nx && (nx.type === 'case' || nx.type === 'title') && t > s.t1 - .45) { const k = seg(t, s.t1 - .45, s.t1); x.save(); x.globalAlpha = k; x.fillStyle = C.bg; x.fillRect(0, 0, W, H); x.restore(); }
  if (s.type === 'black' || s.type === 'hero' && s.fadeIn) { const k = 1 - seg(t, s.t0, s.t0 + (s.fadeIn || 1.2)); if (s.type !== 'black' && k > 0) { x.save(); x.globalAlpha = k; x.fillStyle = '#000'; x.fillRect(0, 0, W, H); x.restore(); } }
  subs(t);
}
window.render = render;
window.TEXTS = t => { REC = []; render(t); const r = REC; REC = null; return r; };
(async () => {
  await Promise.all(['400 40px Sans', '500 40px Sans', '700 40px Sans', '400 40px Mono', '600 40px Mono', 'italic 400 40px SerifI'].map(f => document.fonts.load(f)));
  try { FILM = await (await fetch('film.json')).json(); } catch (e) { console.warn('no film.json'); }
  SIZES = await (await fetch('assets/sizes.json')).json(); CLIPN = await (await fetch('assets/clips.json')).json();
  SPECK = makeSpeck(); makeGrain();
  const names = new Set(['skyline']); JSON.stringify(FILM, (k, v) => { if (typeof v === 'string' && /^[a-z0-9_]+$/.test(v) && v.length > 2) names.add(v); return v; });
  const L = []; for (const n of names) { if (SIZES[n]) L.push(load(`assets/${n}.jpg`).then(im => { if (im) { im._n = n; IM[n] = im; } }));
    if (CLIPN[n]) { CLIP[n] = []; for (let i = 1; i <= CLIPN[n]; i++) L.push(load(`assets/film/${n}/${String(i).padStart(3, '0')}.jpg`).then(im => { CLIP[n][i - 1] = im; })); } }
  await Promise.all(L);
  window.DUR = FILM.dur; window.READY = true; render(0);
})();
</script></body></html>
