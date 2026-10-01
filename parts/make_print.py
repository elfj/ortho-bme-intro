# -*- coding: utf-8 -*-
"""Build deck-print.html: strip presenter block, inject @page print CSS."""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = io.open(os.path.join(ROOT, "deck.html"), encoding="utf-8").read()
s = re.sub(r"<!--PRESENTER-START-->.*?<!--PRESENTER-END-->", "", s, flags=re.S)
print_css = """<style>
@page{ size:1280px 720px; margin:0 }
@media print{
  body{ padding:0 !important; background:#fff !important }
  .deck{ gap:0 !important; margin:0 !important }
  .slide{ page-break-after:always; box-shadow:none !important; border-radius:0 !important }
}
</style></head>"""
s = s.replace("</head>", print_css, 1)
io.open(os.path.join(ROOT, "deck-print.html"), "w", encoding="utf-8", newline="\n").write(s)
print("deck-print.html written (presenter stripped)")
