/* =====================================================================
 *  CONTROLS — player-configurable key bindings (window.LQ_CONTROLS)
 *  ---------------------------------------------------------------------
 *  Loaded AFTER save.js (prefs) and BEFORE mobile.js / game.js: the stored
 *  bindings are applied IN PLACE to window.CONFIG.controls at load, so every
 *  reader (game.js through C.controls, mobile.js, the mute listener) sees the
 *  player's keys. Bindings are a GLOBAL preference (prefs key 'controls',
 *  shared by every character and slot), like the audio toggles.
 *
 *  Key names are KAPLAY's: e.key lowercased, arrows -> left/right/up/down,
 *  ' ' -> space (cf. fromEvent).
 *
 *  Each action shows two editable slots (keys[0], keys[1]); extra legacy
 *  aliases (e.g. 'a' for QWERTY on left) are kept until they conflict.
 *  Assigning a key already used elsewhere:
 *   - another GAMEPLAY action whose ONLY key it is gets our old key (swap),
 *     so no action is ever left without a key;
 *   - otherwise the key is simply removed from the other action (a mute
 *     toggle may end up unbound: shown as '--' in the screen).
 * ===================================================================== */
window.LQ_CONTROLS = (() => {
  'use strict';
  const CFG = (window.CONFIG && window.CONFIG.controls) || {};
  const SV = window.LQ_SAVE;

  // Editable actions, in screen order. kind 'play' = gameplay (never left unbound).
  const ACTIONS = [
    { id: 'left',      label: 'Gauche',                 kind: 'play' },
    { id: 'right',     label: 'Droite',                 kind: 'play' },
    { id: 'jump',      label: 'Sauter',                 kind: 'play' },
    { id: 'crouch',    label: 'Accroupi / descendre',   kind: 'play' },
    { id: 'shoot',     label: 'Tir principal',          kind: 'play' },
    { id: 'lob',       label: 'Tir special (maintenir)', kind: 'play' },
    { id: 'cat',       label: 'Allie (chat, etudiants)', kind: 'play' },
    { id: 'dash',      label: 'Dash',                   kind: 'play' },
    { id: 'muteSfx',   label: 'Couper les bruitages',   kind: 'sys' },
    { id: 'muteMusic', label: 'Couper la musique',      kind: 'sys' },
  ];
  const IDS = ACTIONS.map((a) => a.id);
  const DEFAULTS = {};
  IDS.forEach((id) => { DEFAULTS[id] = (CFG[id] || []).slice(); });

  // Keys that can never be bound: ESC opens the quit box / goes back.
  const RESERVED = ['escape'];

  const LABELS = {
    space: 'ESPACE', shift: 'MAJ', enter: 'ENTREE', control: 'CTRL', alt: 'ALT',
    left: 'GAUCHE', right: 'DROITE', up: 'HAUT', down: 'BAS', tab: 'TAB',
    backspace: 'RETOUR', delete: 'SUPPR', capslock: 'VERR MAJ', insert: 'INSER',
    home: 'DEBUT', end: 'FIN', pageup: 'PAGE HAUT', pagedown: 'PAGE BAS',
    altgraph: 'ALT GR', contextmenu: 'MENU', meta: 'META',
  };
  // Bitmap font: no accents -> transliterate the few AZERTY letters with one.
  const PLAIN = { 'é': 'E', 'è': 'E', 'ê': 'E', 'à': 'A', 'ù': 'U', 'ç': 'C', '²': '2', '§': 'S', 'µ': 'U' };
  function label(k) {
    if (!k) return '--';
    if (LABELS[k]) return LABELS[k];
    if (PLAIN[k]) return PLAIN[k];
    return String(k).toUpperCase();
  }

  // KeyboardEvent -> KAPLAY key name (same normalisation as the engine).
  const ENGINE = { ArrowLeft: 'left', ArrowRight: 'right', ArrowUp: 'up', ArrowDown: 'down', ' ': 'space' };
  const fromEvent = (e) => ENGINE[e.key] || String(e.key || '').toLowerCase();

  const keys = (id) => CFG[id] || (CFG[id] = []);
  const kindOf = (id) => (ACTIONS.find((a) => a.id === id) || {}).kind;

  function persist() {
    if (!SV || !SV.setPref) return;
    const out = {};
    IDS.forEach((id) => { out[id] = keys(id).slice(); });
    try { SV.setPref('controls', out); } catch (_) {}
  }

  // Replace the content of the live array (references held elsewhere stay valid).
  const setKeys = (id, arr) => { const a = keys(id); a.length = 0; arr.forEach((k) => a.push(k)); };

  function apply(map) {
    if (!map || typeof map !== 'object') return;
    IDS.forEach((id) => {
      const v = map[id];
      if (!Array.isArray(v)) return;
      const clean = v.filter((k, i) => typeof k === 'string' && k && RESERVED.indexOf(k) < 0 && v.indexOf(k) === i);
      if (clean.length || kindOf(id) === 'sys') setKeys(id, clean);
    });
  }

  // Bind `key` to slot `slot` (0 | 1) of action `id`.
  //  Returns null on success, or the label of the action that blocks it
  //  ('reserved' for ESC): binding a gameplay action's ONLY key into an
  //  empty slot would leave that action unbound, so it is refused.
  function bind(id, slot, key) {
    if (IDS.indexOf(id) < 0 || !key || RESERVED.indexOf(key) >= 0) return 'reserved';
    const mine = keys(id);
    const old = mine[slot];
    if (old === key) return null;
    const already = mine.indexOf(key);
    if (already >= 0) {                       // already ours: swap the two slots
      if (old) mine[already] = old; else mine.splice(already, 1);
      mine[Math.min(slot, mine.length)] = key;
      persist();
      return null;
    }
    const lone = (other) => other !== id && kindOf(other) === 'play' && keys(other).length === 1 && keys(other)[0] === key;
    const blocker = IDS.find(lone);
    if (blocker && !old) return (ACTIONS.find((a) => a.id === blocker) || {}).label || blocker;
    IDS.forEach((other) => {
      if (other === id) return;
      const ok = keys(other);
      const i = ok.indexOf(key);
      if (i < 0) return;
      if (lone(other)) ok[i] = old;           // swap: the other action takes our old key
      else ok.splice(i, 1);
    });
    if (slot < mine.length) mine[slot] = key; else mine.push(key);
    persist();
    return null;
  }

  // Clear slot 1 (the secondary key); slot 0 of a gameplay action stays bound.
  function clear(id, slot) {
    const mine = keys(id);
    if (slot >= mine.length) return false;
    if (kindOf(id) === 'play' && mine.length <= 1) return false;
    mine.splice(slot, 1);
    persist();
    return true;
  }

  function reset() {
    IDS.forEach((id) => setKeys(id, DEFAULTS[id]));
    persist();
  }

  const isDefault = () => IDS.every((id) => keys(id).join(',') === DEFAULTS[id].join(','));
  // Label of the main key of an action (HUD keycaps, menus).
  const primary = (id) => label(keys(id)[0]);
  // "Q / GAUCHE"-like label of the first n keys.
  const list = (id, n) => keys(id).slice(0, n || 2).map(label).join(' / ') || '--';
  // Movement pair "Q/D ou GAUCHE/DROITE" (left/right zipped).
  function movePair() {
    const L = keys('left'), R = keys('right'), out = [];
    for (let i = 0; i < Math.min(2, L.length, R.length); i++) out.push(label(L[i]) + '/' + label(R[i]));
    return out.join(' ou ') || (primary('left') + '/' + primary('right'));
  }

  // Apply the stored preference now (before mobile.js / game.js read it).
  try { apply(SV && SV.loadPrefs ? SV.loadPrefs().controls : null); } catch (_) {}

  return { ACTIONS, RESERVED, label, fromEvent, keys, bind, clear, reset, isDefault, primary, list, movePair, apply };
})();
