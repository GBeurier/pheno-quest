# Musiques d’Oriane

Ces arrangements MIDI sont joués par le synthétiseur chiptune du jeu et embarqués
dans `js/assets_data.js` : aucun téléchargement pendant la partie.

| Fichier | Niveau | Morceau | Source |
| --- | --- | --- | --- |
| `oriane_niveau1.mid` | L’appart | Bad Bunny — Tití Me Preguntó | [MIDI DB / Hit Trax](https://www.mididb.com/bad-bunny/titi-me-pregunto-midi/) |
| `oriane_niveau2.mid` | La simulation | Darude — Sandstorm | [BitMidi](https://bitmidi.com/darude-sandstorm-mid) |
| `oriane_niveau3.mid` | Le labo | Bad Bunny — DtMF | [MIDI DB / Hit Trax](https://www.mididb.com/bad-bunny/dtmf-midi/) |

Téléchargés le 12 novembre 2026. Les deux Bad Bunny sont des **extraits de
démonstration**, proposés gratuitement par MIDI DB, et non les morceaux complets.
Le téléchargement gratuit ne constitue pas une licence de redistribution ni de
synchronisation ; aucune licence libre n’est revendiquée ici.

Préparation des boucles (sans changer le lecteur partagé) :

- Tití Me Preguntó : fichier `AUD_RC4865.mid`, 480 ticks/noire ; conservation des
  ticks 0 à 23040 (12 mesures à 103 BPM, environ 28 secondes).
- DtMF : fichier `AUD_FV0035.mid`, 48 ticks/noire ; conservation des ticks 384 à
  2688 (12 mesures à 113 BPM, environ 25,5 secondes). Suppression de l’introduction
  silencieuse et du marqueur de fin à 208 secondes qui aurait provoqué un long blanc.
- Les notes encore tenues à la coupe sont fermées ; les réglages d’instruments et
  les métadonnées initiales sont conservés. Le dernier départ de note de DtMF,
  à moins de 40 ms de la coupe, est retiré pour respecter la durée minimale du
  lecteur et conserver une reprise sur la mesure.
- Sandstorm : fichier BitMidi `uploads/37900.mid`, arrangement complet ; tempo
  réglé à 136 BPM (la séquence téléchargée était à 100 BPM).

Après remplacement d’une piste : `python gen_assets_data.py`.
