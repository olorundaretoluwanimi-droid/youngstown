#!/bin/sh
# push the used assets (whole folders/files at a time) and the soundtrack pieces in commits of about 20 MB
cd "$(dirname "$0")/.." || exit 1
push() { for i in 1 2 3 4 5 6; do git push -q origin main && return 0; sleep 15; done; return 1; }
batch=0; n=0
for f in $(cat research/used.txt) audio/master; do
  git add -f "$f"; s=$(du -sb "$f" | cut -f1); batch=$((batch + s))
  if [ $batch -gt 20000000 ]; then n=$((n+1)); { git commit -qm "assets b$n" || true; } && push || exit 1; echo "pushed b$n"; batch=0; fi
done
git commit -qm "assets and soundtrack" ; push && echo "pushed final"
