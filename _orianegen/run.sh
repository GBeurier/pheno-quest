#!/usr/bin/env bash
# Oriane campaign art: ONE codex session per asset, SEQUENTIAL (parallel
#  image_gen calls leak into each other). -i refs are read from
#  prompts/<name>.refs and resolved in refs/ first, then raw/ (so a later asset
#  can use an earlier raw as reference, e.g. oriane_bike <- oriane_sheet).
#  Idempotent: an existing raw/<name>.png is not regenerated.
#  Usage: bash _orianegen/run.sh [name ...]   then   python _orianegen/build.py [name ...]
set -u
cd "$(dirname "$0")/.."
export PATH="$HOME/.local/bin:$PATH"
CODEX="$(command -v codex || echo "$HOME/.local/bin/codex")"
mkdir -p _orianegen/raw
NAMES=("$@")
[ "${#NAMES[@]}" -eq 0 ] && NAMES=(oriane_sheet oriane_bike oriane_bike_cannon tile_simu simu_leg bg_simu_far bg_simu_mid tile_sol_simu
  olab_p1 olab_p2 olab_p3 tile_sol_olab bg_oriane_map bg_oriane_chapter bg_oriane_win)
for n in "${NAMES[@]}"; do
  [ -f "_orianegen/raw/$n.png" ] && { echo "skip $n (raw present)"; continue; }
  ref=()
  if [ -f "_orianegen/prompts/$n.refs" ]; then
    while read -r r; do
      r="$(printf '%s' "$r" | tr -d '\r')"; [ -z "$r" ] && continue   # .refs may be CRLF on Windows
      if [ -f "_orianegen/refs/$r" ]; then ref+=(-i "_orianegen/refs/$r")
      elif [ -f "_orianegen/raw/$r" ]; then ref+=(-i "_orianegen/raw/$r")
      else echo "  (ref missing for $n: $r)"; fi
    done < "_orianegen/prompts/$n.refs"
  fi
  "$CODEX" exec --dangerously-bypass-approvals-and-sandbox "${ref[@]}" \
     < "_orianegen/prompts/$n.txt" > "_orianegen/gen_$n.log" 2>&1
  [ -f "_orianegen/raw/$n.png" ] && echo "raw OK $n" || echo "FAIL $n (no raw)"
done
