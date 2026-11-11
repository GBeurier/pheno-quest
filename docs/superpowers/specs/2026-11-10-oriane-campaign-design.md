# Oriane campaign — "La these d'Oriane" (design)

Date: 2026-11-10. Brief from Greg: `_new_to_add/Concept.txt` (+ chat screenshot, 3 photos of Oriane,
3 NPC portraits, 5 photos of the CIRAD corridor, Intercrop Values logo).

## Intent

Oriane is a PhD student in **crop modelling** (STICS soil-crop model, intercropping). Three levels,
three bosses, then her PhD (win screen). Same tone and 16-bit pixel style as Laura and Marcos.
She must play differently from both: a thrower with a **rolling** special.

Non-goals: changing Laura's or Marcos's gameplay (every engine change is gated by the `chili` kit).

## Oriane's kit (`CHARACTER.kit = 'chili'`, `CONFIG.kits.chili`)

| Key | Laura | Marcos | Oriane |
|---|---|---|---|
| SPACE | seeds | guitar notes | **Chili peppers**: same `arsenal.graines` leveling (P1 1, P2 fan of 3, P3 5 flaming piercing chilis), slight arc + spin. |
| X (hold/release) | pastry lob | power chord | **Peanut-butter jar**: a jar thrown low that **rolls along the ground**, follows slopes/steps down, bounces off walls once, crushes every enemy on its path (pierce), spares NPCs, splats on the boss (AoE). Power = size/damage/range, charge = speed. Costs sun. |
| C | cat | student squad | — (no ally: no charges, 2 medals TEMPS / DATA) |
| Bike `Y` | Laura's bike | — | **Her black city bike + billiard 8-ball helmet** (`oriane_bike`). |

## Levels

1. **`oriane_appart` — "L'appart"**: Laura's apartment map (`LEVEL_MAPS.niveau2`) and the same boss
   **FRANCOIS LE PROPRIO** (`proprietaire`), Oriane's NPCs first in the crowd.
2. **`oriane_simu` — "La simulation"**: inside the crop model. Pixel world: giant screens, code, voxel
   crops, wireframe intercrop plots, glowing code-window platforms. Enemies: R-logo shooters
   (SticsRPacks — she never wanted to touch R), Java coffee-cup chargers (JavaStics), flying pixel
   bugs (`glitch`), printers and mosquitoes reused. Boss **STICS, le modèle qui plante** (the crop model she keeps running and that keeps crashing) (IA `stics`):
   - *calcul*: fans roar, LEDs flash (telegraph) -> bursts of data packets;
   - *azote*: sprays nitrogen droplets that rain down on marked spots ("T'as dilue l'azote dans la
     courbe de STICS ?");
   - *packages*: spawns an R logo (SticsRPacks) or a Java cup (JavaStics);
   - *plantage*: overheats then **crashes** (blue screen, smoke) = punish window (guard 1);
   - P2 (50%): faster cycles, a horizontal "stack trace" laser sweep at jump height, double rain.
3. **`oriane_labo` — "Le labo"**: the real CIRAD corridor from the photos (posters, kitchenette with
   microwave/fridge/water cooler, brown cabinet with wayang puppet and 2CV, office with purple chair).
   Shelf platforms. Final boss **WORIANE** (IA `woriane`), Oriane's dark twin (Wario-style colour swap)
   who embodies her doubts and anxiety:
   - mirrors Oriane: throws dark chilis, bowls dark peanut-butter jars, dashes;
   - *doute*: summons storm clouds of doubt that follow Oriane and drop lightning;
   - *panique* (P2): a panic dash across the arena and a spiral of dark chilis in every direction;
   - *effondrement*: collapses, curled up crying = punish window.
   - Tuning after playtest (2026-11-11): she was too passive -> 160 HP, 15% bigger, aimed potshots while
     pacing, 2 chained attacks per cycle (3 in P2), shorter collapse (1.4 s / 1.0 s). Sprite redone from
     Oriane's photos so she reads as Oriane's Wario-style twin (same face and hair, purple W hoodie, evil grin).
   After Woriane: win screen, **Docteure Oriane**.

## NPCs (`js/npc.js`, `level: 'oriane'` = priority in her 3 levels)

- `head_npc_h_29` Marc Jaeger — "Tu as bien complete ton ADUM ?"
- `head_npc_h_30` Thomas Arsouze — "N'oublie pas de bien distribuer tes calculs !"
- `head_npc_h_31` Remy Vezy — "T'as dilue l'azote dans la courbe de STICS ?"
- Oriane's own NPC head (`head_npc_f_21`) is the character's `npcHead` (not drawn in her own levels).

## Assets (exact names)

Hero: `oriane_idle/run/jump/hurt/throw/duck/dash/dead` (from one 4x4 sheet), `oriane_bike`.
Ammo: `ammo_chili`, `ammo_chili_fire`, `ammo_pbjar`. Boss shots: `shot_packet`, `shot_nitrogen`,
`shot_darkchili`, `shot_darkjar`, `shot_doubt`. Enemies: `enemy_rlogo`, `enemy_javacup`,
`enemy_glitch`. Bosses: `boss_stics_move/atk`, `boss_woriane_move/atk`. Decor: `tile_simu`,
`simu_leg`, `bg_simu_far`, `bg_simu_mid`, `tile_sol_simu`, `bg_olab_a/b`, `tile_sol_olab`.
Screens: `bg_oriane_map`, `bg_oriane_chapter`, `bg_oriane_win`. Heads `head_npc_h_29..31` (+ `_dead`).
Every one of them has a fallback to an existing sprite, so the code runs before the art lands.
Pipelines: `_orianegen/` (hero, decor, screens), `_headgen`, `_icongen` (`*_oriane*`), `_monstgen`,
`_bossgen` (with `.refs`), all generated sequentially with Codex `image_gen`.

## Performance pass (same delivery)

"The game is big and slow": lossy WebP for large opaque/AI-painted images, per-campaign asset packs
loaded on demand (the boot only decodes shared assets + the selected character's pack), plus runtime
hotspots measured with a CPU profile.
