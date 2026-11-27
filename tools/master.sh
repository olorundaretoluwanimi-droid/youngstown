#!/bin/sh
# out/mix.wav → audio/master/soundtrack.m4a.partNN: two-pass loudnorm to −14 LUFS / −1 dBTP, AAC 320k, split into 7 MB pieces
# (pushes over ≈ 30 MB fail on the user's connection, so each piece goes up in its own commit).
cd "$(dirname "$0")/.." || exit 1
J=$(ffmpeg -hide_banner -i out/mix.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
v() { echo "$J" | grep "\"$1\"" | sed 's/.*: "\(.*\)".*/\1/'; }
ffmpeg -hide_banner -loglevel error -y -i out/mix.wav -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(v input_i):measured_TP=$(v input_tp):measured_LRA=$(v input_lra):measured_thresh=$(v input_thresh):offset=$(v target_offset):linear=true,aresample=48000" \
  -c:a aac -b:a 320k out/soundtrack.m4a
ffmpeg -hide_banner -i out/soundtrack.m4a -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
rm -rf audio/master && mkdir -p audio/master && split -b 7M -d -a 2 out/soundtrack.m4a audio/master/soundtrack.m4a.part && ls -l audio/master
