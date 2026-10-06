import re
import numpy as np
import json, os, sys, html as H
from mobile import mobile_html, MCSS
from i18n import EN, SLUG, TITLES
import buttons, mobile as MOB
from config import SITE_URL, CONTACT_EMAIL, INSTAGRAM, HOURS, HOURS_FR, ABOUT_FR
HH,SH=112,880
LOGO_D=open('logo_path.txt').read()
LOGO_VB=open('logo_vb.txt').read()
EL=json.load(open('elements.json')); META=json.load(open('meta.json'))
C=json.load(open('cal2.json')) if os.path.exists('cal2.json') else {}
V=json.load(open('var2.json')) if os.path.exists('var2.json') else {}
CAL='cal' in sys.argv
ORDER=['accueil','services','realisations','catalogue','a-propos','contact']
FONTS=[('Sekuya',400,'sekuya-latin-400'),('Anton',400,'anton-latin-400'),('Jost',300,'jost-latin-300'),('Jost',400,'jost-latin-400'),('Jost',700,'jost-latin-700'),
 ('Kumbh Sans',300,'kumbh-sans-latin-300'),('Kumbh Sans',400,'kumbh-sans-latin-400'),('Kumbh Sans',600,'kumbh-sans-latin-600'),('Oswald',700,'oswald-latin-700'),
 ('Inter',400,'inter-latin-400'),('Inter',500,'inter-latin-500'),('Inter',600,'inter-latin-600'),('Figtree',400,'figtree-latin-400'),('Figtree',600,'figtree-latin-600'),
 ('Figtree',700,'figtree-latin-700'),('Kumbh Sans',700,'kumbh-sans-latin-700'),('Inter',700,'inter-latin-700')]
BG={'w':'#000','b':'#000','wt':'#0a3cff','k':'#ececec','k2':'#ececec','g':'#ececec'}
# Big titles in Sekuya: capitals with 5% letterspacing (Butterick: 5-12% for caps, low end at display sizes).
# Each block is set at one size so its widest line fills the column the mockup title used.
from PIL import ImageFont as _IF
_SK=_IF.truetype('sekuya.ttf',1000); SK_LS=.05; SK_CAP=.70; SK_TOP=.15; SK_PITCH=.94
def _sk_w(t): return _SK.getlength(t.upper())/1000+SK_LS*(len(t)-1)
SEK={}
def _sekuya():
    blocks={}
    for e in EL:
        if e['group']=='h1': blocks.setdefault((e['page'],e['block']),[]).append(e)
    for (p,b),ls in blocks.items():
        ls.sort(key=lambda e:e['box'][1]); x=min(e['box'][0] for e in ls); avail=max(e['box'][2] for e in ls)-x
        fs=avail/max(_sk_w(e['text']) for e in ls); bottom=ls[-1]['box'][3]; n=len(ls)
        for i,e in enumerate(ls):
            cap_top=bottom-SK_CAP*fs-(n-1-i)*SK_PITCH*fs
            SEK[e['id']]={'fs':fs,'x':x,'y':cap_top-SK_TOP*fs,'w':_sk_w(e['text'])*fs,'avail':avail,'base':cap_top+SK_CAP*fs}
_sekuya()
def spec(e):
    s=dict(e['spec']); s.update(V.get(e['id'],{})); s.update(V.get('group:'+e['page']+':'+str(e['group']),{})); return s
def span(e):
    s=spec(e); x0,y0,x1,y1=e['box']; hh=y1-y0; c=C.get(e['id'],{})
    k=SEK.get(e['id'])
    if k: s=dict(s,f='Sekuya',css=''); c={'fs':k['fs'],'x':k['x'],'y':k['y'],'sx':1,'ls':SK_LS*k['fs']}
    fs=c.get('fs',hh*(1.36 if s['f'] in('Anton','Oswald') else 1.4)); x=c.get('x',x0); y=c.get('y',y0-fs*.25)
    st=f"--x:{x:.2f};--y:{y:.2f};--fs:{fs:.3f};--sx:{c.get('sx',1):.4f};--ls:{c.get('ls',0):.3f};font-family:'{s['f']}';font-weight:{s.get('w',400)};color:{e['color']};{s.get('css','')}"
    if CAL: st+=f";--bg:{BG[e['cls']]}"
    dc=f' data-count="{e["page"]}"' if e['id'].endswith('-count') else ''
    if e['group'] in ('nav','small','btn'): dc+=' data-align="center"'
    if e['text']=='Itinéraire': dc+=' data-fixed'
    if k: dc+=f' data-maxw="{k["avail"]:.1f}"'
    return f'<span class="t" id="{e["id"]}"{dc} data-cls="{e["cls"]}" style="{st}">{H.escape(e["text"])}</span>'
def box(b,extra=''): x0,y0,x1,y1=b; return f'style="left:{x0}px;top:{y0}px;width:{x1-x0}px;height:{y1-y0}px;{extra}"'
TOAST={'en':'La version anglaise sera ajoutée après validation du français.','theme':'Le thème clair n’est pas encore maquetté.'}
def page_html(p):
    els=[e for e in EL if e['page']==p]; M=META[p]; out=[]
    for i,s in enumerate(M['slots']): out.append(f'<div class="slot" data-pg="{p}" data-slot="{i}" {box(s)}></div>')
    out.append(MOB.plate_img('plate',p))
    if p=='catalogue':
        b=M['band']; out.append(f'<img class="band" id="cat-band" src="img/cat-band.webp" alt="" aria-hidden="true" loading="lazy" {box(b)}>')
    out.append(vclips(p))
    out.append('<div class="ui">')
    for q in M.get('sq',[]):
        k=SEK.get(q['line'])
        if k:
            z=.2*k['fs']; qx=k['x']+k['w']+.09*k['fs']; q=dict(q,box=[qx,k['base']-z,qx+z,k['base']])
        out.append(f'<i class="sqd" aria-hidden="true" data-line="{q["line"]}" {box(q["box"],"background:"+q["color"])}></i>')
    for v in M.get('vec',[]):
        if v['kind'] in ('logo','toggle') or v.get('row')==0 or (p=='a-propos' and v['kind']=='pill'): continue
        out.append(buttons.svg(v))
    groups={}
    for e in els: groups.setdefault((e['group'],e['block']),[]).append(e)
    for (g,bi),L in groups.items():
        e0=L[0]
        if g in ('nav','lang') or (p=='a-propos' and g=='cta'):
            continue
        elif g=='ph':
            continue
        elif g=='vf':
            d0=[v for v in M['vec'] if v.get('row')==0]
            out.append(f'<div class="vfwrap" id="cat-vf">{span(L[0])}'+''.join(buttons.svg(v) for v in d0)+'</div>')
        elif g=='sup':
            e=L[0]; r=e['row']; y=M['rows'][r]
            su=MOB.SUP_URL.get(r); out.append(f'<a class="sup" '+(f'href="{su}" target="_blank" rel="noopener"' if su else 'href="#catalogue"')+f' data-row="{r}" aria-label="{H.escape(e["text"])} — voir le fournisseur" style="left:70px;top:{y-32}px;width:590px;height:64px"></a>'+span(e).replace('class="t"','class="t" data-suprow="%d"%s'%(r,' data-fixed' if r==0 else ''),1)+MOB.sup_chip(r,e['text'],'d',f' style="left:98px;top:{y-25}px"'))
        else:
            tag=e0.get('tag') or 'div'
            if p!='accueil' and tag=='h1': tag='h2'
            elif p!='accueil' and tag=='h2': tag='h3'
            out.append(f'<{tag} class="grp">'+''.join(span(e) for e in L)+f'</{tag}>')
            if e0.get('link'):
                href,b=e0['link']; ext=' target="_blank" rel="noopener"' if href.startswith('http') else ''
                idattr=' id="%s-hit"'%e0['id'] if e0['id'].endswith('voir') else ''
                out.append(f'<a class="hit pill"{idattr} href="{href}"{ext} aria-label="{H.escape(e0["text"])}" {box(b)}></a>')
    if p in ('accueil','realisations'):
        out.append(f'''<div class="car" data-page="{p}"><button class="hit round prev arrow" data-pg="{p}" aria-label="Image précédente" style="left:1257px;top:835px;width:47px;height:47px"><svg width="24" height="24" viewBox="0 0 24 24"><path d="M20 12H4M11 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
<button class="hit round next arrow" data-pg="{p}" aria-label="Image suivante" style="left:1443px;top:835px;width:47px;height:47px"><svg width="24" height="24" viewBox="0 0 24 24"><path d="M4 12h16M13 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="bars" data-pg="{p}"></div>{PPBTN if p=='accueil' else ''}</div>''')
    if p=='catalogue': out.append('<a class="m3dpill" data-m3d href="maquette/" style="left:77px;top:910px">Essayer sur un produit en 3D <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h16M13 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>')
    if p=='a-propos': out.append(f'<p class="about" style="left:1033px;top:736px;width:440px">{H.escape(ABOUT_FR)}</p>')
    if p=='contact':
        F=[('nom','text','name',(954,295,1495,338)),('courriel','email','email',(954,386,1495,430)),('projet','textarea','',(954,479,1495,588)),('qte','number','',(954,636,1495,680))]
        if HOURS: out.append(MOB.hours_grid('dh',' style="left:262px;top:846px"'))
        out.append(f'<form id="devis" class="qform" novalidate{MOB.form_attrs()}>'+MOB.form_hidden())
        for name,typ,ac,b in F:
            ph=[e for e in els if e.get('ph')==name][0]
            req=' required' if name in('nom','courriel','projet') else ''
            lab=[e for e in els if e.get('label')==name][0]['text']
            common=f'id="f-{name}" name="{name}" aria-label="{H.escape(lab)}" placeholder=" "{req}'+(f' autocomplete="{ac}"' if ac else '')
            ctl=f'<textarea {common} maxlength="5000"></textarea>' if typ=='textarea' else f'<input type="{typ}" {common}'+(' min="1" inputmode="numeric"' if typ=='number' else ' maxlength="150"')+'>'
            phs=span(ph).replace('class="t"','class="t ph"')
            out.append(f'<div class="fld" {box(b)}>{ctl}{phs}<em class="err" id="e-{name}" data-err="{name}"></em></div>')
        out.append('<label class="file" style="left:954px;top:728px;width:541px;height:76px"><input type="file" id="f-fichier" name="fichier" accept=".jpg,.jpeg,.png,.pdf,image/jpeg,image/png,application/pdf"><span class="sr">Joindre un visuel</span></label>')
        out.append('<em class="err" id="e-fichier" data-err="fichier" style="left:958px;top:806px"></em>')
        out.append('<button type="submit" class="hit submit" style="left:954px;top:814px;width:541px;height:57px"><span class="sr">Demander un devis</span></button>')
        out.append('<a class="m3d" data-m3d href="maquette/" style="left:1195px;top:698px;width:300px">ou créer une maquette 3D →</a>')
        out.append('<a class="plink" data-privacy href="confidentialite/" style="left:1074px;top:920px;width:300px">Politique de confidentialité</a>')
        out.append('</form><div class="ok" id="ok" hidden role="status" tabindex="-1"><b>MERCI.</b><p>Votre demande est bien envoyée.</p><p class="note">Nous vous répondrons par courriel.</p><p class="note ref"></p><button type="button" class="again">Nouvelle demande</button></div>'+MOB.ko_html()+'')
    out.append('</div>')
    return '<div class="pin">'+'\n'.join(out)+'</div>'
UID=[0]
def tear_svg(t):
    return ''
    UID[0]+=1; u=f"tc{UID[0]}"
    x0,y0,x1,y1=t['box']; w_,h_=x1-x0,y1-y0
    inner="".join(pc['d'] for pc in t['pieces'])
    ring=(f'<g class="ring"><path d="{t["outer"]}{inner}" fill-rule="evenodd" fill="url(#paperpat)"/>'
          +"".join(f'<path class="tl" pathLength="1" d="{pc["d"]}"/>' for pc in t['pieces'])+'</g>')
    pcs="".join(f'<g class="pc" style="--dx:{pc["dx"]:.0f};--dy:{pc["dy"]:.0f};--rot:{pc["rot"]:.1f};--dl:{pc["delay"]:.2f}"><path d="{pc["d"]}" fill="url(#paperpat)"/>'
                f'<path class="tl" pathLength="1" d="{pc["d"]}"/><path class="tc" pathLength="1" d="{pc["d"]}"/></g>' for pc in t['pieces'])
    return (f'<svg class="tear" aria-hidden="true" style="left:{x0}px;top:{y0}px;width:{w_}px;height:{h_}px" viewBox="{x0} {y0} {w_} {h_}">{ring}{pcs}</svg>')
VIDS={'buono':'vid/buono.mp4','ma':'vid/ma.mp4','caps':'vid/caps.mp4','balloon':'vid/balloon.mp4','ricova':'vid/ricova.mp4','elevate':'vid/elevate.mp4','atelier':'vid/atelier.mp4'}
A_={'Notre atelier': 'Devanture de l’atelier EM Custom Design, rue Jean-Talon Est', 'Ricova': 'Manteau de travail haute visibilité au logo Ricova', 'Buono Bites': 'Lettrage de vitrine pour le pop-up shop Buono Bites', 'Elevate': 'T-shirt imprimé El3vate Miami, palmiers et bandes dégradées', 'Enseigne MA': 'Enseigne ronde suspendue M/A', 'Balloon Babe': 'Impression Balloon Babe sur tissu rose'}
PPBTN='<button class="hit round arrow pp" data-pg="accueil" data-on="1" aria-label="Mettre le carrousel en pause" style="left:1198px;top:840px;width:37px;height:37px"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6v12M15 6v12" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M8.5 5.5v13l10-6.5z" fill="currentColor"/></svg></button>'
VALT={'ma':A_['Enseigne MA'],'caps':'Casquettes bleues et blanches au logo EM','atelier':A_['Notre atelier']}
VCLIP={'services':[(1,'ma','img/ma-main.webp','50% 50%',None)],'catalogue':[(0,'caps','img/src-emcap.webp','50% 45%',1)],
       # contact: the storefront video is placed with the similarity transform that lines it up with the photo printed in the plate
       'contact':[(0,'atelier','img/atelier-poster.webp','50% 50%',None,{'ti':0,'size':(800,1088),'mat':(0.637387,0.008368,-0.008368,0.637387,-69.753,-176.879),'mask':'img/atelier-mask.png'})]}
def _shift(d,dx,dy):
    nums=re.findall(r'-?\d+\.?\d*',d); it=iter(range(len(nums)))
    out=[];k=[0]
    def rep(m):
        v=float(m.group(0)); r=v-(dx if k[0]%2==0 else dy); k[0]+=1; return f"{r:.1f}"
    return re.sub(r'-?\d+\.?\d*',rep,d)
def vclips(p,bounds=None):
    o=[]
    for ti,t in enumerate(META[p].get('tears',[])):
        for i,pc in enumerate(t['pieces']):
            for ent in VCLIP.get(p,[]):
                pi,v,poster,pos,minus=ent[:5]; opt=ent[5] if len(ent)>5 else {}
                if pi!=i or opt.get('ti',ti)!=ti: continue
                x0,y0,x1,y1=pc['box']
                if bounds and not (bounds[0]<=(x0+x1)/2<=bounds[2] and bounds[1]<=(y0+y1)/2<=bounds[3]): continue
                path=_shift(pc['d'],x0,y0)
                vst=f'object-position:{pos}'
                if 'mat' in opt: vst=f"inset:auto;left:0;top:0;width:{opt['size'][0]}px;height:{opt['size'][1]}px;object-fit:fill;transform-origin:0 0;transform:matrix({','.join(str(m) for m in opt['mat'])})"
                keep=''
                if minus is not None:
                    q=t['pieces'][minus]; a0,b0,a1,b1=q['box']; qp=_shift(q['d'],a0,b0)
                    keep=(f'<div class="vclip vkeep" style="left:{a0}px;top:{b0}px;width:{a1-a0}px;height:{b1-b0}px;clip-path:path(\'{qp}\')">'
                          f'<img data-plate="{p}" data-defer="1" data-dark="img/plate-{p}.webp" alt="" style="position:absolute;left:{-a0}px;top:{-b0}px;width:1586px;height:992px;max-width:none"></div>')
                mk=f";-webkit-mask:url({opt['mask']}) 0 0/100% 100% no-repeat;mask:url({opt['mask']}) 0 0/100% 100% no-repeat;background:none" if opt.get('mask') else ''
                o.append(f'<div class="vclip" role="img" aria-label="{H.escape(VALT[v])}" style="left:{x0}px;top:{y0}px;width:{x1-x0}px;height:{y1-y0}px;clip-path:path(\'{path}\'){mk}">'
                         f'<video src="{VIDS[v]}" data-poster="{poster}" style="{vst}" muted loop playsinline preload="none" aria-hidden="true"></video></div>'+keep)
    return ''.join(o)
def header_html():
    els=[e for e in EL if e['page']=='accueil']
    nav=[e for e in els if e['group']=='nav']; fr=[e for e in els if e['group']=='lang' and e['text']=='FR'][0]; en=[e for e in els if e['group']=='lang' and e['text']=='EN'][0]
    t=[v for v in META['accueil']['vec'] if v['kind']=='toggle'][0]['box']
    tog=(f'<button class="theme-toggle htog" aria-label="Mode sombre" aria-pressed="true" style="left:{t[0]}px;top:{t[1]}px;width:{t[2]-t[0]}px;height:{t[3]-t[1]}px">'
         f'<svg viewBox="0 0 59 59" aria-hidden="true"><circle cx="29.5" cy="29.5" r="22.3" fill="none" stroke="#0a3cff" stroke-width="2.6"/>'
         f'<path class="moon" d="M32.4 19.2a10.6 10.6 0 1 0 6.9 17.2 8.6 8.6 0 0 1-6.9-17.2z"/></svg></button>')
    return (f'<header class="dhead" id="dhead"><picture><source data-th srcset="img/head-light.webp" media="(prefers-color-scheme: light)"><img class="hbg" data-plate="head" src="img/head.webp" alt="" aria-hidden="true"></picture>'
            f'<a class="hlogo" href="#accueil" aria-label="EM Visions — accueil"><svg viewBox="{LOGO_VB}" aria-hidden="true"><use href="#emlogo"/></svg></a>'
            '<nav aria-label="Navigation principale">'+''.join(f'<a class="nl" data-key="{e["href"][1:]}" href="{e["href"]}">{span(e)}</a>' for e in nav)+'</nav>'
            f'<i class="uline" aria-hidden="true"></i><a class="nl lang-fr" href="#accueil" hreflang="fr" lang="fr">{span(fr)}</a><a class="nl lang-en" href="en/#home" hreflang="en" lang="en">{span(en)}</a>{tog}</header>')
def vecf(p,b):
    x0,y0,x1,y1=b; o=[]
    for v in META[p].get('vec',[]):
        if v['kind'] in ('logo','toggle'): continue
        a=v['box']
        if a[0]>=x0-2 and a[1]>=y0-2 and a[2]<=x1+2 and a[3]<=y1+2: o.append(buttons.svg(v))
    o.insert(0,vclips(p,(x0,y0,x1,y1)))
    return ''.join(o)
MOB.VECF=vecf
MOB.LOGO=f'<svg class="logo-svg" viewBox="{LOGO_VB}" role="img" aria-label="EM Visions"><use href="#emlogo"/></svg>'
ff='\n'.join(f"@font-face{{font-family:'{n}';font-weight:{w};src:url(fonts/{f}-normal.woff2) format('woff2')}}" for n,w,f in FONTS)
CSS=ff+'''
:root{--blue:#0a3cff;--fg:#fff}html[data-theme=light]{--fg:#141414}
html{scroll-behavior:auto}@media (max-width:1024px){.dhead{display:none}}
html[data-theme=light],html[data-theme=light] body{background:#e9e9e6}html[data-theme=light] .stage{background:#e9e9e6}
html[data-theme=light] .t[data-cls=w]:not([data-fixed]):not(.vfwrap .t):not(.lang-en .t):not(.lang-fr .t){color:#141414!important}
html[data-theme=light] .bars button i{background:#141414}html[data-theme=light] .bars button[aria-current=true] i{background:var(--blue)}*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#050505;overflow-x:clip}a{color:inherit;text-decoration:none}
.frame{position:relative;width:100%;overflow:hidden}
.stage{position:absolute;left:0;top:0;width:1586px;transform-origin:0 0;background:#060606}
.page{position:absolute;left:0;width:1586px;overflow:hidden}.pin{position:absolute;left:0;top:-112px;width:1586px;height:992px}
.dhead{position:fixed;left:0;top:0;width:1586px;height:112px;transform-origin:0 0;z-index:30}
.hbg{position:absolute;inset:0;width:1586px;height:112px;-webkit-mask-image:linear-gradient(#000 78%,transparent);mask-image:linear-gradient(#000 78%,transparent);pointer-events:none}
.hlogo{position:absolute;left:79px;top:15px;width:214px;height:100px;color:var(--fg);display:block}.hlogo svg{width:100%;height:100%;display:block}
.htog{position:absolute;background:none;border:0;padding:0;cursor:pointer;border-radius:50%}.htog svg{width:100%;height:100%;display:block}.htog .moon{fill:var(--fg)}.htog:hover circle{fill:#0a3cff33}
.uline{position:absolute;top:75px;height:5px;background:var(--blue);transition:left .35s cubic-bezier(.3,.8,.3,1),width .35s cubic-bezier(.3,.8,.3,1)}
.vsvg{position:absolute;overflow:visible;pointer-events:none}
.vclip{position:absolute;z-index:2;overflow:hidden;pointer-events:none;background:#111}.vclip video,.slot video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
@media (prefers-reduced-motion:reduce){.slot video,.vclip{display:none}}
.tear{position:absolute;z-index:2;overflow:visible;pointer-events:none;--p:0}
.tear .pc{--q:clamp(0,calc((var(--p) - .5 - var(--dl)) * 2.2),1);transform-box:fill-box;transform-origin:50% 50%;
 transform:translate(calc(var(--q)*var(--dx)*1px),calc(var(--q)*var(--q)*var(--dy)*1px - var(--q)*40px)) rotate(calc(var(--q)*var(--rot)*1deg)) scale(calc(1 + var(--q)*.06));opacity:calc(1 - max(0, var(--q) - .55) * 2.3)}
.tear .ring{opacity:calc(1 - max(0, var(--p) - .78) * 4.6)}
.tear .tl{fill:none;stroke:#fbfbf9;stroke-linecap:round;stroke-linejoin:round;stroke-width:calc(1px + min(1, var(--p)*2)*9px);stroke-dasharray:1 1;stroke-dashoffset:calc(1 - min(1, var(--p)*1.95));filter:url(#fiber)}
.tear .tc{fill:none;stroke:#0000006b;stroke-width:1.6;stroke-dasharray:.004 .003;opacity:calc(min(1, var(--p)*1.95))}
.tear.gone{visibility:hidden}
@media (prefers-reduced-motion:reduce){.tear{display:none}}
.slot{position:absolute;overflow:hidden;z-index:1;background:#111;cursor:pointer}
.slot img,.slot video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .55s ease,transform .9s cubic-bezier(.2,.7,.2,1)}
.slot img.out,.slot video.out{opacity:0;transform:scale(1.04)}
.plate{position:absolute;left:0;top:0;width:1586px;height:992px;z-index:2;pointer-events:none;user-select:none}
.band{position:absolute;z-index:2;pointer-events:none;transition:transform .32s cubic-bezier(.3,.8,.3,1)}
.ui{position:absolute;inset:0;z-index:3;pointer-events:none}.ui a,.ui button,.ui input,.ui textarea,.ui label{pointer-events:auto}
.t{position:absolute;left:calc(var(--x)*1px);top:calc(var(--y)*1px);font-size:calc(var(--fs)*1px);line-height:1;white-space:nowrap;transform:scaleX(var(--sx));transform-origin:0 0;letter-spacing:calc(var(--ls)*1px);pointer-events:none}
.grp,nav,address{font-style:normal;font-weight:inherit;font-size:inherit}
.nl .t{pointer-events:auto;transition:opacity .2s}.nl .t::after{content:'';position:absolute;inset:-12px -10px}.nl:hover .t{opacity:.65}
.hit{position:absolute;background:transparent;border:0;cursor:pointer;display:block}
.schip{display:inline-flex;align-items:center;height:50px;padding:0 14px;background:#fff;border-radius:5px;box-shadow:0 2px 8px #0005;pointer-events:none;flex:none}
.schip img{display:block;width:auto}.schip.dk{background:#0d0d0d;box-shadow:0 0 0 1px #666,0 2px 8px #0005}
.schip.tx{font:400 27px/1 Anton,sans-serif;color:#0a0a0a;text-transform:uppercase;letter-spacing:.01em;white-space:nowrap}
.schip.d{position:absolute}[data-suprow]{opacity:0!important}
.hgrid{list-style:none;display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin:0;padding:0}
.hgrid li{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;text-align:center}
.hgrid b{font:700 11px/1 Oswald,sans-serif;text-transform:uppercase;letter-spacing:.08em}.hgrid span{font:400 17px/1 Anton,sans-serif;white-space:nowrap}
.hgrid b:after{content:"";display:block;width:14px;height:2px;margin:5px auto 2px;background:#0a3cff}.hgrid li.now b:after,.hgrid li.off b:after{background:currentColor}
.hgrid li.off{border:1.5px dashed currentColor}.hgrid li.off span{font:600 10.5px/1 'Kumbh Sans',sans-serif;text-transform:none;opacity:.85}
.hgrid.dh{position:absolute;width:452px;height:64px;filter:drop-shadow(0 2px 8px #0007)}.hgrid.dh li{border-radius:6px;background:#0b0b0b;color:#fff}.hgrid.dh li.off{background:#0b0b0bcc;border-color:#ffffff88}
.hgrid.dh li.now{background:#0a3cff}
.about{position:absolute;color:var(--fg);font:300 17.5px/1.52 'Kumbh Sans',sans-serif;letter-spacing:.01em}
.plink{position:absolute;text-align:center;font:400 11.5px/1.3 Inter,sans-serif;color:#3a3a3b;text-decoration:underline;text-underline-offset:2px}.plink:hover{color:#0a3cff}
.hp{display:none!important}picture{display:contents}.m3d{position:absolute;text-align:right;font:500 13px/1.3 Inter,sans-serif;color:#0a3cff;text-decoration:underline;text-underline-offset:2px}.m3d:hover{color:#000}
.m3dpill{position:absolute;display:inline-flex;align-items:center;gap:10px;height:46px;padding:0 20px;border-radius:23px;border:2px solid #0a3cff;color:var(--fg);font:600 15.5px/1 'Kumbh Sans',sans-serif;text-decoration:none;white-space:nowrap;background:#0a3cff22}.m3dpill:hover{background:#0a3cff;color:#fff}
.round{border-radius:50%}.pp svg+svg,.pp[data-on="0"] svg{display:none}.pp[data-on="0"] svg+svg{display:block}.pp[hidden]{display:none!important}.arrow{color:var(--fg);border:2px solid var(--fg);display:grid;place-items:center;transition:background .2s,border-color .2s}.arrow:hover{background:var(--blue)!important;border-color:var(--blue)}.round:hover{background:#0a3cff55}
.pill{border-radius:44px}.pill:hover{backdrop-filter:brightness(1.12) contrast(1.05)}
.hit:focus-visible,.sup:focus-visible,.nl:focus-visible .t,.fld :focus-visible{outline:3px solid #6f8cff;outline-offset:3px}
.bars{position:absolute;left:1257px;top:898px;width:233px;height:16px}
.bars button{position:absolute;top:0;height:16px;background:none;border:0;cursor:pointer}
.bars button i{position:absolute;left:0;right:0;top:9px;height:2px;background:#fff;transition:all .3s}
.bars button[aria-current=true] i{top:6px;height:6px;background:var(--blue)}
.sup{position:absolute;display:block}.sqd{position:absolute;display:block}.vfwrap{position:absolute;inset:0;transition:transform .32s cubic-bezier(.3,.8,.3,1);pointer-events:none}
.fld{position:absolute}
.fld input,.fld textarea{position:absolute;inset:0;width:100%;height:100%;border:0;background:transparent;font:400 17px/1.35 Inter,sans-serif;color:#1a1a1a;padding:0 18px;outline:none;resize:none}
.fld textarea{padding:8px 18px}.fld input::-webkit-outer-spin-button,.fld input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}.fld input[type=number]{-moz-appearance:textfield}
.fld .ph{opacity:1}.fld input:not(:placeholder-shown)~.ph,.fld textarea:not(:placeholder-shown)~.ph{opacity:0}
.fld .ph{left:calc(var(--x)*1px - var(--ox));top:calc(var(--y)*1px - var(--oy))}
.fld.bad{box-shadow:inset 0 0 0 2px #d6002a;border-radius:3px}
.err{position:absolute;right:10px;bottom:-15px;font:600 11px Inter,sans-serif;color:#d6002a;font-style:normal;white-space:nowrap}
#e-fichier{right:auto}
.file{position:absolute;cursor:pointer;border-radius:4px}.file input{position:absolute;inset:0;opacity:0;cursor:pointer}.file:hover{background:#0a3cff10}
.submit{border-radius:4px}.submit:hover{backdrop-filter:brightness(1.18)}
.ok{position:absolute;left:930px;top:160px;width:590px;height:780px;display:flex;flex-direction:column;justify-content:center;padding:0 60px;background:#eeeeec;font-family:Inter,sans-serif;color:#111;pointer-events:auto;border-radius:6px}
.ok[hidden],form[hidden]{display:none}.ok b{font:400 96px/1 Anton;letter-spacing:-2px}.ok p{font-size:20px;margin-top:18px}.ok .note{font-size:14px;color:#555}
.ok:focus{outline:0}.okb{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin-top:30px}.ok .okb button{margin-top:0}.ok{scroll-margin-top:96px}.bymail{font:600 16px Inter,sans-serif;color:#0a3cff;padding:14px 4px}
.ok button{margin-top:30px;align-self:flex-start;background:var(--blue);color:#fff;border:0;padding:14px 26px;font:600 16px Inter;cursor:pointer;border-radius:4px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(20px);background:#0a3cff;color:#fff;font:500 15px Inter,sans-serif;padding:12px 20px;border-radius:6px;opacity:0;transition:.3s;z-index:9;pointer-events:none}
.toast.on{opacity:1;transform:translateX(-50%)}
.lb{position:fixed;inset:0;background:#000d;display:grid;place-items:center;z-index:8}.lb[hidden]{display:none}
.lb figure{max-width:90vw;max-height:90vh;text-align:center;color:#fff;font:400 28px Anton}.lb img{max-width:90vw;max-height:80vh;display:block;margin:0 auto 12px;border:8px solid #f4f4f2}
.lb button{position:absolute;top:18px;right:22px;background:none;border:2px solid #fff;color:#fff;border-radius:50%;width:48px;height:48px;font-size:24px;cursor:pointer}
'''
CALCSS='''body.cal .plate,body.cal .slot,body.cal .band{display:none}body.cal .page{transition:none}body.cal .t{visibility:hidden}body.cal .t.show{visibility:visible}body.cal .sqd{display:none}
body.cal .stage{background:var(--calbg,#000)}body.cal .fld .ph{opacity:1!important}body.cal .bars,body.cal .ok,body.cal .err,body.cal .toast{display:none!important}'''
JS=r'''
const stage=document.getElementById('stage'),frame=document.getElementById('frame');
const HH=112,SH=880,dhead=document.getElementById('dhead');function fit(){const k=Math.max(frame.clientWidth,320)/1586;stage.style.transform='scale('+k+')';dhead.style.transform='scale('+k+')';frame.style.height=((HH+6*SH)*k)+'px'}
addEventListener('resize',fit);fit();
const PAGES=%PAGES%;
const LANG=document.documentElement.lang==='en'?'en':'fr',IDX=location.protocol==='file:'?'index.html':'';let curPage='accueil',lang=LANG;const EN=%EN%,SLUG=%SLUG%,TITLES=%TITLES%;const UNSLUG=Object.fromEntries(Object.entries(SLUG).map(([a,b])=>[b,a]));
function T(s){return lang==='en'?(EN[s]??s):s}
let REC=null;const MQ=matchMedia('(max-width:1024px)');const isM=()=>MQ.matches;
function collect(){REC={txt:[],attr:[],links:[]};if(LANG==='en'){const pgOf=e=>(e.closest('.page,.mpage')||{id:''}).id.replace(/^[pm]-/,'');document.querySelectorAll('[data-fr]').forEach(el=>{let m;try{m=JSON.parse(el.dataset.fr)}catch(_){return}const pg=pgOf(el);Object.keys(m).forEach(i=>{const n=el.childNodes[i],fr=m[i];if(!n||n.nodeType!==3)return;const v=n.nodeValue,t=v.trim();if(t&&t===(EN[pg+':'+fr]??EN[fr]))n.nodeValue=v.slice(0,v.indexOf(t))+fr+v.slice(v.indexOf(t)+t.length)})});document.querySelectorAll('[data-fra]').forEach(el=>{let m;try{m=JSON.parse(el.dataset.fra)}catch(_){return}Object.keys(m).forEach(a=>{if(el.getAttribute(a)===EN[m[a]])el.setAttribute(a,m[a])})})}const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){const v=n.nodeValue,t=v.trim();if(!t||n.parentNode.closest('script,style'))continue;const pg=(n.parentNode.closest('.page,.mpage')||{id:''}).id.replace(/^[pm]-/,'');
  if(EN[t]!==undefined||EN[pg+':'+t]!==undefined)REC.txt.push({n,fr:t,pg,lead:v.slice(0,v.indexOf(t)),trail:v.slice(v.indexOf(t)+t.length)})}
 document.querySelectorAll('[aria-label],[placeholder],[alt]').forEach(el=>['aria-label','placeholder','alt'].forEach(a=>{const v=el.getAttribute(a);if(v&&EN[v]!==undefined)REC.attr.push({el,a,fr:v})}));
 document.querySelectorAll('a[href^="#"]').forEach(a=>{let k=a.getAttribute('href').slice(1);if(LANG==='en')k=UNSLUG[k]||k;if(SLUG[k]&&!a.classList.contains('lang-fr')&&!a.classList.contains('lang-en')&&!a.closest('.lang'))REC.links.push({a,k})});
 document.querySelectorAll('.t,.sqd').forEach(el=>{el._fr=el.style.cssText})}
function refOf(el){return el.closest('.cin')||el.closest('.dhead')||stage}
function box(el){const ref=refOf(el),R=ref.getBoundingClientRect(),r=el.getBoundingClientRect(),K=R.width/1586||1;return{l:(r.left-R.left)/K,r:(r.right-R.left)/K,c:((r.left+r.right)/2-R.left)/K}}
const vis=el=>el.getClientRects().length>0;
const lineOf=q=>{const c=q.closest('.cin');return c?c.querySelector('#m-'+q.dataset.line):document.getElementById(q.dataset.line)};
const sxOf=el=>parseFloat(el.style.getPropertyValue('--sx'))||1;
function apply(){if(!REC)return;document.documentElement.lang=lang;
 REC.txt.forEach(r=>{r.n.nodeValue=r.lead+r.fr+r.trail});
 document.querySelectorAll('.t,.sqd').forEach(el=>{if(el._fr!==undefined)el.style.cssText=el._fr});
 if(lang==='en'){const TS=[...document.querySelectorAll('.t')].filter(vis),QS=[...document.querySelectorAll('.sqd')].filter(vis);
  TS.forEach(el=>{el._w=+el.dataset.maxw||el.offsetWidth*sxOf(el);if(el.dataset.align==='center')el._c=box(el).c});
  QS.forEach(q=>{const l=lineOf(q);q._gap=l?parseFloat(q.style.left)-box(l).r:null});
  REC.txt.forEach(r=>{r.n.nodeValue=r.lead+(EN[r.pg+':'+r.fr]??EN[r.fr]??r.fr)+r.trail});
  TS.forEach(el=>{const sx=sxOf(el),w=el.offsetWidth*sx;if(!el._w||w<=el._w*1.02)return;
   if(/Anton|Oswald|Sekuya/.test(el.style.fontFamily))el.style.setProperty('--sx',sx*el._w/w);else{const n=Math.max(el.textContent.length-1,1),ls=parseFloat(el.style.getPropertyValue('--ls'))||0;el.style.setProperty('--ls',ls-(w-el._w)/sx/n)}});
  TS.forEach(el=>{if(el.dataset.align!=='center')return;const d=el._c-box(el).c;el.style.setProperty('--x',parseFloat(el.style.getPropertyValue('--x'))+d)});
  QS.forEach(q=>{const l=lineOf(q);if(l&&q._gap!=null)q.style.left=(box(l).r+q._gap)+'px'})}
 REC.attr.forEach(r=>r.el.setAttribute(r.a,T(r.fr)));
 REC.links.forEach(({a,k})=>a.setAttribute('href',hashFor(k)));
 const off=document.documentElement.dataset.theme==='light'?'#141414':'#fff';
 document.querySelectorAll('.lang-fr .t').forEach(x=>{x.style.color=lang==='fr'?'#0a3cff':off;x.style.fontWeight=lang==='fr'?700:400});
 document.querySelectorAll('.lang-en .t').forEach(x=>{x.style.color=lang==='en'?'#0a3cff':off;x.style.fontWeight=lang==='en'?700:400});
 document.querySelectorAll('.lang-fr').forEach(a=>a.toggleAttribute('aria-current',lang==='fr'));document.querySelectorAll('.lang-en').forEach(a=>a.toggleAttribute('aria-current',lang==='en'));
 setActive(curPage,true)}
function setActive(p,force){if(p===setActive.cur&&!force)return;setActive.cur=p;curPage=p;
 document.querySelectorAll('#dhead nav a').forEach(a=>{const on=a.dataset.key===p,t=a.querySelector('.t');a.toggleAttribute('aria-current',on);if(on)a.setAttribute('aria-current','page');
  if(vis(t)){const c0=box(t).c;t.style.fontWeight=on?700:400;const d=c0-box(t).c;t.style.setProperty('--x',parseFloat(t.style.getPropertyValue('--x'))+d)}else t.style.fontWeight=on?700:400});
 const at=document.querySelector('#dhead nav a[data-key="'+p+'"] .t'),ul=document.querySelector('.uline');
 if(at&&vis(at)){const b=box(at);ul.style.left=(b.l-2)+'px';ul.style.width=(b.r-b.l+4)+'px'}
 document.querySelectorAll('[data-nav]').forEach(a=>{a.removeAttribute('aria-current');if(a.dataset.nav===p)a.setAttribute('aria-current','page')});
 document.querySelectorAll('.lang-fr,.mlang-fr').forEach(a=>a.setAttribute('href',(LANG==='en'?'../'+IDX:'')+'#'+p));document.querySelectorAll('.lang-en,.mlang-en').forEach(a=>a.setAttribute('href',(LANG==='fr'?'en/'+IDX:'')+'#'+SLUG[p]));
 document.title=p==='accueil'?DOCT:TITLES[lang][p]+' — EM Visions';if(setActive.car!==p){const o=setActive.car;setActive.car=p;[o,p].forEach(k=>{if(k&&CARS[k]&&CARS[k].render)CARS[k].render()})}}
const DOCT=document.title;
function parse(h){h=(h||'').replace(/^#/,'');if(h==='en'||h.startsWith('en/')){const r=h.slice(3);if(LANG==='fr'){location.replace('en/'+IDX+(r?'#'+r:''));return{L:LANG,p:curPage}}h=r}
 if(LANG==='en')h=UNSLUG[h]||h;return{L:LANG,p:PAGES.includes(h)?h:'accueil'}}
function kk(){return Math.max(frame.clientWidth,320)/1586}
function secTop(p){if(isM()){const el=document.getElementById('m-'+p),mh=document.querySelector('.mhead');return el.getBoundingClientRect().top+scrollY-(mh?mh.offsetHeight:0)+(p==='accueil'?-999:0)}
 return frame.getBoundingClientRect().top+scrollY+PAGES.indexOf(p)*SH*kk()}
let lock=0;
function goTo(p,smooth){lock=Date.now();loadPage(p);setActive(p);scrollTo({top:Math.max(0,secTop(p)),behavior:smooth?'smooth':'auto'})}
function hashFor(p){return LANG==='en'?'#'+SLUG[p]:'#'+p}
function route(smooth){const{L,p}=parse(location.hash);const ch=L!==lang;lang=L;if(ch||!route.done)apply();route.done=1;goTo(p,smooth)}
addEventListener('hashchange',()=>route(true));
document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(!a||a.hasAttribute('data-voir')||a.id.endsWith('-voir-hit'))return;const h=a.getAttribute('href');if(h==='#'||h==='#p-accueil')return;
 const{L,p}=parse(h);if(!/^#(en\/)?[a-z-]*$/.test(h))return;e.preventDefault();const ch=L!==lang;lang=L;if(ch)apply();history.pushState(null,'',h);goTo(p,!ch);if(typeof menu==='function'&&!mnav.hidden)menu(false)});
let spyT=0;addEventListener('scroll',()=>{if(spyT)return;spyT=requestAnimationFrame(()=>{spyT=0;let p;
 if(isM()){const mh=(document.querySelector('.mhead')||{offsetHeight:0}).offsetHeight;p='accueil';PAGES.forEach(k=>{const el=document.getElementById('m-'+k);if(el.getBoundingClientRect().top<=mh+innerHeight*0.35)p=k})}
 else{const i=Math.min(5,Math.max(0,Math.floor((scrollY-frame.getBoundingClientRect().top-scrollY+innerHeight*0.45)/(SH*kk())+ (scrollY>0?0:0))));p=PAGES[Math.min(5,Math.max(0,Math.floor((scrollY+innerHeight*0.45-HH*kk())/(SH*kk()))))]}
 if(p!==curPage){setActive(p);if(Date.now()-lock>900)history.replaceState(null,'',hashFor(p))}})},{passive:true});
MQ.addEventListener('change',()=>{fit();requestAnimationFrame(()=>{fitCrops();apply();goTo(curPage,false)})});
document.querySelectorAll('.fld').forEach(f=>{const l=parseFloat(f.style.left),t=parseFloat(f.style.top);f.style.setProperty('--ox',l+'px');f.style.setProperty('--oy',t+'px')});
const toastEl=document.createElement('div');toastEl.className='toast';toastEl.setAttribute('role','status');document.body.appendChild(toastEl);let tt;
function toast(m){toastEl.textContent=T(m);toastEl.classList.add('on');clearTimeout(tt);tt=setTimeout(()=>toastEl.classList.remove('on'),2600)}
const TOAST=%TOAST%;document.querySelectorAll('[data-toast]').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();toast(TOAST[b.dataset.toast])}));
const VIDS=%VIDS%;
const SEGS=[[1257,1299],[1308,1349],[1356,1397],[1403,1443],[1448,1490]];
const SETS={accueil:[
 {n:'Notre atelier',a:'Devanture de l’atelier EM Custom Design, rue Jean-Talon Est',m:'img/dev-main.webp',t:'img/dev-main.webp',tp:'38% 50%',v:VIDS.atelier},
 {n:'Ricova',a:'Manteau de travail haute visibilité au logo Ricova',m:'img/ricova-main.webp',t:'img/ricova-thumb.webp',v:VIDS.ricova},
 {n:'Buono Bites',a:'Lettrage de vitrine pour le pop-up shop Buono Bites',m:'img/src-buono.webp',t:'img/buono-thumb.webp',v:VIDS.buono},
 {n:'Elevate',a:'T-shirt imprimé El3vate Miami, palmiers et bandes dégradées',m:'img/elevate-main.webp',t:'img/elevate-thumb.webp',v:VIDS.elevate},
 {n:'Enseigne MA',a:'Enseigne ronde suspendue M/A',m:'img/ma-main.webp',t:'img/ma-main.webp',tp:'45% 50%',v:VIDS.ma}],
 realisations:[
 {n:'Ricova',a:'Manteau de travail haute visibilité au logo Ricova',m:'img/ricova-main-exact.webp',t:'img/ricova-thumb.webp',big:'img/ricova-main.webp',v:VIDS.ricova},
 {n:'Buono Bites',a:'Lettrage de vitrine pour le pop-up shop Buono Bites',m:'img/src-buono.webp',t:'img/buono-thumb-r.webp',v:VIDS.buono},
 {n:'Elevate',a:'T-shirt imprimé El3vate Miami, palmiers et bandes dégradées',m:'img/elevate-main.webp',t:'img/elevate-thumb.webp',v:VIDS.elevate},
 {n:'Enseigne MA',a:'Enseigne ronde suspendue M/A',m:'img/ma-main.webp',t:'img/ma-main.webp',tp:'45% 50%',v:VIDS.ma},
 {n:'Balloon Babe',a:'Impression Balloon Babe sur tissu rose',m:'img/src-balloon.webp',t:'img/src-balloon.webp',v:VIDS.balloon}]};
const CARS={};
function put(el,src,pos,instant,vid){const old=el.querySelector(':scope>:not(.out)');const key=vid||src;if(old&&old.dataset.k===key)return;const rc=el.getBoundingClientRect(),off=!(rc.width&&rc.bottom>-200&&rc.top<innerHeight+200);
 let im;if(vid){im=document.createElement('video');Object.assign(im,{muted:true,loop:true,autoplay:true,playsInline:true,poster:src});im.setAttribute('muted','');im.setAttribute('playsinline','');im.preload='auto';im.src=vid}else{im=new Image();if(off){im.loading='lazy';instant=true}im.src=src;im.alt=''}
 im.dataset.k=key;if(!instant)im.classList.add('out');if(pos)im.style.objectPosition=pos;el.appendChild(im);
 if(instant){if(old)old.remove();if(vid)im.play().catch(()=>{});return}
 const show=()=>requestAnimationFrame(()=>requestAnimationFrame(()=>{im.classList.remove('out');if(vid)im.play().catch(()=>{});if(old){old.classList.add('out');setTimeout(()=>old.remove(),900)}}));
 if(vid){im.readyState>=2?show():(im.onloadeddata=show,setTimeout(show,1500))}else im.complete?show():im.onload=show}
// grille des heures : la case d'aujourd'hui (heure de Montréal) s'allume
try{const DN=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(new Date().toLocaleDateString('en-US',{weekday:'short',timeZone:'America/Toronto'}));document.querySelectorAll('.hgrid li[data-d="'+DN+'"]').forEach(e=>e.classList.add('now'))}catch(e){}
const NC=navigator.connection,LITE=!!(NC&&(NC.saveData||/2g|3g/.test(NC.effectiveType||''))),RM=matchMedia('(prefers-reduced-motion:reduce)').matches;let READY=false;const VOK=()=>READY&&!RM&&!LITE;
Object.keys(SETS).forEach(p=>{const items=SETS[p];let idx=0;
 const S=i=>[...document.querySelectorAll(`.slot[data-pg="${p}"][data-slot="${i}"]`)];
 document.querySelectorAll(`.bars[data-pg="${p}"]`).forEach(bars=>SEGS.forEach((s,i)=>{const b=document.createElement('button');b.style.left=(s[0]-1257)+'px';b.style.width=(s[1]-s[0])+'px';b.setAttribute('aria-label',(lang==='en'?'Go to image ':'Aller à l’image ')+(i+1));b.innerHTML='<i></i>';b.onclick=()=>go(i);bars.appendChild(b)}));
 function render(instant){const n=items.length;S(0).forEach(el=>{put(el,items[idx].m,null,instant,VOK()&&curPage===p&&el.getClientRects().length?items[idx].v:null);el.setAttribute('role','img');el.setAttribute('aria-label',T(items[idx].a||items[idx].n))});
  S(1).forEach(el=>put(el,items[(idx+1)%n].t,items[(idx+1)%n].tp,instant));S(2).forEach(el=>put(el,items[(idx+2)%n].t,items[(idx+2)%n].tp,instant));
  document.querySelectorAll(`[data-count="${p}"]`).forEach(c=>c.textContent=String(idx+1).padStart(2,'0'));
  document.querySelectorAll(`.bars[data-pg="${p}"]`).forEach(bars=>[...bars.children].forEach((x,i)=>x.setAttribute('aria-current',i===idx)))}
 const AUTO=p==='accueil'&&!matchMedia('(prefers-reduced-motion:reduce)').matches;let timer=0;
 let paused=false;const PPS=[...document.querySelectorAll(`.pp[data-pg="${p}"]`)];PPS.forEach(b=>{b.hidden=!AUTO;b.onclick=()=>{paused=!paused;PPS.forEach(x=>{x.dataset.on=paused?0:1;x.setAttribute('aria-label',T(paused?'Relancer le carrousel':'Mettre le carrousel en pause'))});paused?clearInterval(timer):arm()}});
 function arm(){if(!AUTO)return;clearInterval(timer);if(paused)return;timer=setInterval(()=>{if(document.hidden||curPage!==p)return;go(idx+1,true)},1500)}
 function go(i,auto){idx=(i+items.length)%items.length;render();if(!auto)arm()}
 document.querySelectorAll(`.prev[data-pg="${p}"]`).forEach(b=>b.onclick=()=>go(idx-1));document.querySelectorAll(`.next[data-pg="${p}"]`).forEach(b=>b.onclick=()=>go(idx+1));
 S(1).forEach(el=>el.onclick=()=>go(idx+1));S(2).forEach(el=>el.onclick=()=>go(idx+2));
 S(0).forEach(el=>el.onclick=()=>{if(p==='realisations')openLB(items[idx])});
 document.querySelectorAll(`#p-${p},#m-${p}`).forEach(sec=>{let sx=null;sec.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});sec.addEventListener('touchend',e=>{if(sx==null)return;const d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>50&&e.target.closest('.crop'))go(idx+(d<0?1:-1));sx=null})});
 addEventListener('keydown',e=>{if(curPage!==p||e.target.closest('input,textarea'))return;if(e.key==='ArrowRight')go(idx+1);if(e.key==='ArrowLeft')go(idx-1)});
 CARS[p]={cur:()=>items[idx]};CARS[p].render=render;CARS[p].arm=arm;render(true)});
function vidsGo(){if(READY)return;READY=true;CARS.accueil.arm();setTimeout(allPlates,LITE?15000:1800);if(!VOK())return;Object.values(CARS).forEach(c=>c.render());
 const list=SETS.accueil.filter(x=>x.v).map(x=>x.v);let i=0;CARS.accueil.pre=[];(function next(){if(i>=list.length)return;const v=document.createElement('video');v.muted=true;v.preload='auto';let done=false;const go=()=>{if(done)return;done=true;next()};v.oncanplaythrough=go;v.onerror=go;setTimeout(go,4000);v.src=list[i++];CARS.accueil.pre.push(v)})()}
if(document.readyState==='complete')setTimeout(vidsGo,0);else addEventListener('load',()=>setTimeout(vidsGo,300));
const lb=document.createElement('div');lb.className='lb';lb.hidden=true;lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.innerHTML='<figure><img alt=""><figcaption></figcaption></figure><button aria-label="Fermer">×</button>';document.body.appendChild(lb);
let lastF;function openLB(it){lastF=document.activeElement;lb.querySelector('img').src=it.big||it.m;lb.querySelector('img').alt=T(it.a||it.n);lb.querySelector('figcaption').textContent=it.n.toUpperCase();lb.hidden=false;lb.querySelector('button').focus()}
function closeLB(){lb.hidden=true;lastF&&lastF.focus()}lb.onclick=e=>{if(e.target===lb||e.target.tagName==='BUTTON')closeLB()};addEventListener('keydown',e=>{if(e.key==='Escape'&&!lb.hidden)closeLB()});
document.querySelectorAll('#realisations-voir-hit,[data-voir]').forEach(v=>v.addEventListener('click',e=>{e.preventDefault();openLB(CARS.realisations.cur())}));
const band=document.getElementById('cat-band');if(band){const ROWS=%ROWS%;let act=0;const vfw=document.getElementById('cat-vf');const mv=r=>{band.style.transform=vfw.style.transform='translateY('+(ROWS[r]-ROWS[0])+'px)';document.querySelectorAll('[data-suprow]').forEach(t=>t.toggleAttribute('data-fixed',+t.dataset.suprow===r))};
 document.querySelectorAll('.sup').forEach(a=>{a.addEventListener('mouseenter',()=>mv(+a.dataset.row));a.addEventListener('focus',()=>mv(+a.dataset.row));
  a.addEventListener('click',e=>{act=+a.dataset.row;if(a.target)return;e.preventDefault();toast('Lien bientôt disponible.')})});
 document.getElementById('p-catalogue').querySelector('.ui').addEventListener('mouseleave',()=>mv(act))}
document.querySelectorAll('.msup a').forEach(a=>a.addEventListener('click',e=>{document.querySelectorAll('.msup a').forEach(x=>x.classList.toggle('on',x===a));if(a.target)return;e.preventDefault();toast('Lien bientôt disponible.')}));
const SENT=new URLSearchParams(location.search).has('envoye');if(SENT)history.replaceState(null,'',location.pathname+location.hash);
addEventListener('pageshow',e=>{if(e.persisted)document.querySelectorAll('.qform [type=submit]').forEach(b=>b.disabled=false)});
function initForm(form,fname,fhint,ok){const ko=ok.nextElementSibling;const MSG={nom:'Indiquez votre nom',courriel:'Courriel invalide',projet:'Décrivez votre projet',qte:'Nombre entier ≥ 1'};
 const F=n=>form.querySelector(`[name="${n}"]`),ERR=n=>form.querySelector(`[data-err="${n}"]`)||document.querySelector(`#e-${n}`);
 const fl=F('fichier');const ft=[fname.textContent,fhint.textContent];const N=['nom','courriel','projet','qte'];
 function chk(n,show){const el=F(n);let bad=false;const v=el.value.trim();
  if(n==='nom')bad=!v;if(n==='courriel')bad=!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);if(n==='projet')bad=!v;if(n==='qte')bad=v!==''&&!(/^\d+$/.test(v)&&+v>=1);
  if(show){el.closest('.fld,.mf').classList.toggle('bad',bad);ERR(n).textContent=bad?T(MSG[n]):'';el.setAttribute('aria-invalid',bad)}return !bad}
 N.forEach(n=>{const el=F(n);el.addEventListener('blur',()=>{if(el.value)chk(n,true)});el.addEventListener('input',()=>{if(el.closest('.fld,.mf').classList.contains('bad'))chk(n,true)})});
 function chkFile(){const e=ERR('fichier');const f=fl.files[0];e.textContent='';if(!f){fname.textContent=T(ft[0]);fhint.textContent=T(ft[1]);return true}
  if(!/\.(jpe?g|png|pdf)$/i.test(f.name)){fl.value='';chkFile();e.textContent=T('Format non accepté : JPG, PNG ou PDF');return false}
  if(f.size>10000000){fl.value='';chkFile();e.textContent=T('Fichier trop lourd (max 10 Mo)');return false}
  fname.textContent=f.name.length>34?f.name.slice(0,31)+'…':f.name;fhint.textContent=(f.size/1e6).toFixed(1).replace('.',',')+T(' Mo — toucher pour changer');return true}
 fl.addEventListener('change',chkFile);
 form.addEventListener('submit',async e=>{e.preventDefault();const r=N.map(n=>chk(n,true));if(r.includes(false)){F(N[r.indexOf(false)]).focus();return}
  const btn=form.querySelector('[type=submit]');btn.disabled=true;toast('Envoi en cours…');
  if(form.dataset.send){form.querySelector('[name=_next]').value=location.origin+location.pathname+'?envoye=1'+hashFor('contact');form.querySelector('[name=_replyto]').value=F('courriel').value.trim();form.submit();return}
  let sent=false;try{const ac=new AbortController(),to=setTimeout(()=>ac.abort(),20000);const res=await fetch('/api/demandes',{method:'POST',body:new FormData(form),signal:ac.signal});clearTimeout(to);if(!res.ok)throw 0;sent=true;
   let ref='';try{ref=(await res.json()).reference||''}catch(_){}ok.querySelector('.ref').textContent=ref?T('Référence : ')+ref:''}catch(_){}
  btn.disabled=false;form.hidden=true;toastEl.classList.remove('on');const show=el=>{el.hidden=false;el.focus({preventScroll:true});if(isM())el.scrollIntoView({block:'start'})};if(sent){show(ok)}else{
   const v=n=>F(n).value.trim();const body=[T('Nom')+' : '+v('nom'),T('Courriel')+' : '+v('courriel'),T('Quantité approximative')+' : '+(v('qte')||'—'),'',v('projet')].join('\n');
   const bm=ko.querySelector('.bymail');if(bm.dataset.mail)bm.href='mailto:'+bm.dataset.mail+'?subject='+encodeURIComponent(T('Demande de devis')+' — '+v('nom'))+'&body='+encodeURIComponent(body);show(ko)}});
 if(SENT){form.hidden=true;ok.hidden=false}
 ok.querySelector('.again').onclick=()=>{form.reset();chkFile();form.hidden=false;ok.hidden=true;F('nom').focus()};
 ko.querySelector('.retry').onclick=()=>{form.hidden=false;ko.hidden=true;form.querySelector('[type=submit]').focus()}}
const dform=document.getElementById('devis');if(dform)initForm(dform,document.getElementById('contact-filelabel'),document.getElementById('contact-filehint'),document.getElementById('ok'));
document.querySelectorAll('.mobile .qform').forEach(f=>{const pb=f.closest('.pbody');initForm(f,f.querySelector('[data-fl]'),f.querySelector('[data-fh]'),pb.querySelector('.ok'))});
(async()=>{try{if(!('indexedDB' in window))return;const db=await new Promise((ok,ko)=>{const r=indexedDB.open('em-visions',1);r.onupgradeneeded=()=>r.result.createObjectStore('kv');r.onsuccess=()=>ok(r.result);r.onerror=()=>ko()});
 const rec=await new Promise(ok=>{const q=db.transaction('kv').objectStore('kv').get('maquette');q.onsuccess=()=>ok(q.result);q.onerror=()=>ok(null)});if(!rec||Date.now()-rec.at>36e5)return;
 document.querySelectorAll('form.qform').forEach(f=>{const fl=f.querySelector('[name=fichier]'),dt=new DataTransfer();dt.items.add(new File([rec.snap],rec.snapName,{type:'image/jpeg'}));fl.files=dt.files;fl.dispatchEvent(new Event('change',{bubbles:true}));
  (rec.orig||[]).slice(0,2).forEach((o,i)=>{const nm='visuel_original'+(i?'_2':'');let h=f.querySelector('[name='+nm+']');if(!h){h=document.createElement('input');h.type='file';h.name=nm;h.hidden=true;f.appendChild(h)}const d2=new DataTransfer();d2.items.add(new File([o.blob],o.name,{type:o.type}));h.files=d2.files});
  const pj=f.querySelector('[name=projet]');if(!pj.value.includes(rec.summary))pj.value=(pj.value?pj.value+'\n':'')+rec.summary+'\n';pj.dispatchEvent(new Event('input',{bubbles:true}))});
 db.transaction('kv','readwrite').objectStore('kv').delete('maquette');toast('Maquette 3D ajoutée à votre demande.')}catch(_){}})();
function fitCrops(){document.querySelectorAll('.crop').forEach(c=>{if(!c.offsetWidth)return;const k=c.offsetWidth/+c.dataset.w;c.firstElementChild.style.transform=`scale(${k}) translate(${-c.dataset.x0}px,${-c.dataset.y0}px)`})}
addEventListener('resize',()=>{fitCrops();setActive(curPage,true);if(CARS[curPage]&&CARS[curPage].render)CARS[curPage].render()});fitCrops();document.fonts.ready.then(()=>{collect();route(false)});
const LIGHT=%LIGHT%;
document.querySelectorAll('[data-plate]').forEach(i=>{if(!i.dataset.dark)i.dataset.dark=i.getAttribute('src')});
function loadPlate(i){if(!i.dataset.defer)return;delete i.dataset.defer;i.src=i.dataset.want||i.dataset.dark}
const pio='IntersectionObserver' in window?new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){loadPlate(e.target);pio.unobserve(e.target)}}),{rootMargin:'300px 0px'}):null;
document.querySelectorAll('img[data-defer]').forEach(i=>pio?pio.observe(i):loadPlate(i));
function loadPage(p){document.querySelectorAll('#p-'+p+' img[data-defer],#m-'+p+' img[data-defer]').forEach(i=>{if(i.getClientRects().length)loadPlate(i)})}
function allPlates(){document.querySelectorAll('img[data-defer]').forEach(i=>{if(i.getClientRects().length)loadPlate(i)});document.documentElement.classList.add('rdy')}
function setTheme(t,save){document.documentElement.dataset.theme=t;const L=t==='light';
 document.querySelectorAll('source[data-th]').forEach(x=>x.media=L?'all':'not all');
 document.querySelectorAll('[data-plate]').forEach(i=>{const s=L?LIGHT[i.dataset.plate]:i.dataset.dark;if(i.dataset.defer){i.dataset.want=s;return}if(i.getAttribute('src')!==s)i.src=s});
 document.querySelectorAll('.theme-toggle,.mtheme').forEach(b=>{b.setAttribute('aria-pressed',!L)});
 if(REC)apply();
 if(save){try{localStorage.setItem('em-theme',t)}catch(e){}toast(L?(lang==='en'?'Light theme':'Thème clair'):(lang==='en'?'Dark theme':'Thème sombre'))}}
document.querySelectorAll('.theme-toggle,.mtheme').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();setTheme(document.documentElement.dataset.theme==='light'?'dark':'light',true)}));
setTheme(document.documentElement.dataset.theme||'dark');
const TEARS=[...document.querySelectorAll('.tear')];TEARS.forEach(t=>{t._c=0;t._g=0});let tearRun=0;
function tearTargets(){const H=innerHeight;TEARS.forEach(t=>{if(!t.getClientRects().length){t._g=t._c;return}const r=t.getBoundingClientRect(),c=r.top+Math.min(r.height,H)*0.3;t._g=Math.min(1,Math.max(0,(H*0.95-c)/(H*0.5)))});if(!tearRun)tearRun=requestAnimationFrame(tearStep)}
function tearStep(){tearRun=0;let moving=false;TEARS.forEach(t=>{const d=t._g-t._c;if(Math.abs(d)>0.002){t._c+=d*0.085;moving=true}else t._c=t._g;
 const e=t._c<.5?2*t._c*t._c:1-Math.pow(-2*t._c+2,2)/2;t.style.setProperty('--p',e.toFixed(4));t.classList.toggle('gone',t._c>0.995)});if(moving)tearRun=requestAnimationFrame(tearStep)}
addEventListener('scroll',tearTargets,{passive:true});addEventListener('resize',tearTargets);
setTimeout(tearTargets,450);
const burger=document.querySelector('.burger'),mnav=document.getElementById('mnav');
function menu(open){burger.setAttribute('aria-expanded',open);burger.setAttribute('aria-label',T(open?'Fermer le menu':'Ouvrir le menu'));mnav.hidden=!open;document.body.style.overflow=open?'hidden':''}
burger.onclick=()=>menu(mnav.hidden);mnav.addEventListener('click',e=>{if(e.target.closest('a[href^="#"]:not([data-toast])'))menu(false)});
addEventListener('keydown',e=>{if(e.key==='Escape'&&!mnav.hidden){menu(false);burger.focus()}});
// Videos: start each framed video when it comes into view, and retry on the first tap for browsers that block autoplay.
const inView=v=>{const r=v.getBoundingClientRect();return r.width>0&&r.bottom>0&&r.top<innerHeight};
const playV=v=>{if(v.dataset.poster&&!v.getAttribute('poster'))v.poster=v.dataset.poster;v.muted=true;v.defaultMuted=true;v.setAttribute('playsinline','');const p=v.play();if(p)p.catch(()=>{})};
if('IntersectionObserver' in window){const vo=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)playV(e.target);else e.target.pause()}),{rootMargin:'300px 0px',threshold:0});document.querySelectorAll('.vclip video').forEach(v=>vo.observe(v))}else document.querySelectorAll('.vclip video').forEach(playV)
const kick=()=>document.querySelectorAll('video').forEach(v=>{if(v.paused&&inView(v))playV(v)});
['pointerdown','touchend','keydown','scroll'].forEach(ev=>addEventListener(ev,kick,{passive:true}));
'''
SEO={'fr':{'path':'/','locale':'fr_CA','title':'EM Visions — Vêtements et objets personnalisés à Saint-Léonard, Montréal',
           'desc':'Atelier à Saint-Léonard (Montréal) : vêtements et objets personnalisés, impression, design graphique, impression 3D et sites web. Demandez un devis.',
           'alt':'Page d’accueil EM Visions : « Faites bonne impression »'},
     'en':{'path':'/en/','locale':'en_CA','title':'EM Visions — Custom apparel and objects in Saint-Léonard, Montréal',
           'desc':'Workshop in Saint-Léonard (Montréal): custom apparel and objects, printing, graphic design, 3D printing and websites. Request a quote.',
           'alt':'EM Visions home page: “Make a good impression”'}}
def head_seo(L):
    m=SEO[L]; o=SEO['en' if L=='fr' else 'fr']; e=H.escape; up='' if L=='fr' else '../'
    ld={'@context':'https://schema.org','@type':'LocalBusiness','@id':SITE_URL+'/#atelier','name':'EM Visions','alternateName':'EM Custom Design','description':m['desc'],
        'url':SITE_URL+m['path'],'image':SITE_URL+'/img/og.jpg','logo':SITE_URL+'/img/icon-512.png',**({'email':CONTACT_EMAIL} if CONTACT_EMAIL else {}),
        'address':{'@type':'PostalAddress','streetAddress':'5825, rue Jean-Talon Est','addressLocality':'Saint-Léonard','addressRegion':'QC','postalCode':'H1S 1M4','addressCountry':'CA'},
        'areaServed':'Montréal','sameAs':[INSTAGRAM],**({'openingHoursSpecification':[{'@type':'OpeningHoursSpecification','dayOfWeek':d,'opens':a,'closes':b} for d,a,b in HOURS]} if HOURS else {})}
    return (f'<title>{e(m["title"])}</title><meta name="description" content="{e(m["desc"])}">'
      f'<link rel="canonical" href="{SITE_URL}{m["path"]}"><link rel="alternate" hreflang="fr-CA" href="{SITE_URL}/"><link rel="alternate" hreflang="en-CA" href="{SITE_URL}/en/"><link rel="alternate" hreflang="x-default" href="{SITE_URL}/">'
      f'<meta property="og:type" content="website"><meta property="og:site_name" content="EM Visions"><meta property="og:title" content="{e(m["title"])}"><meta property="og:description" content="{e(m["desc"])}">'
      f'<meta property="og:url" content="{SITE_URL}{m["path"]}"><meta property="og:locale" content="{m["locale"]}"><meta property="og:locale:alternate" content="{o["locale"]}">'
      f'<meta property="og:image" content="{SITE_URL}/img/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(m["alt"])}">'
      f'<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#0a0a0a">'
      f'<link rel="icon" href="{up}img/favicon.svg" type="image/svg+xml"><link rel="icon" href="{up}img/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="{up}img/apple-touch-icon.png">'
      f'<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>')
HEADJS='(function(){let t;try{t=localStorage.getItem("em-theme")}catch(e){}if(t!=="light"&&t!=="dark")t=matchMedia("(prefers-color-scheme: light)").matches?"light":"dark";document.documentElement.dataset.theme=t})()'
import loader; HEADJS+=';'+loader.HEAD
sections=''.join(f'<section class="page" id="p-{p}" aria-label="{TITLES["fr"][p]}" style="top:{HH+i*SH}px;height:{SH}px">\n{page_html(p)}\n</section>\n' for i,p in enumerate(ORDER))
js=JS.replace('%VIDS%',json.dumps(VIDS)).replace('%LIGHT%',json.dumps({**{p:f'img/plate-{p}-light.webp' for p in ORDER},'mtop':'img/m-paper-top-light.webp','mbot':'img/m-paper-bot-light.webp','head':'img/head-light.webp'})).replace('%PAGES%',json.dumps(ORDER)).replace('%EN%',json.dumps(EN,ensure_ascii=False)).replace('%SLUG%',json.dumps(SLUG)).replace('%TITLES%',json.dumps(TITLES,ensure_ascii=False)).replace('%TOAST%',json.dumps(TOAST,ensure_ascii=False)).replace('%ROWS%',json.dumps(META['catalogue']['rows']))
doc=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{head_seo('fr')}<script>{HEADJS}</script>
<style>{CSS}{MCSS}{CALCSS if CAL else ''}{loader.CSS}</style></head><body{' class="cal"' if CAL else ''}>
{loader.html(LOGO_VB)}
<a class="sr" href="#p-accueil">Aller au contenu</a>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><symbol id="emlogo" viewBox="{LOGO_VB}"><path fill="currentColor" fill-rule="evenodd" d="{LOGO_D}"/></symbol>
<filter id="fiber" x="-20%" y="-5%" width="140%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.09 0.6" numOctaves="2" seed="3" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="7"/></filter>
<linearGradient id="paperfill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f4f2"/><stop offset="1" stop-color="#e6e6e3"/></linearGradient>
<filter id="paperedge" x="-2%" y="-5%" width="104%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035 0.05" numOctaves="5" seed="7" result="n"/><feColorMatrix in="n" type="saturate" values="0" result="g"/>
<feComponentTransfer in="g" result="g2"><feFuncR type="linear" slope="0.42" intercept="0.7"/><feFuncG type="linear" slope="0.42" intercept="0.7"/><feFuncB type="linear" slope="0.42" intercept="0.7"/></feComponentTransfer>
<feComposite in="g2" in2="SourceAlpha" operator="in" result="gi"/><feBlend in="SourceGraphic" in2="gi" mode="multiply"/></filter></defs></svg>
{header_html()}
<div class="frame" id="frame"><div class="stage" id="stage" style="height:{HH+6*SH}px">
{sections}</div></div>
{mobile_html(EL,META,span)}
<script>{js}</script></body></html>'''
open('out/cal.html' if CAL else 'out/index.html','w').write(doc)
if not CAL:
    import en_page
    en=doc.replace('<html lang="fr">','<html lang="en">',1); assert head_seo('fr') in en
    en=en.replace(head_seo('fr'),head_seo('en'),1)
    en=en_page.translate(en,EN,SLUG)
    en=re.sub(r'''(?<=["'(=])(img|fonts|vid)/''',r'../\1/',en)
    os.makedirs('out/en',exist_ok=True); open('out/en/index.html','w').write(en)
    import pages_extra; pages_extra.write(LOGO_VB,LOGO_D)
    import maquette_page; maquette_page.write(LOGO_VB,LOGO_D)
    open('out/robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n')
    alt=''.join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{SITE_URL}{p}"/>' for h,p in (('fr-CA','/'),('en-CA','/en/'),('x-default','/')))
    alt2=''.join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{SITE_URL}{p}"/>' for h,p in (('fr-CA','/confidentialite/'),('en-CA','/en/privacy/')))
    open('out/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        +''.join(f'<url><loc>{SITE_URL}{p}</loc>{alt}</url>\n' for p in ('/','/en/'))+''.join(f'<url><loc>{SITE_URL}{p}</loc>{alt2}</url>\n' for p in ('/confidentialite/','/en/privacy/'))+''.join(f'<url><loc>{SITE_URL}{p}</loc></url>\n' for p in ('/maquette/','/en/mockup/'))+'</urlset>\n')
print('built',len(doc))
