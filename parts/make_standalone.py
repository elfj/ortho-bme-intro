# -*- coding: utf-8 -*-
"""Build deck-standalone.html: deck.html with every local image inlined as a data URI (single file to share)."""
import base64, io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = io.open(os.path.join(ROOT, "deck.html"), encoding="utf-8").read()

def inline(m):
    path = os.path.join(ROOT, m.group(1))
    mime = "image/png" if path.endswith(".png") else "image/jpeg"
    data = base64.b64encode(open(path, "rb").read()).decode("ascii")
    return 'src="data:%s;base64,%s"' % (mime, data)

s, n = re.subn(r'src="((?:wtmh-design-kit|deck-assets)/[^"]+)"', inline, s)
io.open(os.path.join(ROOT, "deck-standalone.html"), "w", encoding="utf-8", newline="\n").write(s)
print("inlined images:", n, "bytes:", len(s.encode("utf-8")))
