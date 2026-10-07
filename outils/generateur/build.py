"""Générateur du site EM Visions, version 2.
Une seule page claire, en français (racine) et en anglais (/en/), plus le modélisateur 3D et la politique de confidentialité.
Usage : python3 build.py   →   écrit le site dans out/"""
import html as H, json, os, re
from config import (SITE_URL, CONTACT_EMAIL, INSTAGRAM, HOURS, WEEK, ABOUT_FR, ABOUT_EN, FORM_ENDPOINT, fontface, _h)
from i18n import EN as EN1, SLUG
import realisations as REA, loader

LOGO_VB=open('logo_vb.txt').read().strip(); LOGO_D=open('logo_path.txt').read().strip()
ORDER=['accueil','services','realisations','catalogue','a-propos','contact']
NAV={'accueil':('Accueil','Home'),'services':('Services','Services'),'realisations':('Réalisations','Our work'),'catalogue':('Catalogue','Catalog'),'a-propos':('À propos','About'),'contact':('Contact','Contact')}
SVC=[('Design graphique','Des visuels qui marquent votre identité.','Illustration : une main trace au marqueur une orbite et une étoile bleues'),
     ('Impression','Des supports de qualité pour vos projets.','Illustration : deux mains tirent une raclette d’encre bleue sur un cadre de sérigraphie'),
     ('Vêtements personnalisés','Des textiles uniques à votre image.','Illustration : un t-shirt, une casquette et un chandail à capuchon imprimés en bleu'),
     ('Impression 3D','Des idées qui prennent forme.','Illustration : la buse d’une imprimante 3D construit une pièce bleue couche par couche'),
     ('Sites Web','Des plateformes sur mesure pour propulser votre marque.','Illustration : une page Web en papier déchiré, un curseur clique sur un bouton bleu'),
     ('Applications','Des outils performants pour vos besoins spécifiques.','Illustration : une main tient un téléphone d’où s’échappent des icônes en papier')]
SUPS=[('S&S Activewear','ss',184,26,'https://fr-ca.ssactivewear.com/'),('Canada Sportswear','canada',114,44,'https://canadasportswear.com/'),('Fabrik','fabrik',116,36,'https://fabrik.ca/'),
      ('Eside','eside',93,30,'https://eside.ca/fr/'),('Just Like Hero','jlh',71,52,'https://www.justlikehero.com/'),('Projob','projob',152,34,'https://texet.ca/pages/projob')]
CATS=[('vet','Vêtements','Apparel',['tshirt','longsleeve','tank','polo','crewneck','hoodie','jacket','vest','pants']),
      ('tete','Casquettes et tuques','Caps and beanies',['cap','bucket','beanie','hardhat']),
      ('sacs','Sacs','Bags',['tote','drawstring']),
      ('obj','Objets','Objects',['mug','bottle','travel','pen','pencil','pillow','umbrella']),
      ('aff','Affichage','Displays',['rollup','banner'])]
PROD={m[0]:(m[1],m[2]) for m in re.findall(r"\{id:'(\w+)',n:\['([^']*)','([^']*)'\]",open('maquette_produits.js').read())}
assert sorted(sum((c[3] for c in CATS),[]))==sorted(PROD), 'catégories et produits du modélisateur ne concordent pas'
SHOWN=8   # réalisations visibles avant « Voir toutes les réalisations »

# Textes propres à la version 2 (le reste vient de i18n.py et de realisations.py)
EN2={'L’atelier':'The workshop','Des techniques qui donnent corps à vos idées.':'Techniques that give your ideas a body.','L’art de faire durer les idées':'The art of making ideas last','Notre processus':'Our process',
 'L’impression<br>en trois temps.':'Printing<br>in three steps.','Un savoir-faire précis, du premier croquis au produit fini, pour des créations durables.':'Precise know-how, from the first sketch to the finished product, for creations that last.',
 'Le visuel':'The artwork','On prépare votre visuel, ou on le crée avec vous.':'We prepare your artwork, or create it with you.','L’impression':'The print','L’encre est posée avec précision, couche par couche.':'The ink is laid down precisely, layer by layer.',
 'Le résultat':'The result','Un produit à votre image, au rendu net et durable.':'A product that looks like you, with a crisp, lasting finish.','Nos autres services':'Our other services','Des résultats concrets, sur tous les supports.':'Real results, on every medium.',
 'photo':'photo','photos':'photos','Des supports réels, pour des projets durables. Choisissez un produit, regardez ses couleurs, puis essayez-le avec votre image en 3D.':'Real products for projects that last. Pick a product, look at its colours, then try it with your image in 3D.',
 'Fournisseurs':'Suppliers','Devant et dos':'Front and back','Devant':'Front','couleurs':'colours','couleur':'colour','Impression : ':'Print: ','Posez votre logo ou votre visuel dessus et voyez le résultat avant de demander un devis.':'Place your logo or artwork on it and see the result before asking for a quote.',
 'Couleurs':'Colours','Prix':'Price','Sur demande':'On request','Couleurs à essayer':'Colours to try','Les couleurs exactes sont confirmées avec le devis.':'Exact colours are confirmed with the quote.','Comparer les produits':'Compare products','Voir les {n} produits':'See all {n} products',
 'Un projet spécifique ?':'A specific project?','Parlons de votre support.':'Let’s talk about your medium.','L’équipe':'The team','Les gens derrière<br>l’impression.':'The people behind<br>the print.',
 'Contact / Demande de devis':'Contact / Quote request','Votre nom complet':'Your full name','Décrivez brièvement votre projet (ex. : cartes d’affaires, t-shirts, autocollants, etc.)':'Briefly describe your project (e.g. business cards, t-shirts, stickers, etc.)',
 'Sélectionnez une option':'Select an option','1 à 10':'1 to 10','11 à 50':'11 to 50','51 à 100':'51 to 100','101 à 500':'101 to 500','Plus de 500':'More than 500','Je ne sais pas encore':'I don’t know yet',
 'ou touchez pour parcourir':'or tap to browse','Formats acceptés : JPG, PNG, PDF (max. 10 Mo)':'Accepted formats: JPG, PNG, PDF (max. 10 MB)','Des idées bien imprimées.':'Ideas, well printed.','Service : ':'Service: ',
 'Faites bonne impression':'Make a good impression','Vêtements et objets personnalisés pour donner forme à vos idées.':'Custom apparel and objects that give shape to your ideas.',
 'Voir nos réalisations':'See our work','L’atelier, rue Jean-Talon Est':'The workshop on Jean-Talon Street East','Mettre la vidéo en pause':'Pause the video','Relancer la vidéo':'Play the video',
 'De l’idée à la matière':'From idea to matter','Six services sous un même toit. Dites-nous ce qu’il vous faut, on s’occupe du reste.':'Six services under one roof. Tell us what you need and we take care of the rest.',
 'Le travail parle':'The work speaks','Des idées devenues réelles. Touchez un projet pour voir ses photos.':'Ideas made real. Tap a project to see its photos.',
 'Voir les {n} réalisations':'See all {n} projects','Choisissez votre support':'Choose your medium',
 'Choisissez un produit, puis essayez-le avec votre image dans le modélisateur 3D.':'Pick a product, then try it with your image in the 3D mockup tool.',
 'Catégorie':'Category','Tous les produits':'All products','Essayez-le avant de commander':'Try it before you order',
 'Posez votre logo sur le produit, faites-le tourner, puis joignez la maquette à votre demande de devis.':'Place your logo on the product, rotate it, then attach the mockup to your quote request.',
 'Ouvrir le modélisateur 3D':'Open the 3D mockup tool','Essayer en 3D':'Try in 3D','Casquettes brodées « em » blanches et bleues':'White and blue caps embroidered with “em”',
 'Nos fournisseurs':'Our suppliers','Les prix, on vous les envoie':'We send you the prices',
 'Les prix ne sont pas affichés : on vous les envoie personnellement, selon votre projet.':'Prices aren’t listed: we send them to you personally, based on your project.','Demander les prix':'Ask for prices',
 'Les gens derrière l’impression':'The people behind the print','Deux membres de l’équipe EM Visions examinent un chandail imprimé':'Two EM Visions team members look over a printed sweatshirt',
 'On fait quoi ensemble ?':'What are we making together?','Parlez-nous de votre idée. On vous répond avec les bonnes options.':'Tell us about your idea. We reply with the right options.',
 'Votre idée':'Your idea','Dites-nous ce que vous avez en tête : type d’imprimé, usage, format ou toute autre idée. Pas besoin d’avoir tous les détails pour commencer.':'Tell us what you have in mind: type of print, use, format or any other idea. You don’t need every detail to get started.',
 'Les détails':'The details','Précisez ce qui compte : quantité approximative, échéance, fichiers ou inspirations. Plus on en sait, plus on peut vous proposer les bonnes options.':'Add what matters: approximate quantity, deadline, files or inspiration. The more we know, the better the options we can suggest.',
 'On en parle':'We talk it over','On regarde votre demande et on vous revient rapidement avec nos recommandations et un devis clair.':'We look at your request and get back to you quickly with our recommendations and a clear quote.',
 'Devis':'Quote','Échéance souhaitée':'Needed by','Déposez un fichier ici':'Drop a file here','ou touchez pour le choisir — JPG, PNG, PDF (max 10 Mo)':'or tap to choose one — JPG, PNG, PDF (max 10 MB)',
 'Envoyer ma demande':'Send my request','Où nous trouver':'Where to find us','Aujourd’hui : ':'Today: ',' à ':' to ','Aujourd’hui : fermé':'Today: closed','Devanture de l’atelier EM Custom Design, rue Jean-Talon Est':'Storefront of the EM Custom Design workshop on Jean-Talon Street East',
 'Menu':'Menu','Passer au thème sombre':'Switch to dark theme','Passer au thème clair':'Switch to light theme','Photo ':'Photo ','Vidéo ':'Video ',
 'Projet semblable à : ':'Similar project to: ','Demande de prix : ':'Price request: ','Échéance':'Deadline','Retour aux réalisations':'Back to our work','Tous droits réservés.':'All rights reserved.',
 'Instagram':'Instagram','Fournisseur : ':'Supplier: ','Navigation principale':'Main navigation','Voir le projet : ':'View the project: ','Langue':'Language'}

from urllib.parse import quote
PJ={p['id']:p for p in json.load(open('produits.json'))}       # couleurs et zones d'impression, tirées du modélisateur (produits.json)
ICON={'vet':'<path d="M8.5 4 4 6.5 2 11l3.2 1.6L6.5 11v9h11v-9l1.3 1.6L22 11l-2-4.5L15.5 4a3.5 3.5 0 0 1-7 0z"/>',
      'tete':'<path d="M4 15a8 8 0 0 1 16 0zM4 15c5-2 13-1.6 19 2.4-5-1-12-1.300-19 .6zM12 7V5.500"/>',
      'sacs':'<path d="M5 9h14l-1 11.500H6zM9 9V7a3 3 0 0 1 6 0v2"/>',
      'obj':'<path d="M5 6h11v10a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3zM16 9h2a2.500 2.500 0 0 1 0 5h-2"/>',
      'aff':'<path d="M7 3h10v15H7zM5 21h14M12 18v3"/>'}
uri=lambda svg:"data:image/svg+xml,"+quote(svg,safe="/:=;,'()! *@&-._~")
BLOB=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'><path d='M40 0L100 0L100 19.5L75 19.5Q70 19.5 70 23.5L70 32.5Q70 36.5 75 36.5L96 36.5Q100 36.5 100 41L100 100L32 100"
      "C23 100 22 91 15 81C8 71 0 67 0 52C0 36 14 30 20 16C24 6 30 0 40 0Z'/></svg>")
INK=("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 420' preserveAspectRatio='none'><filter id='r' x='-10%' y='-10%' width='120%' height='120%'><feTurbulence type='fractalNoise' baseFrequency='.035' numOctaves='4' seed='11' result='n'/>"
     "<feDisplacementMap in='SourceGraphic' in2='n' scale='46' result='d'/><feTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='2' seed='4' result='g'/><feColorMatrix in='g' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -3.4 2.5' result='ga'/>"
     "<feComposite in='d' in2='ga' operator='in'/></filter><g fill='#0a3cff' filter='url(#r)'><path d='M250 -20C330 -30 520 10 500 90C485 150 330 120 300 190C270 260 470 240 480 330C486 390 380 440 300 430C240 420 250 340 210 300C160 250 250 210 240 150C232 100 170 -10 250 -20Z'/></g></svg>")
ARL="<svg viewBox='0 0 46 14' aria-hidden='true'><path d='M0 7h44M38 1.500l6 5.500-6 5.500' fill='none' stroke='currentColor' stroke-width='1.200'/></svg>".replace("'",'"')
def ff(up): return (f"@font-face{{font-family:'Archivo';font-weight:100 900;font-stretch:62% 125%;src:url({up}fonts/archivo-latin-wdth-normal.woff2) format('woff2')}}"
                    f"@font-face{{font-family:'Newsreader';font-weight:200 800;src:url({up}fonts/newsreader-latin-wght-normal.woff2) format('woff2')}}")

def build(L):
    en=L=='en'; up='../' if en else ''; e=H.escape
    def t(s):
        if not en: return s
        for d in (EN2,REA.EN,EN1):
            if s in d: return d[s]
        raise KeyError('traduction manquante : '+s)
    def tn(s):                                   # nom propre : traduit seulement s'il a une traduction
        try: return t(s)
        except KeyError: return s
    sid=lambda p:SLUG[p] if en else p            # identifiant de la section dans cette langue
    alt=lambda p:p if en else SLUG[p]            # … et dans l'autre
    tool='mockup/' if en else 'maquette/'; priv='privacy/' if en else 'confidentialite/'
    arr='<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12h18M14 5.500l6.500 6.500-6.500 6.500" fill="none" stroke="currentColor" stroke-width="1.500" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    logo=f'<svg viewBox="{LOGO_VB}" aria-hidden="true"><use href="#emlogo"/></svg>'
    def big(tag,lines,cls,dot=True,extra=''):
        last=lines[-1]; d='' if (not dot or last.endswith('?')) else '<i class="dot" aria-hidden="true"></i>'
        return f'<{tag} class="{cls}"{extra}>'+''.join(e(x)+'<br>' for x in lines[:-1])+f'<span>{e(last)}{d}</span></{tag}>'
    cur='aria-current="true"'
    def lang():
        fr=f'<a href="../#accueil" data-other="../" hreflang="fr" lang="fr">FR</a>' if en else f'<a href="#accueil" {cur} hreflang="fr" lang="fr">FR</a>'
        an=f'<a href="#home" {cur} hreflang="en" lang="en">EN</a>' if en else f'<a href="en/#home" data-other="en/" hreflang="en" lang="en">EN</a>'
        return f'<span class="lang" role="group" aria-label="{e(t("Langue"))}">{fr}<i></i>{an}</span>'
    tog='<button type="button" class="tog"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg></button>'
    links=''.join(f'<a href="#{sid(p)}">{e(NAV[p][en])}</a>' for p in ORDER)
    pill=lambda label,attr='': f'<a class="pill" href="#contact"{attr}><i>{arr}</i><span>{e(t(label))}</span></a>'
    def sec(p,inner,cls=''): return f'<section class="sec {cls}" id="{sid(p)}" data-alt="{alt(p)}" aria-label="{e(NAV[p][en])}"><div class="wrap">{inner}</div></section>'

    # ---------- en-tête
    head=(f'<header class="hd"><div class="hd-in"><a class="logo" href="#{sid("accueil")}" aria-label="EM Visions — {e(NAV["accueil"][en].lower())}">{logo}</a>'
          f'<nav class="nav" aria-label="{e(t("Navigation principale"))}">{links}</nav>{lang()}{tog}'
          f'<button type="button" class="burger" aria-label="{e(t("Ouvrir le menu"))}" aria-expanded="false" aria-controls="menu"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div></header>'
          f'<div class="menu" id="menu" hidden><div class="menu-top"><a class="logo" href="#{sid("accueil")}" aria-label="EM Visions">{logo}</a>'
          f'<button type="button" class="burger menu-x" style="display:grid" aria-label="{e(t("Fermer le menu"))}"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div>'
          f'<nav aria-label="{e(t("Menu"))}">{links}</nav><a class="btn" href="#contact">{e(t("Demander un devis"))}{arr}</a><div class="menu-foot">{lang()}{tog}</div></div>')

    # ---------- accueil
    pin='<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5a7 7 0 0 0-7 7c0 5.2 7 12 7 12s7-6.8 7-12a7 7 0 0 0-7-7z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="9.5" r="2.4" fill="currentColor"/></svg>'
    clock='<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v5l3.4 2.2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    hero=(f'<section id="{sid("accueil")}" data-alt="{alt("accueil")}" aria-label="{e(NAV["accueil"][en])}"><div class="wrap hero"><div>'
          +big('h1',['Make','a good','impression'] if en else ['Faites','bonne','impression'],'dz')
          +f'<p class="lead">{e(t("Vêtements et objets personnalisés pour donner forme à vos idées."))}</p>'
          f'<div class="hero-a">{pill("Demander un devis")}<a class="txt" href="#{sid("realisations")}">{e(t("Voir nos réalisations"))}</a></div>'
          f'<ul class="facts"><li>{pin}<span><b>5825, rue Jean-Talon Est</b>, Saint-Léonard</span></li>'+(f'<li>{clock}<span id="today"></span></li>' if HOURS else '')+'</ul></div>'
          f'<figure class="hero-m"><img src="{up}img/atelier-poster.webp" alt="{e(t("Devanture de l’atelier EM Custom Design, rue Jean-Talon Est"))}" width="626" height="784" fetchpriority="high">'
          f'<video data-src="{up}vid/atelier.mp4" poster="{up}img/atelier-poster.webp" muted loop playsinline preload="none" aria-hidden="true"></video>'
          f'<button type="button" class="pp" hidden aria-pressed="false" aria-label="{e(t("Mettre la vidéo en pause"))}"><svg class="ic b" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6v12M15 6v12" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/></svg>'
          f'<svg class="ic a" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6.5v11l9-5.5z" fill="currentColor"/></svg></button>'
          f'<figcaption><b>{e(t("L’atelier"))}</b>Jean-Talon Est</figcaption></figure></div></section>')

    # ---------- services : un panneau d'ouverture, le processus en trois temps, puis les autres services
    proc=[('Le visuel','On prépare votre visuel, ou on le crée avec vous.','svc-1',SVC[0][2]),
          ('L’impression','L’encre est posée avec précision, couche par couche.','svc-2',SVC[1][2]),
          ('Le résultat','Un produit à votre image, au rendu net et durable.','rea-maverick-tee-blanc','T-shirt blanc Maverick imprimé au dos')]
    pr=''.join(f'<li><div class="tx"><span class="n" aria-hidden="true">{i+1:02d}</span><div><h3>{e(t(a))}</h3><p>{e(t(b))}</p></div>'+(f'<span class="ar" aria-hidden="true">{ARL}</span>' if i<2 else '<span></span>')
               +f'</div><img src="{up}img/{im}.webp" alt="{e(t(al))}" loading="lazy" width="800" height="700"></li>' for i,(a,b,im,al) in enumerate(proc))
    oth=[SVC[0],SVC[2],SVC[3],SVC[4],SVC[5]]
    ot=''.join(f'<li><span class="n" aria-hidden="true">{i+2:02d}</span><h3>{e(t(n))}</h3><p>{e(t(d))}</p><a href="#contact" data-svc="{e(t(n))}" aria-label="{e(t("Parler de mon projet")+" : "+t(n))}">{ARL}</a></li>' for i,(n,d,a) in enumerate(oth))
    services=sec('services',
        f'<div class="sv1"><div class="sv1-t">'+big('h2',['From idea','to','matter'] if en else ['De l’idée','à la','matière'],'dz ink')
        +f'<p class="lead">{e(t("Des techniques qui donnent corps à vos idées."))}</p><div class="sv1-a"><i class="tick" aria-hidden="true"></i>{pill("Parler de mon projet")}</div>'
        f'<ul class="sv1-l" aria-hidden="true">'+''.join(f'<li>{e(x)}</li>' for x in (('Design','Printing','Apparel','3D','Web') if en else ('Design','Impression','Vêtements','3D','Web')))+'</ul></div>'
        f'<div class="sv1-m"><div class="blob"><img src="{up}img/svc-2.webp" alt="{e(t(SVC[1][2]))}" width="720" height="900"></div><p class="sv1-n"><b>01 /</b>{e(t("Impression"))}</p></div>'
        f'<div class="sv1-foot"><p class="sv1-f">{e(t("L’art de faire durer les idées"))}</p></div></div>'
        f'<div class="sv2"><p class="lab kick">{e(t("Notre processus"))}</p><div class="sv2-h"><h3 class="ser">{t("L’impression<br>en trois temps.")}</h3><p class="lead">{e(t("Un savoir-faire précis, du premier croquis au produit fini, pour des créations durables."))}</p></div>'
        f'<ol class="proc">{pr}</ol>'
        f'<div class="others-h"><span class="lab">{e(t("Nos autres services"))}</span><span class="lab">{e(t("Des résultats concrets, sur tous les supports."))}</span></div><ul class="others">{ot}</ul></div>')

    # ---------- réalisations
    R=REA.REAL
    nph=lambda r:len(r['ph'])+(1 if r.get('vk') else 0)
    works=''.join(f'<li{" hidden" if i>=SHOWN else ""}><button type="button" data-i="{i}" aria-label="{e(t("Voir le projet : ")+tn(r["n"]))}"><span class="im"><img src="{up}{r["ph"][0]["s"]}" alt="{e(t(r["ph"][0]["a"]))}" loading="lazy" width="540" height="540"></span>'
                  f'<span class="tt"><b>{e(tn(r["n"]))}</b><i>{nph(r)} {e(t("photo") if nph(r)==1 else t("photos"))}</i></span><small>{e(t(r["k"]))}</small></button></li>' for i,r in enumerate(R))
    real=sec('realisations',f'<div class="head">'+big('h2',['The work','speaks'] if en else ['Le travail','parle'],'dw')+f'<p>{e(t("Des idées devenues réelles. Touchez un projet pour voir ses photos."))}</p></div>'
             +f'<ul class="works">{works}</ul>'+(f'<div class="end"><button type="button" class="btn ghost" id="more">{e(t("Voir les {n} réalisations").replace("{n}",str(len(R))))}{arr}</button></div>' if len(R)>SHOWN else ''))

    # ---------- catalogue
    chev='<svg class="ch" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 4l8 8-8 8" fill="none" stroke="currentColor" stroke-width="1.800"/></svg>'
    ico=lambda c:f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.300" stroke-linejoin="round" stroke-linecap="round">{ICON[c].replace(".500",".5").replace(".300",".3").replace(".600",".6")}</svg>'
    catnav=''.join(f'<li><button type="button" data-cat="{c}" aria-pressed="{"true" if k==0 else "false"}">{ico(c)}{e(ne if en else nf)}{chev}</button></li>' for k,(c,nf,ne,ids) in enumerate(CATS))
    sups=''.join(f'<li><a href="{u}" target="_blank" rel="noopener" aria-label="{e(t("Fournisseur : ")+n)}"><i class="slogo" style="--m:url({up}img/logo-{k}.webp);width:{int(w*.8)}px;aspect-ratio:{w}/{h}"></i></a></li>' for n,k,w,h,u in SUPS)
    sides=lambda p:t('Devant et dos') if len(p['sides'])>1 else t('Devant')
    ncol=lambda p:(f'{len(p["colors"])} '+t('couleurs')) if len(p['colors'])>1 else ('1 '+t('couleur'))
    prods=''.join(f'<li data-cat="{c}"{" hidden" if k else ""}><button type="button" data-p="{i}" aria-pressed="{"true" if (k==0 and j==0) else "false"}"><span class="im"><img src="{up}img/m3d/{i}.webp" alt="" loading="lazy" width="384" height="384"></span>'
                  f'<span class="tt"><b>{e(PROD[i][en])}</b><i>{e(ncol(PJ[i]))}</i></span><small>{e(t("Impression : ")+sides(PJ[i]).lower())}</small>'
                  f'<span class="ds" aria-hidden="true">'+''.join(f'<i style="background:{col[2]}"></i>' for col in PJ[i]['colors'][:5])+'</span></button></li>'
                  for k,(c,nf,ne,ids) in enumerate(CATS) for j,i in enumerate(ids))
    cat=sec('catalogue',f'<div class="head">'+big('h2',['Choose','your medium'] if en else ['Choisissez','votre support'],'dw')
            +f'<p>{e(t("Des supports réels, pour des projets durables. Choisissez un produit, regardez ses couleurs, puis essayez-le avec votre image en 3D."))}</p></div>'
            f'<div class="cat"><div class="cat-nav"><span class="lab" id="catlab">{e(t("Catégorie"))}</span><ul class="cats" aria-labelledby="catlab">{catnav}</ul>'
            f'<div class="grp"><span class="lab">{e(t("Fournisseurs"))}</span><ul>{sups}</ul></div></div><div>'
            f'<div class="pan" id="pan" aria-live="polite"><div class="pan-im"><img id="pan-img" src="{up}img/p/{CATS[0][3][0]}.webp" alt="" width="880" height="880"></div><div class="pan-tx">'
            f'<span class="lab" id="pan-cat"></span><h3 id="pan-name"></h3><p>{e(t("Posez votre logo ou votre visuel dessus et voyez le résultat avant de demander un devis."))}</p>'
            f'<dl><dt>{e(t("Couleurs"))}</dt><dd id="pan-col"></dd><dt>{e(t("Impression"))}</dt><dd id="pan-side"></dd><dt>{e(t("Prix"))}</dt><dd>{e(t("Sur demande"))}</dd></dl>'
            f'<div class="pan-a"><a class="btn" id="pan-try" href="{tool}">{e(t("Essayer en 3D"))}{arr}</a><a class="txt" data-prix href="#contact">{e(t("Demander les prix"))}</a></div>'
            f'<div class="sw"><div><span class="lab">{e(t("Couleurs à essayer"))}</span><p>{e(t("Les couleurs exactes sont confirmées avec le devis."))}</p></div><ul id="pan-sw"></ul></div></div></div>'
            f'<div class="cmp-h"><h3>{e(t("Comparer les produits"))}</h3><button type="button" class="txt" id="allp">{e(t("Voir les {n} produits").replace("{n}",str(len(PROD))))}{arr}</button></div>'
            f'<ul class="prods">{prods}</ul></div></div>'
            f'<div class="band"><div class="band-t"><span class="lab">{e(t("Un projet spécifique ?"))}</span><h3>{e(t("Parlons de votre support."))}</h3>'
            f'<p>{e(t("Les prix ne sont pas affichés : on vous les envoie personnellement, selon votre projet."))}</p><a class="btn white" data-prix href="#contact">{e(t("Demander les prix"))}{arr}</a></div>'
            f'<div class="band-m"><img src="{up}img/cat-ricova.webp" alt="" loading="lazy" width="395" height="280"><ul>'+''.join(f'<li>{e(ne if en else nf)}</li>' for c,nf,ne,ids in CATS)+'</ul></div></div>')

    # ---------- à propos
    about=sec('a-propos',f'<p class="lab kick">{e(t("L’équipe"))}</p><div class="about"><figure><img src="{up}img/equipe.webp" alt="{e(t("Deux membres de l’équipe EM Visions examinent un chandail imprimé"))}" loading="lazy" width="830" height="443"></figure><div>'
              f'<h2 class="ser">{t("Les gens derrière<br>l’impression.")}</h2>'
              f'<div class="team"><div><b>Eduardo Mazzonna</b><span>{e(t("Design graphique"))}</span></div><div><b>Vince Mariani</b><span>{e(t("Gestion de projets"))}</span></div></div>'
              f'<p>{e(ABOUT_EN if en else ABOUT_FR)}</p></div></div>')

    # ---------- contact
    SI=['<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.500 10.900c.600.500 1 1.200 1 2.100h5c0-.900.400-1.600 1-2.100A6 6 0 0 0 12 3zM3 9h1.500M19.500 9H21M5 3.500l1 1M19 3.500l-1 1"/>',
        '<path d="M8 3h9l3 3v12H8zM8 7H5v14h11v-3M11 9h6M11 12h6M11 15h4"/>',
        '<path d="M4 4h11v8H9l-3 3v-3H4zM15 8h5v8h-2v3l-3-3h-4v-2"/>']
    stp=[('Votre idée','Dites-nous ce que vous avez en tête : type d’imprimé, usage, format ou toute autre idée. Pas besoin d’avoir tous les détails pour commencer.'),
         ('Les détails','Précisez ce qui compte : quantité approximative, échéance, fichiers ou inspirations. Plus on en sait, plus on peut vous proposer les bonnes options.'),
         ('On en parle','On regarde votre demande et on vous revient rapidement avec nos recommandations et un devis clair.')]
    on=' class="on"'
    fx=lambda s:s.replace('.500','.5').replace('.600','.6').replace('.900','.9').replace('.200','.2').replace('.400','.4').replace('.100','.1')
    steps=''.join(f'<li{on if i==0 else ""}><span class="n" aria-hidden="true">{i+1:02d}</span><h3>{e(t(a))}</h3><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width=".9" stroke-linecap="round" stroke-linejoin="round">{fx(SI[i])}</svg><p>{e(t(b))}</p></li>' for i,(a,b) in enumerate(stp))
    fattr=f' action="{FORM_ENDPOINT}" method="post" enctype="multipart/form-data" data-send="1"' if FORM_ENDPOINT else ''
    fhid=('<input type="hidden" name="_subject" value="Demande de devis — site EM Visions"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">'
          '<input type="hidden" name="_next" value=""><input type="hidden" name="_replyto" value=""><input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">') if FORM_ENDPOINT else ''
    def fld(n,lab,ctl): return f'<label class="f"><span>{e(t(lab))}</span>{ctl}<em class="err" data-err="{n}" aria-live="polite"></em></label>'
    if CONTACT_EMAIL:
        konote=t('Vos réponses sont conservées. Vous pouvez réessayer ou nous écrire directement par courriel.'); koalt=f'<a class="txt bymail" data-mail="{CONTACT_EMAIL}" href="mailto:{CONTACT_EMAIL}">{e(t("Écrire par courriel"))}</a>'
    else:
        konote=t('Vos réponses sont conservées. Vous pouvez réessayer, nous écrire sur Instagram ou passer à l’atelier.'); koalt=f'<a class="txt bymail" href="{INSTAGRAM}" target="_blank" rel="noopener">{e(t("Écrire sur Instagram"))}</a>'
    qopt=''.join(f'<option>{e(t(o))}</option>' for o in ('1 à 10','11 à 50','51 à 100','101 à 500','Plus de 500','Je ne sais pas encore'))
    form=(f'<div class="fcard"><span class="ftag" aria-hidden="true">{e(t("Devis"))}<br>/ 01</span><h3>{e(t("Demande de devis"))}</h3><form id="devis" novalidate{fattr}>{fhid}'
          +fld('nom','Nom *',f'<input name="nom" type="text" autocomplete="name" maxlength="150" placeholder="{e(t("Votre nom complet"))}" required>')
          +fld('courriel','Courriel *',f'<input name="courriel" type="email" autocomplete="email" inputmode="email" placeholder="{e(t("votre@courriel.com"))}" required>')
          +fld('projet','Votre projet *',f'<textarea name="projet" rows="4" maxlength="5000" placeholder="{e(t("Décrivez brièvement votre projet (ex. : cartes d’affaires, t-shirts, autocollants, etc.)"))}" required></textarea>')
          +'<div class="f2">'+fld('qte','Quantité approximative',f'<select name="qte"><option value="">{e(t("Sélectionnez une option"))}</option>{qopt}</select>')
          +fld('echeance','Échéance','<input name="echeance" type="date">')+'</div>'
          +f'<div class="f" style="margin-bottom:0"><span class="flab" id="fl-lab">{e(t("Joindre un visuel"))}</span><label class="drop"><input type="file" name="fichier" aria-labelledby="fl-lab" accept=".jpg,.jpeg,.png,.pdf,image/jpeg,image/png,application/pdf">'
          '<svg width="34" height="34" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15V4M7.500 8.500L12 4l4.500 4.500M5 14v5h14v-5" fill="none" stroke="currentColor" stroke-width="1.600" stroke-linecap="round" stroke-linejoin="round"/></svg>'
          f'<b data-fl>{e(t("Déposez un fichier ici"))}</b><small data-fh>{e(t("ou touchez pour parcourir"))}</small></label><em class="err" data-err="fichier" aria-live="polite"></em>'
          f'<p class="fnote"><span>{e(t("Formats acceptés : JPG, PNG, PDF (max. 10 Mo)"))}</span><a href="{tool}">{e(t("ou créer une maquette 3D"))}</a></p></div>'
          f'<button type="submit" class="send">{e(t("Envoyer ma demande"))}{arr}</button>'
          f'<p class="legal">{e(t("En soumettant ce formulaire, vous nous permettez de vous contacter concernant votre demande."))} <a href="{priv}">{e(t("Politique de confidentialité"))}</a></p></form>'
          f'<div class="ok" id="ok" hidden role="status" tabindex="-1"><b>{e(t("MERCI."))}</b><p>{e(t("Votre demande est bien envoyée."))}</p><p class="note">{e(t("Nous vous répondrons par courriel."))}</p><p class="note ref"></p><div class="okb"><button type="button" class="btn ghost again">{e(t("Nouvelle demande"))}</button></div></div>'
          f'<div class="ok" id="ko" hidden role="alert" tabindex="-1"><b>{e(t("OUPS."))}</b><p>{e(t("Votre demande n’a pas pu être envoyée."))}</p><p class="note">{e(konote)}</p><div class="okb"><button type="button" class="btn retry">{e(t("Réessayer"))}</button>{koalt}</div></div></div>')
    hours=''
    if HOURS:
        cells=''.join((f'<li data-d="{n}"><b>{en_ if en else fr}</b><span>{_h(s[0],en)}<br>{_h(s[1],en)}</span></li>' if s else f'<li class="off" data-d="{n}"><b>{en_ if en else fr}</b><span>{e(t("Fermé"))}</span></li>') for fr,en_,n,s in WEEK)
        hours=f'<div><span class="lab">{e(t("Heures d’ouverture"))}</span><ul class="hgrid">{cells}</ul></div>'
    strip=''.join(f'<img src="{up}img/{n}.webp" alt="{e(t(a))}" loading="lazy" width="540" height="284">' for n,a in (('rea-maumy-cartes-s','Cartes d’affaires Maumy'),('rea-buono-casquette-s','Casquette brodée Buono Bites'),('rea-maverick-detail-s','Détail de l’impression sur le t-shirt Maverick'),('rea-alpha-detail-s','Détail de l’impression Alpha Athletika')))
    contact=(f'<section class="sec" id="contact" data-alt="contact" aria-label="{e(NAV["contact"][en])}"><div class="wrap"><p class="crumb">{e(t("Contact / Demande de devis"))}</p>'
             +big('h2',['What are we','making?'] if en else ['On fait quoi','ensemble ?'],'dz')+f'<p class="lead">{e(t("Parlez-nous de votre idée. On vous répond avec les bonnes options."))}</p>'
             f'<div class="contact"><ol class="steps">{steps}</ol>{form}</div>'
             f'<div class="infos"><div><span class="lab">{e(t("Où nous trouver"))}</span><address>5825, rue Jean-Talon Est<br>Saint-Léonard, QC H1S 1M4</address>'
             f'<a class="btn ghost" href="https://www.google.com/maps/dir/?api=1&destination=5825+rue+Jean-Talon+Est%2C+Saint-L%C3%A9onard%2C+QC+H1S+1M4" target="_blank" rel="noopener" aria-label="{e(t("Itinéraire (Google Maps)"))}">{e(t("Itinéraire"))}{arr}</a></div>{hours}</div></div>'
             f'<div class="strip">{strip}</div></section>')

    foot=(f'<footer class="ft"><div class="wrap ft-in"><p><b>EM</b> Custom Design<br>{e(t("Des idées bien imprimées."))}</p>'
          f'<ul>'+(f'<li><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></li>' if CONTACT_EMAIL else '')+f'<li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li><li><a href="{priv}">{e(t("Politique de confidentialité"))}</a></li></ul></div></footer>')
    gal=(f'<div class="gal" id="gal" hidden role="dialog" aria-modal="true"><div class="gal-h"><div><button type="button" class="btn ghost" data-g="close">{e(t("Retour aux réalisations"))}</button>'
         f'<button type="button" class="burger gal-x" style="display:grid" data-g="close" aria-label="{e(t("Fermer"))}"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div></div><div class="gal-b"></div></div>')

    # ---------- données du script
    RL=[{'n':tn(r['n']),'k':t(r['k']),'a':t(r['a']),'m':up+r['m'],'t':up+r['m'],'v':(up+'vid/'+r['vk']+'.mp4') if r.get('vk') else None,
         'ph':[{'b':up+p['b'],'s':up+p['s'],'a':t(p['a'])} for p in r['ph']]} for r in R]
    PD={i:{'n':PROD[i][en],'c':(ne if en else nf),'cat':c,'col':ncol(PJ[i]),'side':sides(PJ[i]),'sw':[[col[1 if en else 0],col[2]] for col in PJ[i]['colors']]} for c,nf,ne,ids in CATS for i in ids}
    TR={'dark':t('Passer au thème sombre'),'light':t('Passer au thème clair'),'pause':t('Mettre la vidéo en pause'),'play':t('Relancer la vidéo'),'today':t('Aujourd’hui : '),'to':t(' à '),'todayClosed':t('Aujourd’hui : fermé'),
        'prevPhoto':t('Photo précédente'),'nextPhoto':t('Photo suivante'),'prevProject':t('Projet précédent'),'nextProject':t('Projet suivant'),'photo':t('Photo '),'video':t('Vidéo '),
        'similarBtn':t('Un projet semblable ? Demander un devis'),'similar':t('Projet semblable à : '),'priceReq':t('Demande de prix : '),'service':t('Service : '),
        'eName':t('Indiquez votre nom'),'eMail':t('Courriel invalide'),'eProj':t('Décrivez votre projet'),'eFmt':t('Format non accepté : JPG, PNG ou PDF'),'eSize':t('Fichier trop lourd (max 10 Mo)'),
        'mbChange':t(' Mo — toucher pour changer'),'dec':'.' if en else ',','sending':t('Envoi en cours…'),'ref':t('Référence : '),'name':t('Nom'),'mail':t('Courriel'),'qty':t('Quantité approximative'),'due':t('Échéance'),
        'subject':t('Demande de devis'),'mockAdded':t('Maquette 3D ajoutée à votre demande.'),'tool':tool,'img':up+'img/p/'}
    WK={n:[_h(s[0],en),_h(s[1],en)] if s else None for fr,en_,n,s in WEEK}
    js=(open('script.js').read().replace('%TR%',json.dumps(TR,ensure_ascii=False)).replace('%RL%',json.dumps(RL,ensure_ascii=False)).replace('%WEEK%',json.dumps(WK)).replace('%PD%',json.dumps(PD,ensure_ascii=False)))
    css=open('style.css').read()+f':root{{--blob:url("{uri(BLOB)}");--inkimg:url("{uri(INK)}")}}'
    headjs='(function(){var t;try{t=localStorage.getItem("em-theme")}catch(e){}document.documentElement.dataset.theme=t==="dark"?"dark":"light"})();'+loader.HEAD
    return (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{head_seo(L,up)}<script>{headjs}</script>'
            f'<style>{ff(up)}{css}{loader.CSS}</style></head><body>{loader.html(LOGO_VB)}<a class="sr skip" href="#{sid("services")}">{e(t("Aller au contenu"))}</a>'
            f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><symbol id="emlogo" viewBox="{LOGO_VB}"><path fill="currentColor" fill-rule="evenodd" d="{LOGO_D}"/></symbol></defs></svg>'
            f'{head}<main>{hero}{services}{real}{cat}{about}{contact}</main>{foot}{gal}<div class="toast" id="toast" role="status"></div><script>{js}</script></body></html>')

SEO={'fr':{'path':'/','locale':'fr_CA','title':'EM Visions — Vêtements et objets personnalisés à Saint-Léonard, Montréal',
           'desc':'Atelier à Saint-Léonard (Montréal) : vêtements et objets personnalisés, impression, design graphique, impression 3D et sites web. Demandez un devis.',
           'alt':'Page d’accueil EM Visions : « Faites bonne impression »'},
     'en':{'path':'/en/','locale':'en_CA','title':'EM Visions — Custom apparel and objects in Saint-Léonard, Montréal',
           'desc':'Workshop in Saint-Léonard (Montréal): custom apparel and objects, printing, graphic design, 3D printing and websites. Request a quote.',
           'alt':'EM Visions home page: “Make a good impression”'}}
def head_seo(L,up):
    m=SEO[L]; o=SEO['en' if L=='fr' else 'fr']; e=H.escape
    ld={'@context':'https://schema.org','@type':'LocalBusiness','@id':SITE_URL+'/#atelier','name':'EM Visions','alternateName':'EM Custom Design','description':m['desc'],
        'url':SITE_URL+m['path'],'image':SITE_URL+'/img/og.jpg','logo':SITE_URL+'/img/icon-512.png',**({'email':CONTACT_EMAIL} if CONTACT_EMAIL else {}),
        'address':{'@type':'PostalAddress','streetAddress':'5825, rue Jean-Talon Est','addressLocality':'Saint-Léonard','addressRegion':'QC','postalCode':'H1S 1M4','addressCountry':'CA'},
        'areaServed':'Montréal','sameAs':[INSTAGRAM],**({'openingHoursSpecification':[{'@type':'OpeningHoursSpecification','dayOfWeek':d,'opens':a,'closes':b} for d,a,b in HOURS]} if HOURS else {})}
    return (f'<title>{e(m["title"])}</title><meta name="description" content="{e(m["desc"])}">'
      f'<link rel="canonical" href="{SITE_URL}{m["path"]}"><link rel="alternate" hreflang="fr-CA" href="{SITE_URL}/"><link rel="alternate" hreflang="en-CA" href="{SITE_URL}/en/"><link rel="alternate" hreflang="x-default" href="{SITE_URL}/">'
      f'<meta property="og:type" content="website"><meta property="og:site_name" content="EM Visions"><meta property="og:title" content="{e(m["title"])}"><meta property="og:description" content="{e(m["desc"])}">'
      f'<meta property="og:url" content="{SITE_URL}{m["path"]}"><meta property="og:locale" content="{m["locale"]}"><meta property="og:locale:alternate" content="{o["locale"]}">'
      f'<meta property="og:image" content="{SITE_URL}/img/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(m["alt"])}">'
      f'<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#f6f6f3">'
      f'<link rel="icon" href="{up}img/favicon.svg" type="image/svg+xml"><link rel="icon" href="{up}img/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="{up}img/apple-touch-icon.png">'
      f'<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>')

if __name__=='__main__':
    os.makedirs('out/en',exist_ok=True)
    fr=build('fr'); open('out/index.html','w').write(fr); open('out/en/index.html','w').write(build('en'))
    import pages_extra; pages_extra.write(LOGO_VB,LOGO_D)
    import maquette_page; maquette_page.write(LOGO_VB,LOGO_D)
    open('out/robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n')
    X=lambda ps:''.join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{SITE_URL}{p}"/>' for h,p in ps)
    G=[(('/','/en/'),X((('fr-CA','/'),('en-CA','/en/'),('x-default','/')))),(('/confidentialite/','/en/privacy/'),X((('fr-CA','/confidentialite/'),('en-CA','/en/privacy/')))),
       (('/maquette/','/en/mockup/'),X((('fr-CA','/maquette/'),('en-CA','/en/mockup/'))))]
    open('out/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        +''.join(f'<url><loc>{SITE_URL}{p}</loc>{a}</url>\n' for ps,a in G for p in ps)+'</urlset>\n')
    print('site écrit :',len(fr)//1024,'Ko par page')
