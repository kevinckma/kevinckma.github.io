#!/bin/bash
# Re-sort the manuscript boxes on the encrypted research portal page in place.
# Needs: staticrypt 3.x, python3, and the portal password in $PORTAL_PASSWORD.
# Exits without changing anything if the order and stamps are already up to date.
set -euo pipefail
cd "$(dirname "$0")/.."
SALT="e2cdab35d167f01abe1b4a50ca269ef0"   # public: it is embedded in every encrypted page
PAGE=research/index.html
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
staticrypt "$PAGE" --decrypt -p "$PORTAL_PASSWORD" --salt "$SALT" -c false -d "$TMP/dec" >/dev/null
cp "$TMP/dec/index.html" "$TMP/before.html"
python3 tools/portal_order.py "$TMP/dec/index.html"
if cmp -s "$TMP/before.html" "$TMP/dec/index.html"; then echo "Portal order already up to date."; exit 0; fi
staticrypt "$TMP/dec/index.html" -p "$PORTAL_PASSWORD" --salt "$SALT" -c false --short --remember 30 \
  --template-title "Research portal" --template-instructions "This page is password protected." \
  --template-button "Open" --template-placeholder "Password" --template-remember "Remember me on this device" \
  --template-error "Incorrect password" --template-color-primary "#1f6f78" --template-color-secondary "#f8f5ef" \
  -d "$TMP/enc" >/dev/null
python3 tools/portal_style.py "$TMP/enc/index.html"
cp "$TMP/enc/index.html" "$PAGE"
echo "Portal re-sorted."
