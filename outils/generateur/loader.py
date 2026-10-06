"""Écran de chargement : le logo est « imprimé » en deux passes de raclette, comme en sérigraphie
(une passe bleue, puis la couleur finale posée dessus, légèrement décalée), puis l'écran se lève.
Montré une seule fois par visite (sessionStorage). Sans JavaScript, il n'apparaît pas."""
# à ajouter au script du <head> : décide si l'écran se montre
HEAD='try{if(!sessionStorage.getItem("em-ld")){sessionStorage.setItem("em-ld","1");document.documentElement.classList.add("ld")}}catch(e){}'
CSS='''
#ld{display:none}
html.ld #ld{--w:min(88vw,150vh);--ink:#f4f4f2;display:grid;place-items:center;position:fixed;inset:0;z-index:2147483000;background:#050505;animation:ldsafe 0s 7s forwards}
html.ld[data-theme=light] #ld{--ink:#0a0a0a;background:#efefec}
#ld:after{content:"";position:absolute;left:0;right:0;top:100%;height:3.2vh;background:#0a3cff}
.ld-s{position:relative;width:var(--w);aspect-ratio:1600/747}
.ld-p{position:absolute;left:0;top:0;height:100%;width:0;animation:ldp .62s cubic-bezier(.62,0,.25,1) forwards}
.ld-p>span{position:absolute;inset:0;overflow:hidden}.ld-p svg{display:block;width:var(--w);height:100%}
.ld-p>i{position:absolute;right:0;top:-100vh;bottom:-100vh;width:max(14px,2.2vw);transform:translateX(50%) scaleY(0);animation:ldq .86s cubic-bezier(.62,0,.25,1) forwards}
.ld-1{color:#0a3cff;transform:translate(1.2%,2.6%);animation-delay:.18s}.ld-1>i{background:#0a3cff;animation-delay:.1s}
.ld-2{color:var(--ink);animation-delay:.7s}.ld-2>i{background:var(--ink);animation-delay:.62s}
html.ld-out #ld{transform:translateY(calc(-100% - 3.2vh));transition:transform .72s cubic-bezier(.7,0,.2,1)}
@keyframes ldp{to{width:100%}}
@keyframes ldq{0%{transform:translateX(50%) scaleY(0)}10%{transform:translateX(50%) scaleY(1)}82%{transform:translateX(50%) scaleY(1);opacity:1}100%{transform:translateX(60vw) scaleY(1);opacity:0}}
@keyframes ldsafe{to{visibility:hidden}}
@media (orientation:portrait){html.ld #ld{--w:95vw}.ld-1{transform:translate(1.6%,3.4%)}}
@media (prefers-reduced-motion:reduce){.ld-p{width:100%;animation:none}.ld-p>i{display:none}html.ld-out #ld{transform:none;opacity:0;transition:opacity .25s}}
'''
def html(vb):
    lay=lambda n:f'<div class="ld-p ld-{n}"><span><svg viewBox="{vb}"><use href="#emlogo"/></svg></span><i></i></div>'
    js=("(function(){var d=document.documentElement,el=document.getElementById('ld');if(!el||!d.classList.contains('ld'))return;var t0=Date.now(),go=0;"
        "function out(){if(go)return;go=1;setTimeout(function(){d.classList.add('ld-out');setTimeout(function(){el.remove();d.classList.remove('ld','ld-out')},800)},Math.max(0,1550-(Date.now()-t0)))}"
        "if(document.readyState==='complete')out();else addEventListener('load',out);setTimeout(out,3600)})()")
    return f'<div id="ld" aria-hidden="true"><div class="ld-s">{lay(1)}{lay(2)}</div></div><script>{js}</script>'
