#!/usr/bin/env bash
# Genere les feuilles de boss (move + atk) via codex image_gen puis les regride.
#  SEQUENTIEL (une session codex a la fois : les image_gen en parallele se
#  melangent). Idempotent : un raw deja present n'est pas regenere (supprimer
#  _bossgen/raw/<boss>_{move,atk}_sheet.png pour forcer).
#  Usage : _bossgen/run_batch.sh <boss> [<boss> ...]   (prompts : make_prompts.py)
set -u
cd "$(dirname "$0")/.."
export PATH="$HOME/.local/bin:$PATH"
CODEX="$(command -v codex || echo "$HOME/.local/bin/codex")"
mkdir -p _bossgen/raw
for b in "$@"; do
  log="_bossgen/gen_${b}.log"
  if [ ! -f "_bossgen/raw/${b}_move_sheet.png" ] || [ ! -f "_bossgen/raw/${b}_atk_sheet.png" ]; then
    # optional -i references: one repo-relative path per line in prompts/<boss>.refs
    ref=()
    if [ -f "_bossgen/prompts/${b}.refs" ]; then
      while read -r r; do [ -n "$r" ] && [ -f "$r" ] && ref+=(-i "$r"); done < "_bossgen/prompts/${b}.refs"
    fi
    "$CODEX" exec --dangerously-bypass-approvals-and-sandbox "${ref[@]}" < "_bossgen/prompts/${b}.txt" > "$log" 2>&1
  fi
  for k in move atk; do
    if [ -f "_bossgen/raw/${b}_${k}_sheet.png" ]; then
      python _bossgen/regrid.py "_bossgen/raw/${b}_${k}_sheet.png" "$b" --frames 6 --$k >> "$log" 2>&1
    fi
  done
  echo "DONE $b (move=$([ -f assets/sprites/boss_${b}_move.png ] && echo ok || echo NO) atk=$([ -f assets/sprites/boss_${b}_atk.png ] && echo ok || echo NO))"
done
