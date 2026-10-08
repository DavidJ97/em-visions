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
EN2={'Faites bonne impression.':'Make a good impression.','Vêtements et objets personnalisés, impression et design. Un atelier à Saint-Léonard, rue Jean-Talon Est.':'Custom apparel and objects, printing and design. A workshop in Saint-Léonard, on Jean-Talon Street East.',
 'Voir les produits':'See the products','Pause':'Pause','Lecture':'Play','Six services sous un même toit.':'Six services under one roof.','Touchez un projet pour voir ses photos.':'Tap a project to see its photos.',
 'Touchez un produit pour l’essayer en 3D avec votre image.':'Tap a product to try it in 3D with your image.','Tout':'All','Prix sur demande : on vous les envoie personnellement, selon votre projet.':'Prices on request: we send them to you personally, based on your project.',
 'Ex. : 50 t-shirts avec notre logo, cartes d’affaires, enseigne…':'E.g. 50 t-shirts with our logo, business cards, a sign…','Demander un devis semblable':'Ask for a similar quote',
 'L’atelier':'The workshop','Des techniques qui donnent corps à vos idées.':'Techniques that give your ideas a body.','L’art de faire durer les idées':'The art of making ideas last','Notre processus':'Our process',
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

PJ={p['id']:p for p in json.load(open('produits.json'))}       # couleurs et zones d'impression, tirées du modélisateur (produits.json)
def ff(up): return (f"@font-face{{font-family:'Archivo';font-weight:100 900;font-stretch:62% 125%;src:url({up}fonts/archivo-latin-wdth-normal.woff2) format('woff2')}}"
                    f"@font-face{{font-family:'Instrument Serif';font-weight:400;font-display:swap;src:url({up}fonts/instrument-serif-latin-400-normal.woff2) format('woff2')}}")
EN2.update({'Maquette 3D':'3D mockup','Besoin d’aide':'Need help','Suivez-nous':'Follow us','Les choses sérieuses':'Serious stuff','produits':'products','produit':'product',
 'Vêtements et objets personnalisés, impression et design.':'Custom apparel and objects, printing and design.','Un atelier à Saint-Léonard, rue Jean-Talon Est':'A workshop in Saint-Léonard, on Jean-Talon Street East',
 'Autres liens':'More links'})
HERO=[('atelier','atelier-poster','L’atelier','Devanture de l’atelier EM Custom Design, rue Jean-Talon Est'),('ricova','rea-ricova','Ricova','Manteau de travail haute visibilité au logo Ricova'),
      ('buono','hero-buono','Buono Bites','Lettrage de vitrine pour le pop-up shop Buono Bites'),('ma','hero-ma','Enseigne MA','Enseigne ronde suspendue M/A')]

import datetime; YEAR=datetime.date.today().year
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
    logo=f'<svg viewBox="{LOGO_VB}" aria-hidden="true"><use href="#emlogo"/></svg>'
    cur='aria-current="true"'
    def lang():
        fr=f'<a href="../#accueil" data-other="../" hreflang="fr" lang="fr">FR</a>' if en else f'<a href="#accueil" {cur} hreflang="fr" lang="fr">FR</a>'
        an=f'<a href="#home" {cur} hreflang="en" lang="en">EN</a>' if en else f'<a href="en/#home" data-other="en/" hreflang="en" lang="en">EN</a>'
        return f'<span class="lang cap" role="group" aria-label="{e(t("Langue"))}">{fr}{an}</span>'
    tog='<button type="button" class="tog"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg></button>'
    links=''.join(f'<a href="#{sid(p)}">{e(NAV[p][en])}</a>' for p in ORDER[1:])
    quote=lambda cls='': f'<a class="btn {cls}" href="#contact">{e(t("Demander un devis"))}</a>'
    def row(p,sub,inner): return (f'<section class="wrap row" id="{sid(p)}" data-alt="{alt(p)}" aria-labelledby="h-{p}"><header><h2 id="h-{p}">{e(NAV[p][en])}</h2>'
                                  +(f'<p>{e(t(sub))}</p>' if sub else '')+f'</header><div>{inner}</div></section>')

    # ---------- en-tête
    head=(f'<header class="hd"><div class="hd-in"><a class="logo" href="#{sid("accueil")}" aria-label="EM Visions — {e(NAV["accueil"][en].lower())}">{logo}</a>'
          f'<nav class="nav cap" aria-label="{e(t("Navigation principale"))}">{links}</nav>{lang()}{tog}{quote()}'
          f'<button type="button" class="burger cap" aria-expanded="false" aria-controls="menu">{e(t("Menu"))}</button></div></header>'
          f'<div class="menu" id="menu" hidden><div class="menu-top"><button type="button" class="cap menu-x">{e(t("Fermer"))}</button>'
          f'<a class="logo" href="#{sid("accueil")}" aria-label="EM Visions">{logo}</a><a class="cap" href="#contact">{e(t("Devis"))}</a></div>'
          f'<div class="menu-l"><nav aria-label="{e(t("Menu"))}">{links}</nav><ul><li><a href="#contact">{e(t("Demander un devis"))}</a></li><li><a href="{tool}">{e(t("Maquette 3D"))}</a></li></ul></div>'
          f'<div class="menu-foot"><div class="menu-lg"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.800 0 18M12 3c-3 3.2-3 14.800 0 18"/></g></svg>{lang()}{tog}</div>'
          f'<ul class="menu-s cap" aria-label="{e(t("Autres liens"))}"><li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li><li><a href="https://www.google.com/maps/dir/?api=1&destination=5825+rue+Jean-Talon+Est%2C+Saint-L%C3%A9onard%2C+QC+H1S+1M4" target="_blank" rel="noopener">{e(t("Itinéraire"))}</a></li>'
          f'<li><a href="{priv}">{e(t("Politique de confidentialité"))}</a></li></ul></div></div>')

    # ---------- accueil
    # accueil à la Palace : le logo de verre tourne sur lui-même et suit le doigt ou la souris ; la vidéo de fond change à chaque tour
    tiles=''.join('<figure'+(' class="cur"' if i==0 else '')+f' data-n="{e(tn(n))}"><img src="{up}img/{im}.webp" alt="{e(t(a))}" width="600" height="800"'+(' fetchpriority="high"' if i==0 else ' loading="lazy"')
                  +f'><video data-src="{up}vid/{v}.mp4" muted loop playsinline preload="none" aria-hidden="true"></video></figure>' for i,(v,im,n,a) in enumerate(HERO))
    hero=(f'<section class="hero" id="{sid("accueil")}" data-alt="{alt("accueil")}" aria-label="{e(NAV["accueil"][en])}"><div class="stage"><div class="strip">{tiles}</div>'
          f'<svg class="glass" viewBox="{LOGO_VB}" aria-hidden="true"><use href="#emlogo"/></svg><canvas class="gl" data-m="{up}img/logo-verre.webp" aria-hidden="true"></canvas>'
          f'<button type="button" class="pp" hidden aria-pressed="false" aria-label="{e(t("Mettre la vidéo en pause"))}"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path class="i-pa" d="M7 5h3.4v14H7zM13.6 5H17v14h-3.4z" fill="currentColor"/><path class="i-pl" d="M8 5v14l11-7z" fill="currentColor"/></svg></button>'
          f'<div class="hero-b"><div><p class="cap hero-k" aria-hidden="true"><span>01</span> <b>{e(tn(HERO[0][2]))}</b></p><h1>{e(t("Faites bonne impression."))}</h1></div>{quote()}</div></div></section>'
          f'<div class="wrap intro"><p class="big">{e(t("Vêtements et objets personnalisés, impression et design."))}</p><p class="cap">{e(t("Un atelier à Saint-Léonard, rue Jean-Talon Est"))}</p>'
          f'<a class="btn ghost" href="#{sid("catalogue")}">{e(t("Voir les produits"))}</a></div>')

    # ---------- services
    svc=''.join(f'<li><img src="{up}img/svc-{i+1}.webp" alt="{e(t(a))}" loading="lazy" width="800" height="600"><h3><span aria-hidden="true">{i+1:02d}</span>{e(t(n))}</h3><p>{e(t(d))}</p></li>' for i,(n,d,a) in enumerate(SVC))
    services=row('services','Six services sous un même toit.',f'<ul class="svc">{svc}</ul>')

    # ---------- réalisations
    R=REA.REAL
    works=''.join(f'<li{" hidden" if i>=SHOWN else ""}><button type="button" data-i="{i}" aria-label="{e(t("Voir le projet : ")+tn(r["n"]))}"><span class="im"><img src="{up}{r["ph"][0]["s"]}" alt="{e(t(r["ph"][0]["a"]))}" loading="lazy" width="540" height="540"></span>'
                  f'<b>{e(tn(r["n"]))}</b><small>{e(t(r["k"]))}</small></button></li>' for i,r in enumerate(R))
    real=row('realisations','Touchez un projet pour voir ses photos.',f'<ul class="grid works">{works}</ul>'
             +(f'<div class="end"><button type="button" class="btn ghost" id="more">{e(t("Voir les {n} réalisations").replace("{n}",str(len(R))))}</button></div>' if len(R)>SHOWN else ''))

    # ---------- catalogue : tous les produits dans une grille, détourés, un nom dessous
    ncol=lambda p:(f'{len(p["colors"])} '+t('couleurs')) if len(p['colors'])>1 else ('1 '+t('couleur'))
    filt=(f'<button type="button" data-cat="all" aria-pressed="true">{e(t("Tout"))}</button>'
          +''.join(f'<button type="button" data-cat="{c}" aria-pressed="false">{e(ne if en else nf)}</button>' for c,nf,ne,ids in CATS))
    prods=''.join(f'<li data-cat="{c}"><a href="{tool}?p={i}"><span class="im"><img src="{up}img/m3d/{i}.webp" alt="" loading="lazy" width="384" height="384"></span><b>{e(PROD[i][en])}</b><small>{e(ncol(PJ[i]))}</small></a></li>'
                  for c,nf,ne,ids in CATS for i in ids)
    sups=''.join(f'<li><a href="{u}" target="_blank" rel="noopener" aria-label="{e(t("Fournisseur : ")+n)}"><i class="slogo" style="--m:url({up}img/logo-{k}.webp);width:{int(w*.72)}px;aspect-ratio:{w}/{h}"></i></a></li>' for n,k,w,h,u in SUPS)
    cat=row('catalogue','Touchez un produit pour l’essayer en 3D avec votre image.',
            f'<div class="filt cap" role="group" aria-label="{e(t("Catégorie"))}">{filt}</div><p class="count" aria-live="polite"><span id="pc">{sum(len(c[3]) for c in CATS)}</span> <span data-one="{e(t("produit"))}" data-many="{e(t("produits"))}">{e(t("produits"))}</span></p><ul class="grid prods">{prods}</ul>'
            f'<p class="note"><span>{e(t("Prix sur demande : on vous les envoie personnellement, selon votre projet."))}</span><a class="u cap" data-prix href="#contact">{e(t("Demander les prix"))}</a></p>'
            f'<ul class="sups" aria-label="{e(t("Nos fournisseurs"))}">{sups}</ul>')

    # ---------- à propos
    about=row('a-propos','',f'<div class="about"><img src="{up}img/equipe.webp" alt="{e(t("Deux membres de l’équipe EM Visions examinent un chandail imprimé"))}" loading="lazy" width="830" height="443"><div>'
              f'<p>{e(ABOUT_EN if en else ABOUT_FR)}</p><ul class="team"><li><b>Eduardo Mazzonna</b><span>{e(t("Design graphique"))}</span></li><li><b>Vince Mariani</b><span>{e(t("Gestion de projets"))}</span></li></ul></div></div>')

    # ---------- contact
    fattr=f' action="{FORM_ENDPOINT}" method="post" enctype="multipart/form-data" data-send="1"' if FORM_ENDPOINT else ''
    fhid=('<input type="hidden" name="_subject" value="Demande de devis — site EM Visions"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">'
          '<input type="hidden" name="_next" value=""><input type="hidden" name="_replyto" value=""><input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">') if FORM_ENDPOINT else ''
    def fld(n,lab,ctl): return f'<label class="f"><span>{e(t(lab))}</span>{ctl}<em class="err" data-err="{n}" aria-live="polite"></em></label>'
    if CONTACT_EMAIL:
        konote=t('Vos réponses sont conservées. Vous pouvez réessayer ou nous écrire directement par courriel.'); koalt=f'<a class="u cap bymail" data-mail="{CONTACT_EMAIL}" href="mailto:{CONTACT_EMAIL}">{e(t("Écrire par courriel"))}</a>'
    else:
        konote=t('Vos réponses sont conservées. Vous pouvez réessayer, nous écrire sur Instagram ou passer à l’atelier.'); koalt=f'<a class="u cap bymail" href="{INSTAGRAM}" target="_blank" rel="noopener">{e(t("Écrire sur Instagram"))}</a>'
    qopt=''.join(f'<option>{e(t(o))}</option>' for o in ('1 à 10','11 à 50','51 à 100','101 à 500','Plus de 500','Je ne sais pas encore'))
    form=(f'<div class="fcard"><h3>{e(t("Demande de devis"))}</h3><form id="devis" novalidate{fattr}>{fhid}'
          +'<div class="f2">'+fld('nom','Nom *',f'<input name="nom" type="text" autocomplete="name" maxlength="150" required>')
          +fld('courriel','Courriel *',f'<input name="courriel" type="email" autocomplete="email" inputmode="email" required>')+'</div>'
          +fld('projet','Votre projet *',f'<textarea name="projet" rows="4" maxlength="5000" placeholder="{e(t("Ex. : 50 t-shirts avec notre logo, cartes d’affaires, enseigne…"))}" required></textarea>')
          +'<div class="f2">'+fld('qte','Quantité approximative',f'<select name="qte"><option value="">{e(t("Sélectionnez une option"))}</option>{qopt}</select>')
          +fld('echeance','Échéance','<input name="echeance" type="date">')+'</div>'
          +f'<div class="f"><span class="flab" id="fl-lab">{e(t("Joindre un visuel"))}</span><label class="drop"><input type="file" name="fichier" aria-labelledby="fl-lab" accept=".jpg,.jpeg,.png,.pdf,image/jpeg,image/png,application/pdf">'
          f'<b data-fl>{e(t("Choisir un fichier"))}</b><small data-fh>{e(t("JPG, PNG, PDF (max 10 Mo)"))}</small></label><em class="err" data-err="fichier" aria-live="polite"></em>'
          f'<p class="fnote"><a class="u" href="{tool}">{e(t("ou créer une maquette 3D"))}</a></p></div>'
          f'<button type="submit" class="btn send">{e(t("Envoyer ma demande"))}</button>'
          f'<p class="legal">{e(t("En soumettant ce formulaire, vous nous permettez de vous contacter concernant votre demande."))} <a href="{priv}">{e(t("Politique de confidentialité"))}</a></p></form>'
          f'<div class="ok" id="ok" hidden role="status" tabindex="-1"><b>{e(t("MERCI."))}</b><p>{e(t("Votre demande est bien envoyée."))}</p><p class="nt">{e(t("Nous vous répondrons par courriel."))}</p><p class="nt ref"></p><div class="okb"><button type="button" class="btn ghost again">{e(t("Nouvelle demande"))}</button></div></div>'
          f'<div class="ok" id="ko" hidden role="alert" tabindex="-1"><b>{e(t("OUPS."))}</b><p>{e(t("Votre demande n’a pas pu être envoyée."))}</p><p class="nt">{e(konote)}</p><div class="okb"><button type="button" class="btn retry">{e(t("Réessayer"))}</button>{koalt}</div></div></div>')
    FULL={'Lun':('Lundi','Monday'),'Mar':('Mardi','Tuesday'),'Mer':('Mercredi','Wednesday'),'Jeu':('Jeudi','Thursday'),'Ven':('Vendredi','Friday'),'Sam':('Samedi','Saturday'),'Dim':('Dimanche','Sunday')}
    hours=''
    if HOURS:
        hours='<ul class="hours">'+''.join((f'<li data-d="{n}"><span>{FULL[fr][en]}</span>{_h(s[0],en)} – {_h(s[1],en)}</li>' if s else f'<li class="off" data-d="{n}"><span>{FULL[fr][en]}</span>{e(t("Fermé"))}</li>') for fr,en_,n,s in WEEK)+'</ul>'
    contact=row('contact','Parlez-nous de votre idée. On vous répond avec les bonnes options.',
                f'<div class="contact"><div class="info"><address>EM Custom Design<br>5825, rue Jean-Talon Est<br>Saint-Léonard, QC H1S 1M4</address>'
                f'<a class="u cap" href="https://www.google.com/maps/dir/?api=1&destination=5825+rue+Jean-Talon+Est%2C+Saint-L%C3%A9onard%2C+QC+H1S+1M4" target="_blank" rel="noopener" aria-label="{e(t("Itinéraire (Google Maps)"))}">{e(t("Itinéraire"))}</a>{hours}</div>{form}</div>')

    frow=lambda h,items:f'<div class="ft-r"><h2 class="cap">{e(t(h))}</h2><ul>'+''.join(f'<li>{x}</li>' for x in items if x)+'</ul></div>'
    foot=(f'<footer class="ft"><div class="wrap">'
          +frow('Besoin d’aide',[f'<a href="#contact">{e(NAV["contact"][en])}</a>',f'<a href="https://www.google.com/maps/dir/?api=1&destination=5825+rue+Jean-Talon+Est%2C+Saint-L%C3%A9onard%2C+QC+H1S+1M4" target="_blank" rel="noopener">{e(t("Itinéraire"))}</a>',
                                 f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>' if CONTACT_EMAIL else ''])
          +frow('Suivez-nous',[f'<a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a>'])
          +frow('Les choses sérieuses',[f'<a href="{priv}">{e(t("Politique de confidentialité"))}</a>'])
          +f'<div class="ft-b"><p>© EM Custom Design {YEAR}. {e(t("Tous droits réservés."))}<br>5825, rue Jean-Talon Est, Saint-Léonard</p><a class="logo" href="#{sid("accueil")}" aria-label="EM Visions">{logo}</a></div></div></footer>')
    gal=(f'<div class="gal" id="gal" hidden role="dialog" aria-modal="true"><div class="gal-h"><div><button type="button" class="cap u gal-x" data-g="close">← {e(t("Retour aux réalisations"))}</button>'
         f'<button type="button" class="cap" data-g="close">{e(t("Fermer"))}</button></div></div><div class="gal-b"></div></div>')

    # ---------- données du script
    RL=[{'n':tn(r['n']),'k':t(r['k']),'a':t(r['a']),'m':up+r['m'],'t':up+r['m'],'v':(up+'vid/'+r['vk']+'.mp4') if r.get('vk') else None,
         'ph':[{'b':up+p['b'],'s':up+p['s'],'a':t(p['a'])} for p in r['ph']]} for r in R]
    TR={'dark':t('Passer au thème sombre'),'light':t('Passer au thème clair'),'pause':t('Mettre la vidéo en pause'),'play':t('Relancer la vidéo'),
        'prevPhoto':t('Photo précédente'),'nextPhoto':t('Photo suivante'),'prevProject':t('Projet précédent'),'nextProject':t('Projet suivant'),'photo':t('Photo '),'video':t('Vidéo '),
        'similarBtn':t('Demander un devis semblable'),'similar':t('Projet semblable à : '),'priceReq':t('Demande de prix : '),
        'eName':t('Indiquez votre nom'),'eMail':t('Courriel invalide'),'eProj':t('Décrivez votre projet'),'eFmt':t('Format non accepté : JPG, PNG ou PDF'),'eSize':t('Fichier trop lourd (max 10 Mo)'),
        'mbChange':t(' Mo — toucher pour changer'),'dec':'.' if en else ',','sending':t('Envoi en cours…'),'ref':t('Référence : '),'name':t('Nom'),'mail':t('Courriel'),'qty':t('Quantité approximative'),'due':t('Échéance'),
        'subject':t('Demande de devis'),'mockAdded':t('Maquette 3D ajoutée à votre demande.')}
    js=open('script.js').read().replace('%TR%',json.dumps(TR,ensure_ascii=False)).replace('%RL%',json.dumps(RL,ensure_ascii=False))
    css=open('style.css').read()
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
