#!/usr/bin/env python3
"""
Build FILE_MAP.md — a navigation index for index.html.

Run from this directory:  python3 build-index.py
Re-run after big edits so line numbers stay current.
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / 'index.html'
OUT = HERE / 'FILE_MAP.md'

text = SRC.read_text()
lines = text.split('\n')

def line_of(pos):
    return text[:pos].count('\n') + 1

# === Top-level structural landmarks ===
landmarks = []
for pat, label in [
    (r'<!DOCTYPE',          'DOCTYPE'),
    (r'<html',              '<html>'),
    (r'<head>',             '<head>'),
    (r'</head>',            '</head>'),
    (r'<style>',            '<style>'),
    (r'</style>',           '</style>'),
    (r'<body[^>]*>',        '<body>'),
    (r'<main[^>]*>',        '<main>'),
    (r'</main>',            '</main>'),
    (r'<script(?![^>]*src=)', '<script> (inline)'),
    (r'</script>',          '</script>'),
    (r'</body>',            '</body>'),
    (r'</html>',            '</html>'),
]:
    m = re.search(pat, text)
    if m:
        landmarks.append((line_of(m.start()), label))

# === HTML scenes (id="scene-*" + clean-view) ===
scenes = [(line_of(m.start()), m.group(1))
          for m in re.finditer(r'<section[^>]+id="(scene-[\w-]+|clean-view)"', text)]
scene_ranges = []
for ln, name in scenes:
    start_pos = text.find(f'id="{name}"')
    p = text.rfind('<section', 0, start_pos)
    depth = 0
    end_line = None
    while p != -1:
        p_open = text.find('<section', p+1)
        p_close = text.find('</section>', p+1)
        if p_close == -1:
            break
        if p_open != -1 and p_open < p_close:
            depth += 1
            p = p_open
        else:
            if depth == 0:
                end_line = line_of(p_close)
                break
            depth -= 1
            p = p_close
    scene_ranges.append((ln, end_line, name))

# === Top-level CSS selectors ===
style_m = re.search(r'<style>([\s\S]*?)</style>', text)
css = style_m.group(1)
style_start_line = text[:style_m.start()].count('\n') + 1
css_rules = []
depth = 0
selector_start = 0
i = 0
while i < len(css):
    ch, nx = css[i], css[i+1] if i+1 < len(css) else ''
    if ch == '/' and nx == '*':
        end = css.find('*/', i+2)
        i = (end + 2) if end != -1 else len(css)
        continue
    if depth == 0 and ch not in '{};\r\n\t ' and css[selector_start:i].strip() == '':
        selector_start = i
    if ch == '{':
        if depth == 0:
            sel = css[selector_start:i].strip().replace('\n', ' ')
            sel_line = css[:selector_start].count('\n') + 1 + style_start_line
            css_rules.append((sel_line, sel))
        depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0:
            selector_start = i + 1
    i += 1

ats = [(style_start_line + css[:m.start()].count('\n') + 1, m.group(1), m.group(2).strip())
       for m in re.finditer(r'@(media|keyframes|supports|font-face)\s+([^\{]*)\{', css)]

# === JS: functions and top-level CONSTS ===
script_m = re.search(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>', text)
js = script_m.group(1)
js_start_line = text[:script_m.start()].count('\n') + 1
js_items = []
for m in re.finditer(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(', js):
    js_items.append((js_start_line + js[:m.start()].count('\n') + 1, 'function', m.group(1)))
for m in re.finditer(r'^\s*(const|let|var)\s+([A-Z_][A-Z0-9_]+)\s*=', js, re.M):
    js_items.append((js_start_line + js[:m.start()].count('\n') + 1, m.group(1).upper()+'_CONST', m.group(2)))
for m in re.finditer(r'^\s*const\s+([a-z_$][\w$]*)\s*=\s*(?:\([^)]*\)|[a-z_$][\w$]*)\s*=>', js, re.M):
    js_items.append((js_start_line + js[:m.start()].count('\n') + 1, 'arrow', m.group(1)))

# === Topical landmarks (curated, high-traffic edit targets) ===
keymarks = []
KEY_PATTERNS = [
    (r'<!-- SCENE 0: WORLD MAP',     'comment: SCENE 0 WORLD MAP'),
    (r'<!-- SCENE 1: ARCHIVES',      'comment: SCENE 1 ARCHIVES'),
    (r'<!-- SCENE 2: QUEST BOARD',   'comment: SCENE 2 QUEST BOARD'),
    (r'<!-- SCENE 3: INVENTORY',     'comment: SCENE 3 INVENTORY/SHOP'),
    (r'<!-- SCENE 4: TROPHY',        'comment: SCENE 4 TROPHY'),
    (r'<!-- SCENE 5: TAVERN',        'comment: SCENE 5 TAVERN'),
    (r'<!-- CLEAN VIEW',             'comment: CLEAN VIEW'),
    (r'data-coin="1"',                'coin #1 (world map)'),
    (r'data-coin="2"',                'coin #2 (archives)'),
    (r'data-coin="3"',                'coin #3 (quest-board)'),
    (r'data-coin="4"',                'coin #4 (shop)'),
    (r'data-coin="5"',                'coin #5 (trophy)'),
    (r'data-caffeine="1"',            'caffeine #1 (archives, tea)'),
    (r'data-caffeine="2"',            'caffeine #2 (quest-board, coffee)'),
    (r'data-caffeine="3"',            'caffeine #3 (shop, coffee)'),
    (r'data-caffeine="4"',            'caffeine #4 (trophy, tea)'),
    (r'data-caffeine="5"',            'caffeine #5 (tavern, coffee)'),
    (r'id="heroSprite"',              'heroSprite SVG (archives)'),
    (r'class="player-card-sprite"',   'PLAYER card avatar SVG'),
    (r'id="mapAvatar"',               'mapAvatar SVG (overworld)'),
    (r'id="mpCaffeineBar"',           'MP bar (caffeine sync)'),
    (r'id="caffeineCount"',           'topbar caffeine label'),
    (r'id="coinCount"',                'topbar coin label'),
    (r'function triggerPowerup',      'JS triggerPowerup()'),
    (r'function setPowered',           'JS setPowered()'),
    (r'function updateCaffeine',       'JS updateCaffeine()'),
    (r'function readView',             'JS readView()'),
    (r'function readTheme',            'JS readTheme()'),
    (r"const KONAMI",                  'JS KONAMI const'),
    (r'CAFF_KEY',                      'JS CAFF_KEY const'),
    (r'POWER_KEY',                     'JS POWER_KEY const'),
    (r'class="caffeine"',              'topbar .caffeine span'),
    (r'class="coins"',                 'topbar .coins span'),
    (r'class="topbar"',                '.topbar element'),
    (r'class="hint-strip"',            '.hint-strip element'),
    (r'id="miniterm"',                 'miniterm overlay'),
    (r'id="cs2-overlay"|class="cs2-overlay"', 'CS2 konami overlay'),
    (r'class="loadout-card"',          '.loadout-card (LANGUAGES/etc)'),
    (r'class="trophy-banner"',         '.trophy-banner block'),
    (r'class="quest-entry"',           'quest-entry blocks (jobs)'),
    (r'class="cv-job"',                'clean-view .cv-job blocks'),
    (r'class="cv-proj"',               'clean-view .cv-proj blocks'),
    (r'<aside class="panel"',          'right-side panel (player card region)'),
    (r'body\.light-theme\s*\{',         'CSS: body.light-theme overrides'),
    (r'body\.powered-up',              'CSS: body.powered-up rules'),
    (r'@media \(prefers-reduced-motion','CSS: prefers-reduced-motion'),
    (r'<a[^>]+href="mailto:',          'mailto link'),
]
for pat, label in KEY_PATTERNS:
    for m in re.finditer(pat, text):
        keymarks.append((line_of(m.start()), label))

# === Render ===
out = []
out.append("# index.html — navigation map\n")
out.append("Auto-generated by `build-index.py`. Regenerate after big edits.\n")
out.append(f"\n_Total lines: **{len(lines)}**_\n")

out.append("\n## Top-level structure\n")
out.append("| Line | Landmark |")
out.append("|---:|:---|")
for ln, label in landmarks:
    out.append(f"| {ln} | {label} |")

out.append("\n## HTML scenes\n")
out.append("| Lines | Scene id |")
out.append("|:---|:---|")
for s, e, name in scene_ranges:
    out.append(f"| {s}–{e} | `{name}` |")

out.append("\n## Topical landmarks (high-traffic edit targets)\n")
out.append("| Line | Landmark |")
out.append("|---:|:---|")
seen = set()
for ln, label in sorted(keymarks):
    key = (ln, label)
    if key in seen: continue
    seen.add(key)
    out.append(f"| {ln} | {label} |")

out.append("\n## CSS — top-level rules\n")
out.append("| Line | Selector |")
out.append("|---:|:---|")
for ln, sel in css_rules:
    sel_show = sel if len(sel) < 110 else sel[:107] + '…'
    out.append(f"| {ln} | `{sel_show}` |")

out.append("\n## CSS — @media / @keyframes / @font-face\n")
out.append("| Line | Kind | Detail |")
out.append("|---:|:---|:---|")
for ln, kind, detail in ats:
    d = detail if len(detail) < 90 else detail[:87] + '…'
    out.append(f"| {ln} | @{kind} | `{d}` |")

out.append("\n## JS — functions & top-level constants\n")
out.append("| Line | Kind | Name |")
out.append("|---:|:---|:---|")
for ln, kind, name in sorted(set(js_items)):
    out.append(f"| {ln} | {kind} | `{name}` |")

OUT.write_text('\n'.join(out) + '\n')
print(f"Wrote {OUT.name}  ({len(out)} lines)  ·  source = {len(lines)} lines")
