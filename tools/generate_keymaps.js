#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { charToHid, loadKeyboard, extractLayers, getAvailableLayouts } = require('worldalphabets');

const HID_HEX_TO_RELAYKEYS = {
  '0x04': 'A', '0x05': 'B', '0x06': 'C', '0x07': 'D', '0x08': 'E',
  '0x09': 'F', '0x0A': 'G', '0x0B': 'H', '0x0C': 'I', '0x0D': 'J',
  '0x0E': 'K', '0x0F': 'L', '0x10': 'M', '0x11': 'N', '0x12': 'O',
  '0x13': 'P', '0x14': 'Q', '0x15': 'R', '0x16': 'S', '0x17': 'T',
  '0x18': 'U', '0x19': 'V', '0x1A': 'W', '0x1B': 'X', '0x1C': 'Y',
  '0x1D': 'Z',
  '0x1E': '1', '0x1F': '2', '0x20': '3', '0x21': '4', '0x22': '5',
  '0x23': '6', '0x24': '7', '0x25': '8', '0x26': '9', '0x27': '0',
  '0x2D': 'MINUS', '0x2E': 'EQUALS',
  '0x2F': 'LEFTBRACKET', '0x30': 'RIGHTBRACKET',
  '0x31': 'BACKSLASH', '0x33': 'SEMICOLON',
  '0x34': 'QUOTE', '0x35': 'BACKQUOTE',
  '0x36': 'COMMA', '0x37': 'PERIOD', '0x38': 'SLASH',
  '0x2C': 'SPACE',
  '0x64': 'BACKSLASH',
};

const WA_MOD_TO_RELAYKEYS = {
  'ShiftLeft': 'LSHIFT', 'ShiftRight': 'RSHIFT',
  'AltLeft': 'LALT', 'AltRight': 'RALT',
  'ControlLeft': 'LCTRL', 'ControlRight': 'RCTRL',
  'MetaLeft': 'LMETA', 'MetaRight': 'RMETA',
};

const LAYOUT_MAP = {
  'us': 'en-us',
  'uk': 'en-united-kingdom',
  'de': 'de-german',
  'fr_azerty': 'fr-french-standard-azerty',
  'es_qwerty': 'es-spanish',
  'it_qwerty': 'it-italian',
};

async function generateKeymap(layoutName, waLayoutId) {
  console.log(`Generating ${layoutName} from ${waLayoutId}...`);

  const keymap = {};
  keymap['\r'] = [null, null];
  keymap['\t'] = ['TAB', []];
  keymap[' '] = ['SPACE', []];
  keymap['\n'] = ['ENTER', []];

  // Collect all unique characters from all keyboard layers
  const kb = await loadKeyboard(waLayoutId);
  const layers = extractLayers(kb, ['base', 'shift', 'altgr', 'shift_altgr']);
  const chars = new Set();
  for (const layer of Object.values(layers)) {
    for (const v of Object.values(layer)) {
      if (v && typeof v === 'string' && v.length === 1) chars.add(v);
    }
  }

  // Use charToHid for each character to get proper HID code + modifiers
  let hits = 0;
  let misses = 0;
  for (const ch of chars) {
    if (keymap[ch]) continue;
    try {
      const results = await charToHid(ch, waLayoutId);
      if (results && results.length > 0) {
        const r = results[0];
        const rkKey = HID_HEX_TO_RELAYKEYS[r.hid];
        if (rkKey) {
          const mods = (r.modifiers || []).map(m => WA_MOD_TO_RELAYKEYS[m]).filter(Boolean);
          keymap[ch] = [rkKey, mods];
          hits++;
          continue;
        }
      }
    } catch (_) {}
    misses++;
  }

  // Sort keys for readability
  const sorted = {};
  const keys = Object.keys(keymap).sort((a, b) => {
    const specialA = ['\r', '\t', '\n', ' '].includes(a);
    const specialB = ['\r', '\t', '\n', ' '].includes(b);
    if (specialA && !specialB) return -1;
    if (!specialA && specialB) return 1;
    return a.localeCompare(b);
  });
  for (const k of keys) {
    sorted[k] = keymap[k];
  }

  const outDir = path.join(__dirname, '..', 'keymaps');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const outFile = path.join(outDir, `${layoutName}_keymap.json`);
  fs.writeFileSync(outFile, JSON.stringify(sorted, null, 4) + '\n');

  const charCount = Object.keys(keymap).filter(k => k !== '\r').length;
  console.log(`  Wrote ${outFile} (${charCount} chars, ${hits} mapped, ${misses} unmatched)`);
  return true;
}

async function main() {
  const args = process.argv.slice(2);

  if (args[0] === '--list') {
    const layouts = await getAvailableLayouts();
    console.log('Available layouts:');
    layouts.forEach(l => console.log(`  ${l}`));
    return;
  }

  if (args[0] === '--all') {
    const layouts = await getAvailableLayouts();
    console.log(`Found ${layouts.length} layouts. Generating all...\n`);
    let count = 0;
    for (const waId of layouts) {
      const name = waId.replace(/[^a-zA-Z0-9]/g, '_');
      const ok = await generateKeymap(name, waId);
      if (ok) count++;
    }
    console.log(`\nGenerated ${count} keymaps.`);
    return;
  }

  console.log('Generating standard RelayKeys keymaps...\n');
  for (const [name, waId] of Object.entries(LAYOUT_MAP)) {
    await generateKeymap(name, waId);
  }
  console.log('\nDone.');
}

main().catch(e => { console.error(e); process.exit(1); });
