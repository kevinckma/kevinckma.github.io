# Research portal tools

## Manuscript order (newest first) — automatic

The manuscript boxes on the research portal, and the thumbnails at the top of the
page, are ordered so the box changed most recently comes first.

This happens automatically: whenever `research/index.html` is pushed to GitHub,
the "Sort research portal manuscripts" workflow (`.github/workflows/portal-order.yml`)
decrypts the page, runs `tools/portal_order.py`, re-encrypts it and commits the
result. It needs the portal password saved as the repository secret `PORTAL_PASSWORD`.

To do the same by hand: `PORTAL_PASSWORD=... tools/portal_rebuild.sh`

- `portal_order.py`: stamps any box whose content changed with the current time and sorts the boxes
- `portal_rebuild.sh`: decrypt, sort, re-encrypt (same salt and template), re-apply styling
- `portal_style.py`: login-page styling applied after encryption

No passwords are stored in this folder.

## Shared site.css / site.js

Every page (main site, the two portal pages (Manuscripts, Resources) and their login pages) loads `/site.css` and `/site.js`.
They provide the light/dark theme (light by default; dark only after a visitor clicks the nav button,
then remembered in localStorage across all pages), the "Skip to content" link, and keyboard
access to enlargeable images and their popups. `portal_style.py` adds the two tags to login pages;
keep them in the `<head>` of any new page.
