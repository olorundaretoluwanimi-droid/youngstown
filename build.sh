#!/bin/sh
# One command, from the project folder: assets → timeline → mix → master pieces. The picture is rendered on GitHub (render.yml),
# the soundtrack is joined to it there (finish.yml). Local preview of any range: node tools/render_range.mjs <a> <b> (from $LIB).
set -e
LIB=${LIB:-/c/Users/HP/lemo-opuscar}; export LIB
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
PY="$LIB/.venv/Scripts/python.exe"; [ -x "$PY" ] || PY="$LIB/.venv/bin/python"
sh tools/get_raw.sh                       # public-domain / CC material → raw/ (logged in SOURCES.jsonl)
"$PY" tools/prep.py                       # raw/ → assets/ (+ 1906 page crops, ink drawings, 12 fps film clips)
python -I tools/mapdata.py                # Natural Earth → assets/map.json
python -I tools/make_lines.py             # script → audio/lines.json, script.md
# narration (AI33 credits!): python -I ../tools/tts_ai33.py lines audio/lines.json audio/vo_raw
"$PY" tools/clean_vo.py audio/vo_raw audio/vo   # breaths out, long pauses shortened, soft tails
"$PY" -c "import json,glob,os,soundfile as sf;json.dump({os.path.basename(f)[:-4]:round(sf.info(f).duration,3) for f in glob.glob('audio/vo/*.wav')},open('audio/vo/dur.json','w'))"
python -I tools/build_film.py             # → film.json, audio/cues.json
[ "${STOP_BEFORE_MIX:-0}" = 1 ] && exit 0
"$PY" audio/mix.py                        # score + foley + voice → out/mix.wav
sh tools/master.sh                        # → audio/master/soundtrack.m4a.partNN (−14 LUFS)
