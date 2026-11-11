#!/usr/bin/env bash
# Oriane campaign icons: ONE codex session per icon, SEQUENTIAL. Idempotent
#  (an existing raw/<name>.png is not regenerated). ammo_chili_fire uses
#  ammo_chili as -i reference. Then build_oriane.py.
#  Usage: bash _icongen/run_oriane.sh [name ...]
set -u
cd "$(dirname "$0")/.."
export PATH="$HOME/.local/bin:$PATH"
CODEX="$(command -v codex || echo "$HOME/.local/bin/codex")"
mkdir -p _icongen/raw
NAMES=("$@")
[ "${#NAMES[@]}" -eq 0 ] && NAMES=(ammo_chili ammo_chili_fire ammo_pbjar shot_packet shot_nitrogen shot_darkchili shot_darkjar shot_doubt)
for n in "${NAMES[@]}"; do
  [ -f "_icongen/raw/$n.png" ] && { echo "skip $n (raw present)"; continue; }
  ref=()
  [ "$n" = ammo_chili_fire ] && [ -f _icongen/raw/ammo_chili.png ] && ref=(-i _icongen/raw/ammo_chili.png)
  "$CODEX" exec --dangerously-bypass-approvals-and-sandbox "${ref[@]}" \
     < "_icongen/prompts_oriane/$n.txt" > "_icongen/gen_oriane_$n.log" 2>&1
  [ -f "_icongen/raw/$n.png" ] && echo "raw OK $n" || echo "FAIL $n (no raw)"
done
python _icongen/build_oriane.py
