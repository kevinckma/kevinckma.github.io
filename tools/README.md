# Research portal tools

## Manuscript order (newest first)

The manuscript boxes on the research portal, and the thumbnails at the top of
the page, are ordered automatically: the box changed most recently comes first.

After any edit to the portal page:

1. Decrypt it (run from a folder whose `.staticrypt.json` holds the portal's salt):
   `staticrypt research/index.html --decrypt -p "$PASSWORD" -d /tmp/portal`
2. Make the edit in `/tmp/portal/index.html`.
3. `python3 tools/portal_order.py /tmp/portal/index.html`
   (stamps any changed box with the current time and re-sorts the boxes)
4. Re-encrypt with the same salt and the usual template options, re-apply the
   login-page styling, and copy the result back to `research/index.html`.

The script only reads and writes the decrypted page; it holds no passwords.
