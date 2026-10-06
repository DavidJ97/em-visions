import html as H, re, random
from config import CONTACT_EMAIL, INSTAGRAM, HOURS, HOURS_FR, ABOUT_FR, FORM_ENDPOINT, WEEK_FR
def hours_grid(cls='',style=''):
    """Les heures d'ouverture en grille : une case par jour, le jour d'aujourd'hui s'allume en bleu (script de la page)."""
    cell=lambda fr,n,s:(f'<li data-d="{n}"><b>{fr}</b><span>{s[0]}</span><span>{s[1]}</span></li>' if s else f'<li class="off" data-d="{n}"><b>{fr}</b><span>Fermé</span></li>')
    return f'<ul class="hgrid {cls}" aria-label="Heures d’ouverture"{style}>'+''.join(cell(*w) for w in WEEK_FR)+'</ul>'

def plate_img(cls,p):
    # Accueil : chargée tout de suite, en priorité, et directement dans le bon thème. Les autres : à l'approche de l'écran.
    if p=='accueil':
        return (f'<picture><source data-th srcset="img/plate-{p}-light.webp" media="(prefers-color-scheme: light)">'
                f'<img class="{cls}" data-plate="{p}" src="img/plate-{p}.webp" alt="" aria-hidden="true" draggable="false" fetchpriority="high"></picture>')
    return f'<img class="{cls}" data-plate="{p}" data-defer="1" data-dark="img/plate-{p}.webp" alt="" aria-hidden="true" draggable="false">'
def form_attrs():
    return f' action="{FORM_ENDPOINT}" method="post" enctype="multipart/form-data" data-send="1"' if FORM_ENDPOINT else ''
def form_hidden():
    if not FORM_ENDPOINT: return ''
    return ('<input type="hidden" name="_subject" value="Demande de devis — site EM Visions"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">'
            '<input type="hidden" name="_next" value=""><input type="hidden" name="_replyto" value=""><input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">')
CLOCK='<svg width="{s}" height="{s}" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.5" fill="none" stroke="{c}" stroke-width="2.2"/><path d="M12 6.5V12l3.6 2.4" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def ko_html():
    if CONTACT_EMAIL:
        note='Vos réponses sont conservées. Vous pouvez réessayer ou nous écrire directement par courriel.'
        alt=f'<a class="bymail" data-mail="{CONTACT_EMAIL}" href="mailto:{CONTACT_EMAIL}">Écrire par courriel</a>'
    else:
        note='Vos réponses sont conservées. Vous pouvez réessayer, nous écrire sur Instagram ou passer à l’atelier.'
        alt=f'<a class="bymail" href="{INSTAGRAM}" target="_blank" rel="noopener">Écrire sur Instagram</a>'
    return ('<div class="ok ko" hidden role="alert" tabindex="-1"><b>OUPS.</b><p>Votre demande n’a pas pu être envoyée.</p>'
            f'<p class="note">{note}</p><div class="okb"><button type="button" class="retry">Réessayer</button>{alt}</div></div>')
VECF=lambda p,b:''
LOGO=''
NAV=[('accueil','Accueil'),('services','Services'),('realisations','Réalisations'),('catalogue','Catalogue'),('a-propos','À propos'),('contact','Contact')]
def crop(p,x0,y0,x1,y1,inner='',cls='',plate=True,extra=''):
    pl=plate_img('cplate',p) if plate else ''
    return (f'<div class="crop {cls}" data-x0="{x0}" data-y0="{y0}" data-w="{x1-x0}" style="aspect-ratio:{x1-x0}/{y1-y0}" {extra}>'
            f'<div class="cin">{pl}{VECF(p,(x0,y0,x1,y1))}{inner}</div></div>')
def mspan(span_html):
    return re.sub(r'id="([^"]+)"',lambda m:f'id="m-{m.group(1)}"',span_html)
def slots(p,META):
    return ''.join(f'<div class="slot" data-pg="{p}" data-slot="{i}" style="left:{s[0]}px;top:{s[1]}px;width:{s[2]-s[0]}px;height:{s[3]-s[1]}px"></div>' for i,s in enumerate(META[p]['slots']))
def cta(p,EL,span,box,href,label,ext=''):
    e=[e for e in EL if e['page']==p and e['group']=='cta'][0]
    x0,y0,x1,y1=box
    return f'<a class="mcta" href="{href}"{ext} aria-label="{H.escape(label)}">'+crop(p,x0,y0,x1,y1,mspan(span(e)))+'</a>'
def h1(lines,tag='h1'):
    return f'<{tag} class="mh1">'+'<br>'.join(H.escape(l) for l in lines)+'<i class="sq" aria-hidden="true"></i></'+tag+'>'
ARR='<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h16M13 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARRL='<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12H4M11 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
DIAG='<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 18L18 6M8 6h10v10" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
# Sites des fournisseurs, dans l'ordre de la page Catalogue (à faire valider par EM).
# Eside = distributeur canadien des casquettes Flexfit ; Projob = vêtements de travail, distribués au Canada par Texet.
SUP_URL={0:'https://fr-ca.ssactivewear.com/',1:'https://canadasportswear.com/',2:'https://fabrik.ca/',3:'https://eside.ca/fr/',4:'https://www.justlikehero.com/',5:'https://texet.ca/pages/projob'}
# Logos officiels des fournisseurs, dans l'ordre de la liste : (largeur, hauteur) affichées.
# Ils sont ramenés à une seule couleur (img/logo-*.webp = silhouette) pour suivre les couleurs du site :
# blanc en thème sombre et sur la bande bleue, noir en thème clair.
SUP_LOGO={0:('ss',184,26),1:('canada',114,44),2:('fabrik',116,36),3:('eside',93,30),4:('jlh',71,52),5:('projob',152,34)}
def sup_logo(i,cls='',extra=''):
    """Logo du fournisseur, décoratif : le lien porte déjà son nom."""
    k,w,h=SUP_LOGO[i]
    return f'<i class="slogo {cls}" aria-hidden="true"{extra} style="--m:url(img/logo-{k}.webp);width:{w}px;height:{h}px"></i>'
def carctl(p):
    pp=p=='accueil'
    return (f'<div class="mctl">'+('<i class="ppsp" aria-hidden="true"></i>' if pp else '')+f'<button class="arrow prev" data-pg="{p}" aria-label="Image précédente">{ARRL}</button>'
            f'<span class="mcount"><b data-count="{p}">01</b> / 05</span>'
            f'<button class="arrow next" data-pg="{p}" aria-label="Image suivante">{ARR}</button>'+('<button class="arrow pp" data-pg="accueil" data-on="1" aria-label="Mettre le carrousel en pause"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6v12M15 6v12" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M8.5 5.5v13l10-6.5z" fill="currentColor"/></svg></button>' if pp else '')+f'</div><div class="mbars bars" data-pg="{p}"></div>')
A_BUONO='Lettrage de vitrine pour le pop-up shop Buono Bites'
def _torn(seed,inset):
    """Polygone CSS au bord irrégulier, comme du papier déchiré."""
    r=random.Random(seed); pts=[]; j=lambda:inset+r.random()*1.6
    for k in range(0,101,4): pts.append((k+ (r.random()-.5)*2 if 0<k<100 else k, j()*1.9))
    for k in range(6,95,7): pts.append((100-j(), k+(r.random()-.5)*3))
    for k in range(100,-1,-4): pts.append((k+ (r.random()-.5)*2 if 0<k<100 else k, 100-j()*1.9))
    for k in range(94,5,-7): pts.append((j(), k+(r.random()-.5)*3))
    return 'polygon('+','.join(f'{min(100,max(0,x)):.1f}% {min(100,max(0,y)):.1f}%' for x,y in pts)+')'
TORN=[(_torn(11+i,0),_torn(71+i,1.4)) for i in range(6)]
# chaque service a son illustration (img/svc-N.webp), posée en escalier : une à gauche, une à droite, en descendant.
# Chaque cadre est différent : format, largeur, inclinaison, déchirure et couleur du papier glissé dessous.
SVC=[('01','Design graphique','Des visuels qui marquent votre identité.','Illustration : une main trace au marqueur une orbite et une étoile bleues',(900,600),'88%','-1.4deg','#0a3cff','7px','8px'),
     ('02','Impression','Des supports de qualité pour vos projets.','Illustration : deux mains tirent une raclette d’encre bleue sur un cadre de sérigraphie',(720,900),'64%','1.2deg','var(--alt)','-8px','7px'),
     ('03','Vêtements personnalisés','Des textiles uniques à votre image.','Illustration : un t-shirt, une casquette et un chandail à capuchon imprimés en bleu',(800,800),'76%','-.8deg','#0a3cff','8px','-7px'),
     ('04','Impression 3D','Des idées qui prennent forme.','Illustration : la buse d’une imprimante 3D construit une pièce bleue couche par couche',(900,600),'88%','1deg','var(--alt)','-7px','-8px'),
     ('05','Sites Web','Des plateformes sur mesure pour propulser votre marque.','Illustration : une page Web en papier déchiré, un curseur clique sur un bouton bleu',(720,900),'64%','-1.6deg','#0a3cff','-8px','8px'),
     ('06','Applications','Des outils performants pour vos besoins spécifiques.','Illustration : une main tient un téléphone d’où s’échappent des icônes en papier',(800,800),'76%','1.3deg','var(--alt)','8px','8px')]
def mobile_html(EL,META,span):
    P={}
    P['accueil']=(h1(['Faites','bonne','impression'])+'<i class="rule"></i><p class="msub">Vêtements et objets personnalisés pour donner forme à vos idées.</p>'
        +cta('accueil',EL,span,(72,710,432,810),'#contact','Demander un devis')
        +crop('accueil',405,95,1586,925,slots('accueil',META),'bleed comp')+carctl('accueil'))
    P['services']=(h1(['De l’idée','à la','matière'],'h2')+'<i class="rule"></i>'
        +'<ol class="msvc">'+''.join(f'<li class="{"r" if i%2 else "l"}"><div class="ph" style="--w:{w};--ar:{sz[0]}/{sz[1]};--rot:{rot};--bk:{bk};--bx:{bx};--by:{by};--t:{TORN[i][0]};--u:{TORN[i][1]}"><em class="gn" aria-hidden="true">{n.lstrip("0")}</em><span class="im"><img src="img/svc-{i+1}.webp" alt="{H.escape(al)}" width="{sz[0]}" height="{sz[1]}" loading="lazy"><i class="cv"></i></span><s></s></div><span class="n">{n}</span><div><b>{H.escape(t)}</b><span>{H.escape(d)}</span></div></li>' for i,(n,t,d,al,sz,w,rot,bk,bx,by) in enumerate(SVC))+'</ol>'
        +cta('services',EL,span,(78,870,486,966),'#contact','Parler de mon projet'))
    P['realisations']=(h1(['Le','travail','parle'],'h2')+'<i class="rule"></i><p class="msub">Des idées devenues réelles.</p>'
        +crop('realisations',405,95,1586,925,slots('realisations',META),'bleed comp')+carctl('realisations')
        +'<a class="mcta" href="#" data-voir="1" aria-label="Voir le projet">'+crop('realisations',72,710,424,810,mspan(span([e for e in EL if e['page']=='realisations' and e['group']=='cta'][0])))+'</a>')
    sups=['S&S Activewear','Canada Sportswear','Fabrik','Eside','Just Like Hero','Projob']
    P['catalogue']=(h1(['Choisissez','votre support'],'h2')+'<i class="rule"></i><p class="msub">Des fournisseurs de confiance pour concrétiser vos idées.</p>'
        +'<ul class="msup">'+''.join(f'<li><a '+(f'href="{SUP_URL[i]}" target="_blank" rel="noopener"' if i in SUP_URL else 'href="#catalogue"')+f' class="{"on" if i==0 else ""}" data-supplier="{i}">{sup_logo(i,"m")}<b>{H.escape(s)}</b><span class="vf">Voir le fournisseur</span>{DIAG if i==0 else ARR}</a></li>' for i,s in enumerate(sups))+'</ul>'
        +'<div class="mpills"><a class="mm3d" data-m3d href="maquette/">Essayer sur un produit en 3D '+ARR+'</a><a class="mm3d prix" data-prix href="#contact">Demander les prix '+ARR+'</a></div>'
        +'<p class="mprix">Les prix ne sont pas affichés : on vous les envoie personnellement, selon votre projet.</p>'
        +crop('catalogue',630,95,1586,930,'','bleed comp'))
    P['a-propos']=(crop('a-propos',0,105,1015,935,'','bleed comp top')+h1(['Les gens','derrière','l’impression'],'h2')+'<i class="rule"></i>'
        +'<div class="mteam"><div><b>Eduardo Mazzonna</b><span>Design graphique</span></div><div><b>Vince Mariani</b><span>Gestion de projets</span></div></div>'
        +f'<p class="msub mabout">{H.escape(ABOUT_FR)}</p>')
    P['contact']=(h1(['On en','parle ?'],'h2')+'<p class="msub">Un projet, une idée, une question ? On est là pour en discuter. Écrivez-nous et on vous répond rapidement.</p><i class="rule"></i>'
        +'<address class="maddr"><svg width="30" height="38" viewBox="0 0 24 30" aria-hidden="true"><path d="M12 1.5a9 9 0 0 0-9 9c0 6.8 9 17.5 9 17.5s9-10.7 9-17.5a9 9 0 0 0-9-9z" fill="none" stroke="#0a3cff" stroke-width="2.6"/><circle cx="12" cy="10.5" r="3.3" fill="#0a3cff"/></svg><span>5825, rue Jean-Talon Est<br>Saint-Léonard, QC H1S 1M4</span></address>'
        +(hours_grid('mh') if HOURS else '')
        +'<div class="mpaper"><img class="edge etop" data-plate="mtop" src="img/m-paper-top.webp" alt="" aria-hidden="true" loading="lazy"><div class="pbody">'
        +'<h2 class="mh2">Demande de devis<i class="sq" aria-hidden="true"></i></h2>'
        +f'<form class="qform" novalidate{form_attrs()}>'+form_hidden()
        +''.join(f'<label class="mf"><span class="flab">{lab}</span>{ctl}<em class="err" data-err="{n}"></em></label>' for n,lab,ctl in [
            ('nom','Nom *','<input name="nom" type="text" autocomplete="name" maxlength="150" placeholder="Votre nom" required>'),
            ('courriel','Courriel *','<input name="courriel" type="email" autocomplete="email" inputmode="email" placeholder="votre@courriel.com" required>'),
            ('projet','Votre projet *','<textarea name="projet" rows="4" maxlength="5000" placeholder="Décrivez-nous votre projet en quelques mots..." required></textarea>'),
            ('qte','Quantité approximative','<input name="qte" type="number" min="1" inputmode="numeric" placeholder="Ex. : 50, 100, 500, etc.">')])
        +'<div class="mf"><span class="flab">Joindre un visuel</span><label class="mfile"><input type="file" name="fichier" accept=".jpg,.jpeg,.png,.pdf,image/jpeg,image/png,application/pdf">'
        +'<svg width="22" height="26" viewBox="0 0 24 24" aria-hidden="true"><path d="M16.5 6.5l-8 8a2.5 2.5 0 0 0 3.5 3.5l8.5-8.5a4.5 4.5 0 0 0-6.4-6.4L5.6 11.6a6.5 6.5 0 0 0 9.2 9.2L20 15.5" fill="none" stroke="#222" stroke-width="1.6" stroke-linecap="round"/></svg>'
        +'<span><b data-fl>Choisir un fichier</b><small data-fh>JPG, PNG, PDF (max 10 Mo)</small></span></label><em class="err" data-err="fichier"></em><a class="mm3dl" data-m3d href="maquette/">ou créer une maquette 3D</a></div>'
        +'<button type="submit" class="msubmit">Demander un devis '+ARR+'</button>'
        +'<p class="legal">En soumettant ce formulaire, vous nous permettez de vous contacter concernant votre demande.<br><a data-privacy href="confidentialite/">Politique de confidentialité</a></p></form>'
        +'<div class="ok" hidden role="status" tabindex="-1"><b>MERCI.</b><p>Votre demande est bien envoyée.</p><p class="note">Nous vous répondrons par courriel.</p><p class="note ref"></p><button type="button" class="again">Nouvelle demande</button></div>'+ko_html()+''
        +'</div><img class="edge ebot" data-plate="mbot" src="img/m-paper-bot.webp" alt="" aria-hidden="true" loading="lazy"></div>'
        +crop('contact',435,112,875,592,'','bleed comp')
        +'<div class="mmap">'+crop('contact',35,592,865,930,mspan(span([e for e in EL if e['page']=='contact' and e['text']=='Itinéraire'][0]))+'<a class="mitin" href="https://goo.gl/maps/oVVn3rjDxX8nbqMw5" target="_blank" rel="noopener" aria-label="Itinéraire (Google Maps)"></a>','bleed comp')+'</div>')
    out=['<div class="mobile" id="mobile">',
        '<header class="mhead"><a href="#accueil" class="mlogo" aria-label="EM Visions — accueil">'+LOGO+'</a>',
        '<button class="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="mnav"><i></i><i></i><i></i></button></header>',
        '<nav class="mnav" id="mnav" aria-label="Navigation principale" hidden><div class="mnav-in">'+''.join(f'<a href="#{k}" data-nav="{k}">{H.escape(v)}</a>' for k,v in NAV)
        +'<div class="mnav-foot"><span class="lang"><a href="#accueil" class="mlang-fr" hreflang="fr" lang="fr">FR</a><i></i><a href="en/#home" class="mlang-en" hreflang="en" lang="en">EN</a></span>'
        +'<button class="mtheme" aria-label="Mode sombre" aria-pressed="true"><svg viewBox="0 0 59 59" width="52" height="52" aria-hidden="true"><circle cx="29.5" cy="29.5" r="22.3" fill="none" stroke="#0a3cff" stroke-width="2.6"/><path d="M32.4 19.2a10.6 10.6 0 1 0 6.9 17.2 8.6 8.6 0 0 1-6.9-17.2z" fill="currentColor"/></svg></button></div></div></nav>']
    for k,_ in NAV: out.append(f'<section class="mpage" id="m-{k}" aria-label="{k}">{P[k]}</section>')
    out.append('<footer class="mfoot">'+LOGO.replace('logo-svg','logo-svg flogo')+'<p>5825, rue Jean-Talon Est, Saint-Léonard</p>'+(f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>' if CONTACT_EMAIL else '')+f'<a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a><a data-privacy href="confidentialite/">Politique de confidentialité</a></footer></div>')
    return '\n'.join(out)
MCSS='''
@media (max-width:1024px){
 html[data-theme=light] body{background:#e9e9e6 url(img/tex-light.webp) repeat;background-size:256px;color:#141414}
 html[data-theme=light] .mhead{background:linear-gradient(#e9e9e6 calc(100% - 16px),#e9e9e600)}
 html[data-theme=light] .burger i{background:#141414}
 html[data-theme=light] .mnav{background:#e9e9e6 url(img/tex-light.webp)}
 html[data-theme=light] .mnav-in>a,html[data-theme=light] .mh1{color:#141414}
 html[data-theme=light] .lang i{background:#141414}html[data-theme=light] .mtheme{color:#141414}
 html[data-theme=light] .msvc div span{color:#333}
 html[data-theme=light] .msup a{border-left-color:#555;border-bottom-color:#aaa}html[data-theme=light] .msup a.on{border-color:transparent}
 html[data-theme=light] .mteam div+div{border-color:#141414}
 html[data-theme=light] .mctl .arrow{border-color:#141414;color:#141414}html[data-theme=light] .mfoot{color:#555;border-color:#ccc}
 html[data-theme=light] .mfoot a{color:#141414}
 html[data-theme=light] .mcta .vsvg{filter:drop-shadow(0 3px 5px #0004)}
}
.mobile{display:none}
@media (max-width:1024px){
 .frame{display:none}.mobile{display:block}
 body{background:#070707 url(img/tex.webp) repeat;background-size:256px;color:#f4f4f2;font-family:Archivo,sans-serif}
 .mhead{position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center;padding:14px 20px 22px;background:linear-gradient(#070707 calc(100% - 16px),#07070700)}
 .mlogo{color:var(--fg,#fff);display:block}.logo-svg{height:52px;width:auto;display:block;color:inherit}.flogo{height:64px;color:var(--fg)}
 .burger{width:52px;height:52px;border:2.6px solid #0a3cff;border-radius:50%;background:none;display:grid;place-content:center;gap:5px;cursor:pointer}
 .burger i{display:block;width:20px;height:2px;background:#fff;transition:.25s}
 .burger[aria-expanded=true] i:nth-child(1){transform:translateY(7px) rotate(45deg)}.burger[aria-expanded=true] i:nth-child(2){opacity:0}.burger[aria-expanded=true] i:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
 .mnav{position:fixed;inset:0;z-index:15;background:#070707 url(img/tex.webp);padding:100px 28px 32px;display:flex}.mnav[hidden]{display:none}
 .mnav-in{display:flex;flex-direction:column;gap:6px;width:100%}
 .mnav-in>a{font:900 extra-condensed clamp(46px,12.6vw,74px)/1.08 Archivo,sans-serif;word-spacing:.08em;text-transform:uppercase;letter-spacing:-.01em;color:#f4f4f2;-webkit-text-stroke:1px currentColor;padding:2px 0;width:max-content}
 .mnav-in>a[aria-current=page]{box-shadow:inset 0 -7px 0 #0a3cff}
 .mnav-foot{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font:700 16px Archivo,sans-serif;letter-spacing:.06em}
 .lang{display:flex;gap:14px;align-items:center}.lang i{width:2px;height:20px;background:#fff}html[lang=fr] .mlang-fr,html[lang=en] .mlang-en{color:#0a3cff}
 .mtheme{width:52px;height:52px;border:0;padding:0;border-radius:50%;background:none;display:grid;place-items:center;color:#fff;cursor:pointer}
 .mpage{display:block;position:relative;padding:10px 20px 56px;max-width:760px;margin:0 auto;scroll-margin-top:80px}.mpage+.mpage{border-top:1px solid #ffffff14;padding-top:34px}
 @keyframes mfade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
 .mh1{position:relative;isolation:isolate;font:400 clamp(26px,7.9vw,58px)/1.16 Sekuya,Archivo,sans-serif;word-spacing:0;text-transform:uppercase;letter-spacing:.05em;color:#f6f6f4;margin:18px 0 0}
 .mh1::before{content:'';position:absolute;z-index:-1;left:30%;right:-70px;top:-45%;bottom:-55%;background:url(img/ink0.webp) 60% 50%/contain no-repeat;pointer-events:none}
 .rdy #m-services .mh1::before,.rdy #m-a-propos .mh1::before{background-image:url(img/ink1.webp)}
 .rdy #m-realisations .mh1::before,.rdy #m-contact .mh1::before{background-image:url(img/ink2.webp)}
 #m-catalogue .mh1::before{left:42%;top:-35%;bottom:-25%}
 .mh1 .sq,.mh2 .sq{display:inline-block;width:.2em;height:.22em;background:#0a3cff;margin-left:.06em;-webkit-text-stroke:0}
 .rule{display:block;width:64px;height:6px;background:#0a3cff;margin:22px 0 18px}
 .mabout{max-width:none!important;margin-top:22px;font-size:clamp(16px,4.3vw,19px)!important;line-height:1.5!important}
 .msub{font-weight:300;font-size:clamp(18px,4.8vw,23px);line-height:1.4;max-width:30ch;letter-spacing:.01em}
 .mcta{display:block;width:min(100%,360px);margin:26px 0 8px}.mcta:active{transform:scale(.98)}
 .crop{position:relative;overflow:hidden;width:100%}.cin{position:absolute;left:0;top:0;width:1586px;height:992px;transform-origin:0 0}
 .cin .cplate{position:absolute;left:0;top:0;width:1586px;height:992px;z-index:2;pointer-events:none}
 .cin .slot{position:absolute;z-index:1}.cin .tear{z-index:3}.cin .vsvg{z-index:3}.cin .t{z-index:4}
 .bleed{width:calc(100% + 40px);margin-left:-20px}.comp{margin-top:26px}.comp.top{margin-top:0}
 .mctl{display:flex;justify-content:center;align-items:center;gap:28px;margin-top:6px}
 .mctl .arrow.pp,.mctl .ppsp{width:38px;height:38px;flex:none}.mctl:has(.pp){gap:20px}
 .mctl .arrow{width:48px;height:48px;border-radius:50%;border:2px solid #fff;background:none;color:#fff;display:grid;place-items:center;cursor:pointer}
 .mcount{font:400 18px Archivo,sans-serif;min-width:70px;text-align:center}.mcount b{font-weight:700}
 .mbars{position:relative;left:auto;top:auto;width:233px;height:16px;margin:10px auto 0}
 .msvc{--alt:#f4f4f2;--ln:#f4f4f2;list-style:none;display:grid;gap:46px;margin:22px 0 14px}
 html[data-theme=light] .msvc{--alt:#0a0a0a;--ln:#141414}
 .msvc li{display:grid;grid-template-columns:auto 1fr;column-gap:16px;row-gap:20px;align-items:start;align-content:start}
 .msvc li.r{grid-template-columns:1fr auto}
 .msvc .ph{grid-column:1/-1;position:relative;width:var(--w);aspect-ratio:var(--ar);transform:rotate(var(--rot));margin-left:-8px}
 .msvc li.r .ph{justify-self:end;margin:0 -8px 0 0}
 .msvc .ph::before{content:"";position:absolute;inset:0;background:var(--bk);clip-path:var(--t);transform:translate(var(--bx),var(--by))}
 .msvc .im{position:absolute;inset:0;overflow:hidden;clip-path:var(--u)}.msvc .im img{width:100%;height:100%;object-fit:cover;display:block}
 /* mouvement : chaque image arrive comme une impression (feuille blanche, passage de raclette, numéro tamponné) */
 .msvc{margin-inline:-20px;padding-inline:20px;overflow-x:clip}
 .msvc .cv{position:absolute;inset:0;background:#f1efe9;display:none}.msvc .ph>s{position:absolute;top:-4%;bottom:-4%;left:0;width:8px;margin-left:-4px;background:#0a3cff;opacity:0;pointer-events:none}
 .msvc .gn{position:absolute;z-index:-1;top:50%;left:min(94%,calc(100vw - 44px - .44em));font:900 extra-condensed 52.9vw/.8 Archivo,sans-serif;word-spacing:.08em;font-style:normal;color:transparent;-webkit-text-stroke:2px #0a3cff;transform:translateY(-50%);white-space:nowrap;pointer-events:none}
 .msvc li.r .gn{left:auto;right:min(94%,calc(100vw - 44px - .44em))}
 .msvc.anim .cv{display:block}
 .msvc.anim .ph{transition:opacity .45s,transform .7s cubic-bezier(.2,1.25,.3,1)}.msvc.anim .ph::before{transition:transform .75s cubic-bezier(.2,1.5,.3,1) .3s,opacity .3s .3s}
 .msvc.anim .n{transition:transform .4s cubic-bezier(.2,1.7,.4,1) .6s,opacity .2s .6s}.msvc.anim li>div:last-child{transition:transform .5s .68s,opacity .5s .68s}
 .msvc.anim .gn{transition:opacity .8s .2s}
 .msvc.anim li:not(.in) .ph{opacity:0;transform:rotate(calc(var(--rot)*4)) translateY(46px) scale(.9)}
 .msvc.anim li:not(.in) .ph::before{opacity:0;transform:translate(calc(var(--bx)*-6),calc(var(--by)*6)) rotate(-9deg)}
 .msvc.anim li:not(.in) .n{opacity:0;transform:scale(2.4) rotate(9deg)}.msvc.anim li:not(.in)>div:last-child{opacity:0;transform:translateY(18px)}.msvc.anim li:not(.in) .gn{opacity:0}
 .msvc.anim li.in .cv{animation:svcv .62s cubic-bezier(.62,0,.25,1) .22s both}.msvc.anim li.in .ph>s{animation:svsq .62s cubic-bezier(.62,0,.25,1) .22s both}
 .msvc.anim li.r.in .cv{animation-name:svcvr}.msvc.anim li.r.in .ph>s{animation-name:svsqr}
 @keyframes svcv{from{clip-path:inset(0 0 0 0)}to{clip-path:inset(0 0 0 100%)}}@keyframes svcvr{from{clip-path:inset(0 0 0 0)}to{clip-path:inset(0 100% 0 0)}}
 @keyframes svsq{0%{left:0;opacity:1}90%{left:100%;opacity:1}100%{left:100%;opacity:0}}@keyframes svsqr{0%{left:100%;opacity:1}90%{left:0;opacity:1}100%{left:0;opacity:0}}
 @supports (animation-timeline:view()){
  .msvc.anim .im img{animation:svkb linear both;animation-timeline:view();animation-range:entry 0% exit 100%}
  .msvc.anim .gn{animation:svgn linear both;animation-timeline:view();animation-range:entry 0% exit 100%}
  @keyframes svkb{from{transform:scale(1.16) translateY(-4%)}to{transform:scale(1.02) translateY(4%)}}
  @keyframes svgn{from{transform:translateY(-12%)}to{transform:translateY(-88%)}}
 }
 .msvc li.r .n{order:2;border-right:0;border-left:2px solid var(--ln);padding:0 0 0 14px;text-align:right}
 .msvc li.r>div:last-child{text-align:right}
 .msvc .n{font:900 extra-condensed 60px/1 Archivo,sans-serif;word-spacing:.08em;color:#0a3cff;min-width:58px;border-right:2px solid var(--ln);padding-right:14px}
 .msvc b{display:block;font:700 24px/1.08 Archivo,sans-serif;font-stretch:62.5%;word-spacing:.08em;text-transform:uppercase;letter-spacing:.01em}
 .msvc div span{display:block;font-weight:300;font-size:17px;line-height:1.3;margin-top:4px;color:#e8e8e8}
 .msup{list-style:none;margin:26px 0 0}
 .msup a{display:flex;align-items:center;gap:12px;min-height:62px;padding:0 14px 0 20px;border-left:2px solid #d8d8d8;border-bottom:1px solid #5a5a5a;transition:background .2s}
 .msup b{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}.msup a{position:relative}.msup .slogo{margin-right:auto;zoom:1.12;max-width:50%}.msup a.on .slogo{color:#fff}.msup a.on .vf{margin-right:16px}
 .msup .vf{display:none;font:600 14px Archivo,sans-serif;white-space:nowrap;padding-left:12px;border-left:2px solid #fff}
 .msup a.on{background:url(img/cat-band.webp) center/100% 100% no-repeat;border-color:transparent;margin:0 -8px;padding-left:28px;min-height:70px}
 .msup a.on b,.msup a.on .vf,.msup a.on svg{color:#fff}@media (max-width:420px){.msup .vf{font-size:12px;padding-left:8px}.msup a.on{padding-right:12px}.msup a.on svg{display:none!important}}.msup b{white-space:nowrap}.msup a.on .vf{display:block}.msup a.on svg{display:block}
 .mteam{display:grid;grid-template-columns:1fr 1fr;gap:0}
 .mteam div{padding-right:14px}.mteam div+div{border-left:2px solid #f4f4f2;padding-left:14px}
 .mteam b{display:block;font:700 clamp(22px,5.8vw,30px)/1.1 Archivo,sans-serif;font-stretch:70%;word-spacing:.08em;text-transform:uppercase}
 .mteam span{display:block;font:400 11px Archivo,sans-serif;letter-spacing:.2em;text-transform:uppercase;margin-top:8px}
 .maddr{display:flex;gap:14px;align-items:center;font:600 18px/1.45 Archivo,sans-serif;font-style:normal}
 .hgrid.mh{margin:20px 0 4px;gap:5px}.hgrid.mh li{min-height:86px;padding:9px 0 8px;border-radius:7px;background:#f4f4f2;color:#0a0a0a}.hgrid.mh b{font-size:13px}.hgrid.mh span{font-size:21px}
 .hgrid.mh li.off{background:none;color:#f4f4f2}.hgrid.mh li.off span{font-size:11.5px}
 html[data-theme=light] .hgrid.mh li{background:#0a0a0a;color:#f4f4f2}html[data-theme=light] .hgrid.mh li.off{background:none;color:#0a0a0a}
 .hgrid.mh li.now,html[data-theme=light] .hgrid.mh li.now{background:#0a3cff;color:#fff}
 .mpaper{margin:30px -12px 0;filter:drop-shadow(0 6px 18px #000a)}
 .mpaper .edge{display:block;width:100%;height:auto}
 .pbody{background:linear-gradient(#efefef,#e5e5e5);padding:6px 22px 18px;color:#111}
 .mh2{font:900 extra-condensed clamp(38px,11vw,62px)/1 Archivo,sans-serif;word-spacing:.08em;text-transform:uppercase;-webkit-text-stroke:2px currentColor;letter-spacing:-.01em;margin-bottom:16px}
 .mf{display:block;margin-bottom:16px;position:relative}.mf .flab{display:block;font:500 16px Archivo,sans-serif;margin-bottom:7px}
 .mf input,.mf textarea{width:100%;border:1px solid #9b9b9b;background:#f4f4f2d9;border-radius:2px;padding:13px 14px;font:400 16px Archivo,sans-serif;color:#111;outline:none}
 .mf textarea{resize:vertical;min-height:110px}.mf input:focus,.mf textarea:focus{border-color:#0a3cff;box-shadow:0 0 0 2px #0a3cff33}
 .mf input::placeholder,.mf textarea::placeholder{color:#8a8a8a}
 .mf.bad input,.mf.bad textarea{border-color:#d6002a}.mf .err{position:static;display:block;font:600 13px Archivo,sans-serif;color:#d6002a;margin-top:4px;font-style:normal}
 .mfile{display:flex;gap:16px;align-items:center;border:1.5px dashed #8d8d8d;border-radius:4px;padding:14px 16px;cursor:pointer;position:relative;background:#f4f4f280}
 .mfile input{position:absolute;inset:0;opacity:0;cursor:pointer}.mfile b{display:block;font:500 16px Archivo,sans-serif}.mfile small{display:block;font:400 14px Archivo,sans-serif;color:#777;margin-top:2px}
 .msubmit{width:100%;height:58px;border:0;border-radius:4px;color:#fff;font:600 18px Archivo,sans-serif;display:flex;justify-content:center;align-items:center;gap:10px;cursor:pointer;margin-top:4px;position:relative;overflow:hidden;isolation:isolate;
  background:linear-gradient(90deg,#0a3cff,#4f78ff 22%,#0a3cff 48%,#0526c9 76%,#0a3cff) 0 0/200% 100%;animation:msg 5s linear infinite,msh 2.4s ease-in-out infinite}
 .msubmit::after{content:'';position:absolute;z-index:-1;top:-20%;bottom:-20%;left:-90px;width:46px;background:linear-gradient(90deg,#fff0,#ffffff99,#fff0);transform:skewX(-20deg);animation:mss 3.2s cubic-bezier(.4,0,.2,1) infinite}
 @keyframes msg{to{background-position:200% 0}}@keyframes msh{0%,100%{box-shadow:0 0 0 #0a3cff00}50%{box-shadow:0 0 24px #0a3cffcc}}@keyframes mss{0%,55%{left:-90px}100%{left:calc(100% + 60px)}}
 .msubmit svg{animation:dva 1.6s ease-in-out infinite}
 @media (prefers-reduced-motion:reduce){.msubmit,.msubmit::after,.msubmit svg{animation:none}.msubmit::after{display:none}}
 .mm3d{display:inline-flex;align-items:center;gap:10px;margin:22px 0 4px;height:48px;padding:0 20px;border-radius:24px;border:2px solid #0a3cff;background:#0a3cff22;color:inherit;font:600 16px/1 Archivo,sans-serif;text-decoration:none}.mpills{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 0}.mpills .mm3d{margin:0}.mm3d.prix{background:#0a3cff;color:#fff}.mprix{margin:12px 0 6px;font-size:13.5px;line-height:1.4;opacity:.72;max-width:36ch}.mm3dl{display:inline-block;margin-top:8px;padding:6px 0;color:#0a3cff;font:500 14px Archivo,sans-serif;text-underline-offset:3px}
 .legal{font:400 12px/1.4 Archivo,sans-serif;color:#444;text-align:center;margin-top:12px}.legal a{color:#222;display:inline-block;margin-top:6px;padding:4px 0}
 .pbody .ok{position:static;width:auto;height:auto;padding:40px 0;background:none;border-radius:0}
 .mmap{position:relative}.mitin{position:absolute;z-index:4;left:74px;top:852px;width:174px;height:56px;border-radius:40px}
 .mfoot{border-top:1px solid #333;margin-top:30px;padding:30px 20px 50px;display:flex;flex-direction:column;align-items:center;gap:8px;font:400 14px Archivo,sans-serif;color:#bbb;text-align:center}
 .mfoot a{color:#fff;text-decoration:underline;text-underline-offset:3px}
}
@media (min-width:700px) and (max-width:1024px){
 .mpage{padding:20px 40px 50px}.bleed{width:calc(100% + 80px);margin-left:-40px}
 .mhead{padding:18px 40px 26px}.mlogo .logo-svg{height:64px}
 .msvc{grid-template-columns:1fr 1fr;column-gap:40px;row-gap:26px;align-items:start}.msvc li.r{margin-top:120px}.msvc .ph{width:100%;margin:0!important}.msvc{margin-inline:-40px;padding-inline:40px}.msvc .gn{font-size:30vw;left:94%}.msvc li.r .gn{left:auto;right:94%}
 .mteam{max-width:560px}

 .mpaper{margin:36px 0 0}
}
'''
