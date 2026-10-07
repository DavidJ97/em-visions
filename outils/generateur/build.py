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
EN2={'Faites bonne impression':'Make a good impression','Vêtements et objets personnalisés pour donner forme à vos idées.':'Custom apparel and objects that give shape to your ideas.',
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
    other='../' if en else 'en/'
    tool='mockup/' if en else 'maquette/'; priv='privacy/' if en else 'confidentialite/'
    arr='<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h16M13 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    logo=f'<svg viewBox="{LOGO_VB}" aria-hidden="true"><use href="#emlogo"/></svg>'
    def title(tag,lines,cls):
        return f'<{tag} class="{cls}">'+''.join(e(x)+'<br>' for x in lines[:-1])+f'<span>{e(lines[-1])}'+('' if lines[-1].endswith('?') else '<i aria-hidden="true"></i>')+f'</span></{tag}>'
    def sec_head(lines,lead): return f'<div class="sec-h">{title("h2",lines,"h2")}<p class="lead">{e(lead)}</p></div>'
    cur='aria-current="true"'
    def lang():
        fr=f'<a href="../#accueil" data-other="../" hreflang="fr" lang="fr">FR</a>' if en else f'<a href="#accueil" {cur} hreflang="fr" lang="fr">FR</a>'
        an=f'<a href="#home" {cur} hreflang="en" lang="en">EN</a>' if en else f'<a href="en/#home" data-other="en/" hreflang="en" lang="en">EN</a>'
        return f'<span class="lang" role="group" aria-label="{e(t("Langue"))}">{fr}<i></i>{an}</span>'
    tog='<button type="button" class="tog"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg></button>'
    links=''.join(f'<a href="#{sid(p)}">{e(NAV[p][en])}</a>' for p in ORDER)
    quote=lambda cls='',label='Demander un devis': f'<a class="btn {cls}" href="#contact">{e(t(label))}{arr}</a>'

    # ---------- en-tête
    head=(f'<header class="hd"><div class="hd-in"><a class="logo" href="#{sid("accueil")}" aria-label="EM Visions — {e(NAV["accueil"][en].lower())}">{logo}</a>'
          f'<nav class="nav" aria-label="{e(t("Navigation principale"))}">{links}</nav>{lang()}{tog}{quote("sm")}'
          f'<button type="button" class="burger" aria-label="{e(t("Ouvrir le menu"))}" aria-expanded="false" aria-controls="menu"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div></header>'
          f'<div class="menu" id="menu" hidden><div class="menu-top"><a class="logo" href="#{sid("accueil")}" aria-label="EM Visions">{logo}</a>'
          f'<button type="button" class="burger menu-x" style="display:grid" aria-label="{e(t("Fermer le menu"))}"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div>'
          f'<nav aria-label="{e(t("Menu"))}">{links}</nav>{quote()}<div class="menu-foot">{lang()}{tog}</div></div>')

    # ---------- accueil
    pin='<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5a7 7 0 0 0-7 7c0 5.2 7 12 7 12s7-6.8 7-12a7 7 0 0 0-7-7z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="9.5" r="2.4" fill="currentColor"/></svg>'
    clock='<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v5l3.4 2.2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    h1l=['Make','a good','impression'] if en else ['Faites','bonne','impression']
    hero=(f'<section id="{sid("accueil")}" data-alt="{alt("accueil")}" aria-label="{e(NAV["accueil"][en])}"><div class="wrap hero"><div>'
          f'{title("h1",h1l,"h1")}<p class="lead">{e(t("Vêtements et objets personnalisés pour donner forme à vos idées."))}</p>'
          f'<div class="hero-a">{quote("shine")}<a class="btn ghost" href="#{sid("realisations")}">{e(t("Voir nos réalisations"))}</a></div>'
          f'<ul class="facts"><li>{pin}<span><b>5825, rue Jean-Talon Est</b>, Saint-Léonard</span></li>'+(f'<li>{clock}<span id="today"></span></li>' if HOURS else '')+'</ul></div>'
          f'<figure class="hero-m"><img src="{up}img/atelier-poster.webp" alt="{e(t("Devanture de l’atelier EM Custom Design, rue Jean-Talon Est"))}" width="626" height="784" fetchpriority="high">'
          f'<video data-src="{up}vid/atelier.mp4" poster="{up}img/atelier-poster.webp" muted loop playsinline preload="none" aria-hidden="true"></video>'
          f'<button type="button" class="pp" hidden aria-pressed="false" aria-label="{e(t("Mettre la vidéo en pause"))}"><svg class="ic b" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6v12M15 6v12" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/></svg>'
          f'<svg class="ic a" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6.5v11l9-5.5z" fill="currentColor"/></svg></button>'
          f'<figcaption>{e(t("L’atelier, rue Jean-Talon Est"))}</figcaption></figure></div></section>')

    # ---------- services
    def sec(p,inner): return f'<section class="sec" id="{sid(p)}" data-alt="{alt(p)}" aria-label="{e(NAV[p][en])}"><div class="wrap">{inner}</div></section>'
    svc=''.join(f'<li><img src="{up}img/svc-{i+1}.webp" alt="{e(t(a))}" loading="lazy" width="800" height="600"><div class="tt"><span class="n" aria-hidden="true">{i+1:02d}</span><h3>{e(t(n))}</h3></div><p>{e(t(d))}</p></li>' for i,(n,d,a) in enumerate(SVC))
    services=sec('services',sec_head(['From idea','to matter'] if en else ['De l’idée','à la matière'],t('Six services sous un même toit. Dites-nous ce qu’il vous faut, on s’occupe du reste.'))
                 +f'<ul class="svc">{svc}</ul><div class="end">{quote("","Parler de mon projet")}</div>')

    # ---------- réalisations
    R=REA.REAL
    works=''.join(f'<li{" hidden" if i>=SHOWN else ""}><button type="button" data-i="{i}" aria-label="{e(t("Voir le projet : ")+tn(r["n"]))}"><span class="im"><img src="{up}{r["ph"][0]["s"]}" alt="{e(t(r["ph"][0]["a"]))}" loading="lazy" width="540" height="675"></span><b>{e(tn(r["n"]))}</b><small>{e(t(r["k"]))}</small></button></li>' for i,r in enumerate(R))
    real=sec('realisations',sec_head(['The work','speaks'] if en else ['Le travail','parle'],t('Des idées devenues réelles. Touchez un projet pour voir ses photos.'))
             +f'<ul class="works">{works}</ul>'+(f'<div class="end"><button type="button" class="btn ghost" id="more">{e(t("Voir les {n} réalisations").replace("{n}",str(len(R))))}</button></div>' if len(R)>SHOWN else ''))

    # ---------- catalogue
    catnav=(f'<li><button type="button" data-cat="all" aria-pressed="true">{e(t("Tous les produits"))}<small>{len(PROD)}</small></button></li>'
            +''.join(f'<li><button type="button" data-cat="{c}" aria-pressed="false">{e(ne if en else nf)}<small>{len(ids)}</small></button></li>' for c,nf,ne,ids in CATS))
    prods=''.join(f'<li data-cat="{c}"><a href="{tool}?p={i}"><img src="{up}img/m3d/{i}.webp" alt="" loading="lazy" width="384" height="384"><b>{e(PROD[i][en])}</b><span>{e(t("Essayer en 3D"))}</span></a></li>' for c,nf,ne,ids in CATS for i in ids)
    sups=''.join(f'<li><a href="{u}" target="_blank" rel="noopener" aria-label="{e(t("Fournisseur : ")+n)}"><i class="slogo" style="--m:url({up}img/logo-{k}.webp);width:{w}px;aspect-ratio:{w}/{h}"></i></a></li>' for n,k,w,h,u in SUPS)
    cat=sec('catalogue',sec_head(['Choose','your medium'] if en else ['Choisissez','votre support'],t('Choisissez un produit, puis essayez-le avec votre image dans le modélisateur 3D.'))
            +f'<div class="cat"><div class="cat-nav"><span class="lab" id="catlab">{e(t("Catégorie"))}</span><ul aria-labelledby="catlab">{catnav}</ul></div><div>'
            f'<div class="feat"><img src="{up}img/cat-casquettes.webp" alt="{e(t("Casquettes brodées « em » blanches et bleues"))}" loading="lazy" width="530" height="520"><div><h3>{e(t("Essayez-le avant de commander"))}</h3>'
            f'<p>{e(t("Posez votre logo sur le produit, faites-le tourner, puis joignez la maquette à votre demande de devis."))}</p><a class="btn" href="{tool}">{e(t("Ouvrir le modélisateur 3D"))}{arr}</a></div></div>'
            f'<ul class="prods">{prods}</ul></div></div>'
            f'<div class="sups"><span class="lab">{e(t("Nos fournisseurs"))}</span><ul>{sups}</ul></div>'
            f'<div class="band"><div><h3>{e(t("Les prix, on vous les envoie"))}</h3><p>{e(t("Les prix ne sont pas affichés : on vous les envoie personnellement, selon votre projet."))}</p></div>'
            f'<a class="btn white" data-prix href="#contact">{e(t("Demander les prix"))}{arr}</a></div>')

    # ---------- à propos
    about=sec('a-propos',f'<div class="about"><figure><img src="{up}img/equipe.webp" alt="{e(t("Deux membres de l’équipe EM Visions examinent un chandail imprimé"))}" loading="lazy" width="835" height="450"></figure><div>'
              +title('h2',['The people','behind','the print'] if en else ['Les gens','derrière','l’impression'],'h2')
              +f'<div class="team"><div><b>Eduardo Mazzonna</b><span>{e(t("Design graphique"))}</span></div><div><b>Vince Mariani</b><span>{e(t("Gestion de projets"))}</span></div></div>'
              f'<p>{e(ABOUT_EN if en else ABOUT_FR)}</p></div></div>')

    # ---------- contact
    stp=[('Votre idée','Dites-nous ce que vous avez en tête : type d’imprimé, usage, format ou toute autre idée. Pas besoin d’avoir tous les détails pour commencer.'),
         ('Les détails','Précisez ce qui compte : quantité approximative, échéance, fichiers ou inspirations. Plus on en sait, plus on peut vous proposer les bonnes options.'),
         ('On en parle','On regarde votre demande et on vous revient rapidement avec nos recommandations et un devis clair.')]
    on=' class="on"'
    steps=''.join(f'<li{on if i==0 else ""}><span class="n" aria-hidden="true">{i+1:02d}</span><h3>{e(t(a))}</h3><p>{e(t(b))}</p></li>' for i,(a,b) in enumerate(stp))
    fattr=f' action="{FORM_ENDPOINT}" method="post" enctype="multipart/form-data" data-send="1"' if FORM_ENDPOINT else ''
    fhid=('<input type="hidden" name="_subject" value="Demande de devis — site EM Visions"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">'
          '<input type="hidden" name="_next" value=""><input type="hidden" name="_replyto" value=""><input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">') if FORM_ENDPOINT else ''
    def fld(n,lab,ctl): return f'<label class="f"><span>{e(t(lab))}</span>{ctl}<em class="err" data-err="{n}" aria-live="polite"></em></label>'
    if CONTACT_EMAIL:
        konote=t('Vos réponses sont conservées. Vous pouvez réessayer ou nous écrire directement par courriel.'); koalt=f'<a class="txt bymail" data-mail="{CONTACT_EMAIL}" href="mailto:{CONTACT_EMAIL}">{e(t("Écrire par courriel"))}</a>'
    else:
        konote=t('Vos réponses sont conservées. Vous pouvez réessayer, nous écrire sur Instagram ou passer à l’atelier.'); koalt=f'<a class="txt bymail" href="{INSTAGRAM}" target="_blank" rel="noopener">{e(t("Écrire sur Instagram"))}</a>'
    form=(f'<div class="fcard"><span class="ftag" aria-hidden="true">{e(t("Devis"))}</span><h3>{e(t("Demande de devis"))}</h3><form id="devis" novalidate{fattr}>{fhid}'
          +fld('nom','Nom *',f'<input name="nom" type="text" autocomplete="name" maxlength="150" placeholder="{e(t("Votre nom"))}" required>')
          +fld('courriel','Courriel *',f'<input name="courriel" type="email" autocomplete="email" inputmode="email" placeholder="{e(t("votre@courriel.com"))}" required>')
          +fld('projet','Votre projet *',f'<textarea name="projet" rows="4" maxlength="5000" placeholder="{e(t("Décrivez-nous votre projet en quelques mots..."))}" required></textarea>')
          +'<div class="f2">'+fld('qte','Quantité approximative',f'<input name="qte" type="number" min="1" inputmode="numeric" placeholder="{e(t("Ex. : 50, 100, 500, etc."))}">')
          +fld('echeance','Échéance souhaitée','<input name="echeance" type="date">')+'</div>'
          +f'<div class="f"><span class="flab" id="fl-lab">{e(t("Joindre un visuel"))}</span><label class="drop"><input type="file" name="fichier" aria-labelledby="fl-lab" accept=".jpg,.jpeg,.png,.pdf,image/jpeg,image/png,application/pdf">'
          '<svg width="34" height="34" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 16V4M7 9l5-5 5 5M4 17v2a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
          f'<b data-fl>{e(t("Déposez un fichier ici"))}</b><small data-fh>{e(t("ou touchez pour le choisir — JPG, PNG, PDF (max 10 Mo)"))}</small></label><em class="err" data-err="fichier" aria-live="polite"></em>'
          f'<a class="txt" href="{tool}">{e(t("ou créer une maquette 3D"))}</a></div>'
          f'<button type="submit" class="btn shine send">{e(t("Envoyer ma demande"))}{arr}</button>'
          f'<p class="legal">{e(t("En soumettant ce formulaire, vous nous permettez de vous contacter concernant votre demande."))} <a href="{priv}">{e(t("Politique de confidentialité"))}</a></p></form>'
          f'<div class="ok" id="ok" hidden role="status" tabindex="-1"><b>{e(t("MERCI."))}</b><p>{e(t("Votre demande est bien envoyée."))}</p><p class="note">{e(t("Nous vous répondrons par courriel."))}</p><p class="note ref"></p><div class="okb"><button type="button" class="btn ghost again">{e(t("Nouvelle demande"))}</button></div></div>'
          f'<div class="ok" id="ko" hidden role="alert" tabindex="-1"><b>{e(t("OUPS."))}</b><p>{e(t("Votre demande n’a pas pu être envoyée."))}</p><p class="note">{e(konote)}</p><div class="okb"><button type="button" class="btn retry">{e(t("Réessayer"))}</button>{koalt}</div></div></div>')
    hours=''
    if HOURS:
        cells=''.join((f'<li data-d="{n}"><b>{en_ if en else fr}</b><span>{_h(s[0],en)}<br>{_h(s[1],en)}</span></li>' if s else f'<li class="off" data-d="{n}"><b>{en_ if en else fr}</b><span>{e(t("Fermé"))}</span></li>') for fr,en_,n,s in WEEK)
        hours=f'<div><span class="lab">{e(t("Heures d’ouverture"))}</span><ul class="hgrid">{cells}</ul></div>'
    contact=sec('contact',sec_head(['What are we','making','together?'] if en else ['On fait quoi','ensemble ?'],t('Parlez-nous de votre idée. On vous répond avec les bonnes options.'))
                +f'<div class="contact"><ol class="steps">{steps}</ol>{form}</div>'
                f'<div class="infos"><div><span class="lab">{e(t("Où nous trouver"))}</span><address>5825, rue Jean-Talon Est<br>Saint-Léonard, QC H1S 1M4</address>'
                f'<a class="btn ghost sm" href="https://www.google.com/maps/dir/?api=1&destination=5825+rue+Jean-Talon+Est%2C+Saint-L%C3%A9onard%2C+QC+H1S+1M4" target="_blank" rel="noopener" aria-label="{e(t("Itinéraire (Google Maps)"))}">{e(t("Itinéraire"))}{arr}</a></div>'
                f'{hours}<div><img src="{up}img/devanture.webp" alt="{e(t("Devanture de l’atelier EM Custom Design, rue Jean-Talon Est"))}" loading="lazy" width="626" height="470"></div></div>')

    foot=(f'<footer class="ft"><div class="wrap ft-in"><a class="logo" href="#{sid("accueil")}" aria-label="EM Visions">{logo}</a><p>EM Custom Design<br>5825, rue Jean-Talon Est, Saint-Léonard</p>'
          f'<ul>'+(f'<li><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></li>' if CONTACT_EMAIL else '')+f'<li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li><li><a href="{priv}">{e(t("Politique de confidentialité"))}</a></li></ul></div></footer>')
    gal=(f'<div class="gal" id="gal" hidden role="dialog" aria-modal="true"><div class="gal-h"><div><button type="button" class="btn ghost sm" data-g="close">{e(t("Retour aux réalisations"))}</button>'
         f'<button type="button" class="burger gal-x" style="display:grid" data-g="close" aria-label="{e(t("Fermer"))}"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div></div><div class="gal-b"></div></div>')

    # ---------- données du script
    RL=[{'n':tn(r['n']),'k':t(r['k']),'a':t(r['a']),'m':up+r['m'],'t':up+r['m'],'v':(up+'vid/'+r['vk']+'.mp4') if r.get('vk') else None,
         'ph':[{'b':up+p['b'],'s':up+p['s'],'a':t(p['a'])} for p in r['ph']]} for r in R]
    TR={'dark':t('Passer au thème sombre'),'light':t('Passer au thème clair'),'pause':t('Mettre la vidéo en pause'),'play':t('Relancer la vidéo'),'today':t('Aujourd’hui : '),'to':t(' à '),'todayClosed':t('Aujourd’hui : fermé'),
        'prevPhoto':t('Photo précédente'),'nextPhoto':t('Photo suivante'),'prevProject':t('Projet précédent'),'nextProject':t('Projet suivant'),'photo':t('Photo '),'video':t('Vidéo '),
        'similarBtn':t('Un projet semblable ? Demander un devis'),'similar':t('Projet semblable à : '),'priceReq':t('Demande de prix : '),
        'eName':t('Indiquez votre nom'),'eMail':t('Courriel invalide'),'eProj':t('Décrivez votre projet'),'eQty':t('Nombre entier ≥ 1'),'eFmt':t('Format non accepté : JPG, PNG ou PDF'),'eSize':t('Fichier trop lourd (max 10 Mo)'),
        'mbChange':t(' Mo — toucher pour changer'),'dec':'.' if en else ',','sending':t('Envoi en cours…'),'ref':t('Référence : '),'name':t('Nom'),'mail':t('Courriel'),'qty':t('Quantité approximative'),'due':t('Échéance'),
        'subject':t('Demande de devis'),'mockAdded':t('Maquette 3D ajoutée à votre demande.')}
    WK={n:[_h(s[0],en),_h(s[1],en)] if s else None for fr,en_,n,s in WEEK}
    js=open('script.js').read().replace('%TR%',json.dumps(TR,ensure_ascii=False)).replace('%RL%',json.dumps(RL,ensure_ascii=False)).replace('%WEEK%',json.dumps(WK))
    css=open('style.css').read()
    headjs='(function(){var t;try{t=localStorage.getItem("em-theme")}catch(e){}document.documentElement.dataset.theme=t==="dark"?"dark":"light"})();'+loader.HEAD
    return (f'<!doctype html><html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{head_seo(L,up)}<script>{headjs}</script>'
            f'<style>{fontface(up,swap=False)}{css}{loader.CSS}</style></head><body>{loader.html(LOGO_VB)}<a class="sr skip" href="#{sid("services")}">{e(t("Aller au contenu"))}</a>'
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
