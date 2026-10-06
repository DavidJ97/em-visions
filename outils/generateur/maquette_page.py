"""Page du modélisateur 3D : site/maquette/ (français) et site/en/mockup/ (anglais)."""
import html as H, os, shutil
from config import SITE_URL
T={'fr':{'path':'/maquette/','up':'../','app':'app.js','title':'Maquette 3D','h1':'Créez votre maquette','back':'Retour au site','other':('EN','../en/mockup/'),'home':'../','to':'../#contact',
  'desc':'Choisissez un produit parmi vingt, posez votre image, faites-le pivoter en 3D et joignez la maquette à votre demande de devis.',
  'lead':'Choisissez un produit, posez votre image, faites-le pivoter, puis joignez la maquette à votre demande de devis.',
  's1':'Produit','s2':'Couleur','s3':'Votre image','pick':'Choisir une image','fmt':'PNG, JPG ou SVG, 12 Mo max.','size':'Taille','x':'Horizontal','y':'Vertical','rot':'Rotation','rm':'Retirer l’image',
  'send':'Joindre à ma demande de devis','note':'Aperçu indicatif : les couleurs, les formats et l’emplacement exacts sont confirmés avec le devis. Votre image reste sur votre appareil tant que vous n’envoyez pas la demande.',
  'hint':'Glissez pour faire pivoter','view':'Aperçu 3D du produit'},
 'en':{'path':'/en/mockup/','up':'../../','app':'../../maquette/app.js','title':'3D mockup','h1':'Build your mockup','back':'Back to the site','other':('FR','../../maquette/'),'home':'../','to':'../#contact',
  'desc':'Pick one of twenty products, place your image, rotate it in 3D and attach the mockup to your quote request.',
  'lead':'Pick a product, place your image, rotate it, then attach the mockup to your quote request.',
  's1':'Product','s2':'Colour','s3':'Your image','pick':'Choose an image','fmt':'PNG, JPG or SVG, 12 MB max.','size':'Size','x':'Horizontal','y':'Vertical','rot':'Rotation','rm':'Remove image',
  'send':'Attach to my quote request','note':'Indicative preview: exact colours, sizes and placement are confirmed with the quote. Your image stays on your device until you send the request.',
  'hint':'Drag to rotate','view':'3D preview of the product'}}
CSS='''*{box-sizing:border-box;margin:0;padding:0}:root{--bg:#0a0a0a;--fg:#f4f4f2;--mut:#a9a9a6;--line:#2a2a2c;--card:#1c1d21;--blue:#0a3cff;--stage1:#3b3f4a;--stage2:#0e0f12}
html[data-theme=light]{--bg:#efefec;--fg:#141414;--mut:#555;--line:#cfcfcb;--card:#e4e4e0;--stage1:#fbfbf9;--stage2:#d9d9d4}
html,body{height:100%}body{background:var(--bg);color:var(--fg);font:400 16px/1.5 'Kumbh Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--fg)}button{font:inherit;color:inherit;cursor:pointer}:focus-visible{outline:3px solid #6f8cff;outline-offset:2px}
header{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:10px 24px;height:76px}
.logo{display:block;width:128px;height:60px;color:var(--fg)}.logo svg{width:100%;height:100%;display:block}
nav{display:flex;gap:22px;align-items:center;font-weight:600;font-size:15px}
.wrap{display:grid;grid-template-columns:minmax(0,1fr) 452px;height:calc(100vh - 76px);min-height:560px}
.stagebox{position:relative;background:radial-gradient(120% 90% at 50% 38%,var(--stage1),var(--stage2));overflow:hidden;border-top:1px solid var(--line)}
#view{position:absolute;inset:0;width:100%;height:100%;display:block;cursor:grab;touch-action:pan-y;outline-offset:-4px}#view.grab{cursor:grabbing}
.cap{position:absolute;left:24px;bottom:20px;right:24px;display:flex;justify-content:space-between;align-items:flex-end;gap:12px;pointer-events:none}
.cap b{font:700 clamp(20px,2.4vw,30px)/1.05 Oswald,sans-serif;text-transform:uppercase;letter-spacing:.02em}.cap b small{display:block;font:400 14px/1.4 'Kumbh Sans';text-transform:none;color:var(--mut);letter-spacing:0;margin-top:4px}
.cap i{font-style:normal;font-size:13px;color:var(--mut);display:flex;gap:8px;align-items:center;white-space:nowrap}
.panel{overflow:auto;padding:26px 26px 40px;border-left:1px solid var(--line);border-top:1px solid var(--line)}
h1{font:400 clamp(22px,2.3vw,30px)/1.14 Sekuya,'Kumbh Sans',sans-serif;text-transform:uppercase;letter-spacing:.05em}h1:after{content:"";display:block;width:60px;height:5px;background:var(--blue);margin-top:16px}
.lead{color:var(--mut);margin-top:14px;font-size:15.5px}
h2{display:flex;align-items:center;gap:12px;font:700 17px/1 Oswald,sans-serif;text-transform:uppercase;letter-spacing:.04em;margin:30px 0 12px}h2 b{color:#4d74ff;font-size:22px}h2 span{margin-left:auto;font:400 13.5px 'Kumbh Sans';text-transform:none;letter-spacing:0;color:var(--mut)}
.prods{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.prod{background:var(--card);border:2px solid transparent;border-radius:10px;padding:6px 4px 8px;display:flex;flex-direction:column;align-items:center;gap:2px;min-width:0}
.prod img{width:100%;max-width:84px;aspect-ratio:1;height:auto;display:block}.prod span{font-size:11.5px;line-height:1.2;text-align:center;color:var(--mut);overflow-wrap:anywhere}
.prod[aria-pressed=true]{border-color:var(--blue)}.prod[aria-pressed=true] span{color:var(--fg)}.prod:hover{border-color:#4d74ff66}.prod[aria-pressed=true]:hover{border-color:var(--blue)}
.cols{display:flex;flex-wrap:wrap;gap:10px}.sw{width:38px;height:38px;border-radius:50%;border:2px solid var(--line);box-shadow:inset 0 0 0 2px var(--bg)}.sw[aria-pressed=true]{border-color:var(--blue);box-shadow:inset 0 0 0 3px var(--bg)}
.tabs{display:flex;gap:8px;margin-bottom:12px}.tabs[hidden]{display:none}.tabs button{flex:1;background:var(--card);border:2px solid transparent;border-radius:8px;padding:9px 10px;font-weight:600;font-size:14.5px}.tabs button[aria-pressed=true]{border-color:var(--blue)}
.up{display:flex;align-items:center;gap:14px;border:2px dashed var(--line);border-radius:10px;padding:14px 16px;cursor:pointer}.up:hover{border-color:#4d74ff}.up input{position:absolute;opacity:0;width:1px;height:1px}.up:focus-within{outline:3px solid #6f8cff;outline-offset:2px}
.up svg{flex:none;color:#4d74ff}.up b{display:block;font-weight:600;overflow-wrap:anywhere}.up small{color:var(--mut);font-size:13px}
#adj{margin-top:14px;display:grid;gap:10px}#adj[hidden]{display:none}.sl{display:grid;grid-template-columns:92px 1fr;align-items:center;gap:12px;font-size:14px}.sl input{width:100%;accent-color:#3d68ff;height:28px}
.rm{justify-self:start;background:none;border:0;text-decoration:underline;text-underline-offset:3px;color:var(--mut);font-size:14px;padding:6px 0}
.cta{margin-top:30px;width:100%;background:var(--blue);color:#fff;border:0;border-radius:6px;padding:17px 18px;font:600 17px 'Kumbh Sans',sans-serif;display:flex;justify-content:center;gap:12px;align-items:center}.cta:hover{background:#2a55ff}.cta:disabled{opacity:.6}
.note{color:var(--mut);font-size:13px;margin-top:14px}
.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(20px);background:var(--blue);color:#fff;font:500 15px 'Kumbh Sans',sans-serif;padding:12px 20px;border-radius:6px;opacity:0;transition:.3s;z-index:9;pointer-events:none;max-width:90vw;text-align:center}.toast.on{opacity:1;transform:translateX(-50%)}
@media (max-width:900px){html,body{height:auto}header{padding:8px 16px;height:64px}.logo{width:104px;height:48px}.wrap{display:block;height:auto}
 .stagebox{position:sticky;top:0;height:44vh;min-height:280px;z-index:2;border-bottom:1px solid var(--line)}.cap{left:16px;right:16px;bottom:12px}.cap i{display:none}
 .panel{border-left:0;border-top:0;padding:22px 16px 48px;overflow:visible}.prods{grid-template-columns:repeat(4,1fr);gap:6px}}'''
HEADJS='(function(){let t;try{t=localStorage.getItem("em-theme")}catch(e){}if(t!=="light"&&t!=="dark")t=matchMedia("(prefers-color-scheme: light)").matches?"light":"dark";document.documentElement.dataset.theme=t})()'
FONTS=(('Sekuya',400,'sekuya-latin-400'),('Kumbh Sans',400,'kumbh-sans-latin-400'),('Kumbh Sans',600,'kumbh-sans-latin-600'),('Oswald',700,'oswald-latin-700'))
def page(L,logo_vb,logo_d):
    t=T[L]; e=H.escape; up=t['up']
    ff=''.join(f"@font-face{{font-family:'{n}';font-weight:{w};font-display:swap;src:url({up}fonts/{f}-normal.woff2) format('woff2')}}" for n,w,f in FONTS)
    sl=lambda k,lab,mn,mx,st,v:f'<label class="sl"><span>{e(lab)}</span><input type="range" id="s-{k}" min="{mn}" max="{mx}" step="{st}" value="{v}"></label>'
    return (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(t["title"])} — EM Visions</title>'
      f'<meta name="description" content="{e(t["desc"])}"><link rel="canonical" href="{SITE_URL}{t["path"]}">'
      f'<link rel="alternate" hreflang="fr-CA" href="{SITE_URL}/maquette/"><link rel="alternate" hreflang="en-CA" href="{SITE_URL}/en/mockup/">'
      f'<meta property="og:title" content="{e(t["title"])} — EM Visions"><meta property="og:description" content="{e(t["desc"])}"><meta property="og:image" content="{SITE_URL}/img/og.jpg">'
      f'<link rel="icon" href="{up}img/favicon.svg" type="image/svg+xml"><link rel="icon" href="{up}img/favicon-32.png" sizes="32x32" type="image/png"><meta name="theme-color" content="#0a0a0a">'
      f'<link rel="modulepreload" href="{up}vendor/three.module.min.js"><script>{HEADJS}</script><style>{ff}{CSS}</style></head><body>'
      f'<header><a class="logo" href="{t["home"]}" aria-label="EM Visions"><svg viewBox="{logo_vb}" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{logo_d}"/></svg></a>'
      f'<nav><a href="{t["home"]}">← {e(t["back"])}</a><a href="{t["other"][1]}" hreflang="{t["other"][0].lower()}" lang="{t["other"][0].lower()}">{t["other"][0]}</a></nav></header>'
      f'<main class="wrap"><section class="stagebox"><canvas id="view" tabindex="0" role="img" aria-label="{e(t["view"])}"></canvas>'
      f'<p class="cap"><b><span id="pname"></span><small id="colname"></small></b><i><svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12a8 4 0 1 0 8-4M9 5l3 3-3 3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>{e(t["hint"])}</i></p></section>'
      f'<aside class="panel"><h1>{e(t["h1"])}</h1><p class="lead">{e(t["lead"])}</p>'
      f'<h2><b>1</b>{e(t["s1"])}</h2><div class="prods" id="prods"></div>'
      f'<h2><b>2</b>{e(t["s2"])}</h2><div class="cols" id="cols"></div>'
      f'<h2><b>3</b>{e(t["s3"])}</h2><div class="tabs" id="tabs" hidden></div>'
      f'<label class="up"><input type="file" id="file" accept="image/png,image/jpeg,image/webp,image/svg+xml"><svg width="26" height="26" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 16V4M7 9l5-5 5 5M4 17v2a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span><b id="upname">{e(t["pick"])}</b><small>{e(t["fmt"])}</small></span></label>'
      f'<div id="adj" hidden>{sl("size",t["size"],.15,1.8,.01,.9)}{sl("cx",t["x"],-1.2,1.2,.01,0)}{sl("cy",t["y"],-1.2,1.2,.01,0)}{sl("rot",t["rot"],-180,180,1,0)}<button type="button" class="rm" id="rm">{e(t["rm"])}</button></div>'
      f'<button type="button" class="cta" id="send" data-to="{t["to"]}">{e(t["send"])}<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h16M13 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>'
      f'<p class="note">{e(t["note"])}</p></aside></main><div class="toast" id="toast" role="status"></div>'
      f'<script type="module" src="{t["app"]}"></script></body></html>')
def write(logo_vb,logo_d):
    for L,d in (('fr','out/maquette'),('en','out/en/mockup')):
        os.makedirs(d,exist_ok=True); open(d+'/index.html','w').write(page(L,logo_vb,logo_d))
    shutil.copy('maquette_app.js','out/maquette/app.js'); shutil.copy('maquette_produits.js','out/maquette/produits.js')
