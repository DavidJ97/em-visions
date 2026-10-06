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
    # Petit tintement métallique très fin au passage de la première raclette. Il est fabriqué par le navigateur (aucun fichier).
    # Les navigateurs bloquent le son tant que le visiteur n'a pas touché la page : s'il est bloqué, on ne joue rien.
    ting=("function ting(){try{var A=window.AudioContext||window.webkitAudioContext;if(!A)return;var c=new A();if(c.state!=='running'){c.close&&c.close();return}"
          "var t=c.currentTime+.02,m=c.createGain();m.gain.value=.05;m.connect(c.destination);"
          "[[3140,.9,1],[4770,.6,.55],[6390,.42,.34],[8960,.26,.2],[11800,.16,.1]].forEach(function(p){var o=c.createOscillator(),g=c.createGain();o.type='sine';o.frequency.value=p[0];"
          "g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(p[2],t+.004);g.gain.exponentialRampToValueAtTime(.0001,t+p[1]);o.connect(g);g.connect(m);o.start(t);o.stop(t+p[1]+.05)});"
          "setTimeout(function(){c.close&&c.close()},1400)}catch(e){}}")
    js=("(function(){var d=document.documentElement,el=document.getElementById('ld');if(!el||!d.classList.contains('ld'))return;var t0=Date.now(),go=0;"
        +ting+"setTimeout(ting,160);"
        "function out(){if(go)return;go=1;setTimeout(function(){d.classList.add('ld-out');setTimeout(function(){el.remove();d.classList.remove('ld','ld-out')},800)},Math.max(0,1550-(Date.now()-t0)))}"
        "if(document.readyState==='complete')out();else addEventListener('load',out);setTimeout(out,3600)})()")
    return f'<div id="ld" aria-hidden="true"><div class="ld-s">{lay(1)}{lay(2)}</div></div><script>{js}</script>'
