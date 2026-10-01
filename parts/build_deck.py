# -*- coding: utf-8 -*-
"""Assemble deck.html: template head CSS + 32 authored sections + footer macro expansion."""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "wtmh-design-kit", "template.html")
OUT = os.path.join(ROOT, "deck.html")

src = io.open(TPL, encoding="utf-8").read()
head = src[: src.index('<div class="deck">') + len('<div class="deck">')]
head = re.sub(r"<title>.*?</title>",
              "<title>深度學習及生成式 AI 於骨科學的應用｜醫學工程概論 2026-10-01</title>",
              head, count=1, flags=re.S)
# strip legacy VRMT-deck "#sN ..." rules from the template CSS: they target fixed slide
# numbers of the original deck and would silently restyle whatever page lands on that id
head, n_legacy = re.subn(r"^[ \t]*#s\d+[^{]*\{[^}]*\}[ \t]*\n", "", head, flags=re.M)

FOOTER = '''  <footer class="footer-ribbon">
    <div class="fl-left">
      <img class="ncku-logo" src="wtmh-design-kit/assets/brand/logo-ncku-h-small.png" alt="NCKU" />
      <img class="wtmh-logo" src="wtmh-design-kit/assets/brand/logo-wtmh-new-small.png" alt="WTMH Lab" />
    </div>
    <div class="ribbon-bar">
      <span class="lab-name">NCKU BME WTMH Lab</span>
      <span class="pageno">{n}</span>
    </div>
  </footer>'''

body = []
for part in ["sections-a.html", "sections-b.html", "sections-c.html", "sections-d.html"]:
    body.append(io.open(os.path.join(ROOT, "parts", part), encoding="utf-8").read())
body = "\n".join(body)

# auto-renumber: section ids become s1..sN in document order; each footer macro
# takes its enclosing section's number, so inserting/removing pages never breaks numbering
tokens = re.split(r'(<section class="slide[^"]*" id="s\d+"[^>]*>|<!--F:\d+-->)', body)
n = 0
out = []
for t in tokens:
    m = re.match(r'<section class="slide([^"]*)" id="s\d+"([^>]*)>$', t)
    if m:
        n += 1
        out.append(f'<section class="slide{m.group(1)}" id="s{n}"{m.group(2)}>')
    elif t.startswith("<!--F:"):
        out.append(FOOTER.format(n=n))
    else:
        out.append(t)
body = "".join(out)

PRESENTER = '''
<!--PRESENTER-START-->
<style>
body.present{padding:0;background:#111;overflow:hidden}
body.present .slide{display:none;position:fixed;top:50%;left:50%;margin:0;border-radius:0;box-shadow:none}
body.present .slide.pactive{display:block}
#phud{position:fixed;right:14px;bottom:10px;z-index:99;font:600 12px Inter,sans-serif;color:#fff;background:rgba(0,0,0,.45);padding:4px 10px;border-radius:12px;display:none}
body.present #phud{display:block}
#phint{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:99;font:500 12.5px Inter,'Noto Sans TC',sans-serif;color:#fff;background:rgba(0,0,0,.6);padding:6px 16px;border-radius:14px;display:none;white-space:nowrap}
/* in-slide build steps: hidden in presenter mode until reached; always visible in scroll/print */
body.present .bstep{opacity:0;transition:opacity .25s}
body.present .bstep.on{opacity:1}
</style>
<div id="phud"></div><div id="phint">&larr; &rarr; 換頁／分段 &middot; F 全螢幕 &middot; Esc 捲動總覽 &middot; P 回播放</div>
<script>
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var n=slides.length, i=0, present=!/[?&]scroll/.test(location.search);
  function fit(){var s=Math.min(innerWidth/1280,innerHeight/720);slides.forEach(function(el){el.style.transform='translate(-50%,-50%) scale('+s+')';});}
  var step=0;
  function steps(el){return el.querySelectorAll('.bstep').length?Math.max.apply(null,[].map.call(el.querySelectorAll('.bstep'),function(b){return +b.dataset.step||1;})):(+el.dataset.steps||0);}
  function applyStep(el){el.querySelectorAll('.bstep').forEach(function(b){b.classList.toggle('on',(+b.dataset.step||1)<=step);});var hk=el.dataset.hook;if(hk&&window.slideHooks&&window.slideHooks[hk])window.slideHooks[hk](step,el);}
  function show(k,last){i=Math.max(0,Math.min(n-1,k));step=last?steps(slides[i]):0;slides.forEach(function(el,j){el.classList.toggle('pactive',j===i);});applyStep(slides[i]);var h=document.getElementById('phud');if(h)h.textContent=(i+1)+' / '+n;try{history.replaceState(null,'','#'+(i+1));}catch(e){}}
  function next(){if(step<steps(slides[i])){step++;applyStep(slides[i]);}else show(i+1);}
  function prev(){if(step>0){step--;applyStep(slides[i]);}else show(i-1,true);}
  function enter(){document.body.classList.add('present');fit();show(i);hint();}
  function exit(){document.body.classList.remove('present');slides.forEach(function(el){el.classList.remove('pactive');el.style.transform='';});slides[i].scrollIntoView({block:'start'});}
  var ht;function hint(){var h=document.getElementById('phint');if(!h)return;h.style.display='block';clearTimeout(ht);ht=setTimeout(function(){h.style.display='none';},4500);}
  addEventListener('resize',function(){if(document.body.classList.contains('present'))fit();});
  addEventListener('keydown',function(e){
    var p=document.body.classList.contains('present');
    if(e.key==='Escape'&&p){exit();return;}
    if((e.key==='p'||e.key==='P')&&!p){enter();return;}
    if(!p)return;
    if(e.target.closest('input'))return;
    if(e.key==='ArrowRight'||e.key==='ArrowDown'||e.key===' '||e.key==='PageDown'){e.preventDefault();next();}
    else if(e.key==='ArrowLeft'||e.key==='ArrowUp'||e.key==='PageUp'){e.preventDefault();prev();}
    else if(e.key==='Home'){show(0);}
    else if(e.key==='End'){show(n-1);}
    else if(e.key==='f'||e.key==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();}
  });
  addEventListener('click',function(e){
    if(!document.body.classList.contains('present'))return;
    if(e.target.closest('a,input,button,[data-ui]'))return;
    if(e.clientX<innerWidth*0.25)prev();else next();
  });
  var m=location.hash.match(/^#(\\d+)$/); if(m)i=Math.min(n-1,Math.max(0,parseInt(m[1],10)-1));
  if(present)enter();else slides.forEach(function(el){var hk=el.dataset.hook;if(hk&&window.slideHooks&&window.slideHooks[hk])window.slideHooks[hk](0,el);});
})();
</script>
<!--PRESENTER-END-->
'''

WIDGETS = io.open(os.path.join(ROOT, "parts", "widgets.html"), encoding="utf-8").read() if os.path.exists(os.path.join(ROOT, "parts", "widgets.html")) else ""
out = head + "\n\n" + body + "\n</div>\n" + WIDGETS + PRESENTER + "</body>\n</html>\n"
io.open(OUT, "w", encoding="utf-8", newline="\n").write(out)

# integrity checks
ids = re.findall(r'<section class="slide[^"]*" id="s(\d+)"[^>]*>', body)
pagenos = re.findall(r'<span class="pageno">(\d+)</span>', body)
print("sections:", len(ids), "ids sequential:", ids == [str(i) for i in range(1, len(ids) + 1)])
print("pagenos:", pagenos)
print("leftover macros:", out.count("<!--F:"))
print("legacy #sN rules stripped:", n_legacy)
print("bytes:", len(out.encode("utf-8")))
