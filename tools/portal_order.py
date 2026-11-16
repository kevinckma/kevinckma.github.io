#!/usr/bin/env python3
"""Order the manuscript boxes on the research portal, most recently updated first.

Run on the DECRYPTED portal page (research/index.html after `staticrypt --decrypt`)
every time the page is rebuilt, then re-encrypt it:

    python3 tools/portal_order.py path/to/decrypted/index.html

How it works
- Each manuscript box (<div class="res-group" id="ms-..."> inside <section id="manuscripts">)
  carries data-updated (ISO time) and data-hash (fingerprint of the box's content).
- If a box's content no longer matches its data-hash, it was edited since the last run:
  data-updated is set to now and the hash is refreshed.
- The boxes, and the thumbnails at the top of the page (<a class="ms-card" href="#ms-...">),
  are then sorted newest first. Nothing else on the page is touched.
"""
import hashlib, re, sys
from datetime import datetime
from zoneinfo import ZoneInfo

path = sys.argv[1]
html = open(path, encoding="utf-8").read()
now = datetime.now(ZoneInfo("America/Vancouver")).strftime("%Y-%m-%dT%H:%M")

sec_start = html.index('<section id="manuscripts">')
sec_end = html.index('</section>', sec_start)
section = html[sec_start:sec_end]
first = section.index('    <div class="res-group"')
head, body = section[:first], section[first:]
boxes = re.split(r'(?=    <div class="res-group")', body)
boxes = [b.rstrip() + '\n' for b in boxes if b.strip()]   # position-independent (stable hash)

ATTR = re.compile(r' data-(?:updated|hash)="[^"]*"')

def stamp(box):
    clean = ATTR.sub('', box)
    h = hashlib.sha1(clean.encode("utf-8")).hexdigest()[:12]
    old_h = re.search(r'data-hash="([^"]*)"', box)
    old_d = re.search(r'data-updated="([^"]*)"', box)
    if old_h and old_h.group(1) == h:
        date = old_d.group(1)
    elif not old_h and old_d:          # first run on a hand-dated box: keep its date
        date = old_d.group(1)
    else:
        date = now
    box = clean.replace('<div class="res-group"', f'<div class="res-group" data-updated="{date}" data-hash="{h}"', 1)
    gid = re.search(r'id="([^"]+)"', box).group(1)
    return date, gid, box

stamped = [stamp(b) for b in boxes]
stamped.sort(key=lambda t: t[0], reverse=True)
order = [gid for _, gid, _ in stamped]
new_body = ''.join(b for _, _, b in stamped)
html = html[:sec_start] + head + new_body.rstrip('\n') + '\n  ' + html[sec_end:]

# thumbnails at the top, same order
m = re.search(r'(<div class="pub-jump ms-cards">\n)(.*?)(\n\s*</div>)', html, re.S)
if m:
    cards = re.findall(r'\s*<a class="ms-card" href="#([^"]+)".*?</a>', m.group(2), re.S)
    blocks = {gid: re.search(r'[ \t]*<a class="ms-card" href="#' + re.escape(gid) + r'".*?</a>', m.group(2), re.S).group(0) for gid in cards}
    ordered = [blocks[g] for g in order if g in blocks] + [blocks[g] for g in cards if g not in order]
    html = html[:m.start(2)] + '\n'.join(ordered) + html[m.end(2):]

open(path, "w", encoding="utf-8").write(html)
print("Order:", ", ".join(f"{g} ({d})" for d, g, _ in stamped))
