# asr_check.py: transcribe every cleaned narration line (faster-whisper small.en) and flag lines whose words differ from the script
import json, os, re, sys, difflib
from faster_whisper import WhisperModel
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = [l for l in json.load(open(os.path.join(D, 'audio/lines.json'), encoding='utf-8')) if l['text']]
m = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=2)
norm = lambda s: re.sub(r"[^a-z0-9' ]", ' ', s.lower()).split()
out = []
for l in L:
    segs, _ = m.transcribe(os.path.join(D, 'audio/vo', l['id'] + '.wav'), beam_size=1)
    got = ' '.join(s.text for s in segs).strip(); r = difflib.SequenceMatcher(None, norm(l['text']), norm(got)).ratio()
    out.append(dict(id=l['id'], ratio=round(r, 3), want=l['text'], got=got)); print(l['id'], round(r, 3), flush=True)
json.dump(out, open(os.path.join(D, 'audio/asr.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
