#!/usr/bin/env bash
# Victory screens of Marcos / Oriane: ONE codex session per screen, SEQUENTIAL
#  (parallel image_gen calls leak into each other). -i refs come from
#  prompts/<name>.refs, resolved in refs/. Idempotent: an existing
#  raw/<name>.png is not regenerated (delete or rename it to redo).
#  Usage: bash _wingen/run.sh [name ...]   then   python _wingen/build.py [name ...]
set -u
cd "$(dirname "$0")/.."
export PATH="$HOME/.local/bin:$PATH"
CODEX="$(command -v codex || echo "$HOME/.local/bin/codex")"
mkdir -p _wingen/raw
NAMES=("$@")
[ "${#NAMES[@]}" -eq 0 ] && NAMES=(bg_oriane_win bg_marcos_win)
for n in "${NAMES[@]}"; do
  [ -f "_wingen/raw/$n.png" ] && { echo "skip $n (raw present)"; continue; }
  ref=()
  while read -r r; do
    r="$(printf '%s' "$r" | tr -d '\r')"; [ -z "$r" ] && continue
    if [ -f "_wingen/refs/$r" ]; then ref+=(-i "_wingen/refs/$r"); else echo "  (ref missing for $n: $r)"; fi
  done < "_wingen/prompts/$n.refs"
  "$CODEX" exec --dangerously-bypass-approvals-and-sandbox "${ref[@]}" \
     < "_wingen/prompts/$n.txt" > "_wingen/gen_$n.log" 2>&1
  [ -f "_wingen/raw/$n.png" ] && echo "raw OK $n" || echo "FAIL $n (no raw)"
done
