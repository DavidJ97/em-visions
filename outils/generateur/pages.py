H1={'f':'Archivo','w':900,'wd':62.5,'css':'-webkit-text-stroke:3px currentColor;letter-spacing:-.03em','mode':'sx'}
H1K=dict(H1)
NAV={'f':'Archivo','w':400,'mode':'ls'}; NAVB={'f':'Archivo','w':700,'mode':'ls'}
SUB={'f':'Archivo','w':300,'mode':'ls'}
CTA={'f':'Archivo','w':700,'wd':62.5,'mode':'sx'}
NUM={'f':'Archivo','w':900,'wd':62.5,'mode':'sx'}
TITLE={'f':'Archivo','w':700,'wd':62.5,'mode':'sx'}
DESC={'f':'Archivo','w':300,'mode':'ls'}
ROLE={'f':'Archivo','w':400,'mode':'ls'}
LBL={'f':'Archivo','w':600,'mode':'ls'}
PH={'f':'Archivo','w':400,'mode':'ls'}
BTN={'f':'Archivo','w':600,'mode':'ls'}
ADDR={'f':'Archivo','w':600,'mode':'ls'}
SMALL={'f':'Archivo','w':400,'mode':'ls'}
NAVL=['ACCUEIL','SERVICES','RÉALISATIONS','CATALOGUE','À PROPOS','CONTACT']
NAVH=['accueil','services','realisations','catalogue','a-propos','contact']
def nav(active):
    return [dict(region=(492,43,1152,71),cls='w',split='h',lines=NAVL,spec=[NAVB if i==active else NAV for i in range(6)],
                 href=['#'+h for h in NAVH],group='nav',minarea=2),
            dict(region=(1296,46,1328,72),cls='b',lines=['FR'],spec=[NAVB],href=['#'],group='lang'),
            dict(region=(1342,46,1382,72),cls='w',lines=['EN'],spec=[NAV],href=['#'],group='lang')]
CAROUSEL_ERASE=[('circle',(1280,858,27)),('circle',(1466,858,27)),('rect',(1252,900,1496,915))]
PAGES={
'accueil':dict(nav=0,blocks=nav(0)+[
  dict(region=(62,200,486,568),cls='w',lines=['FAITES','BONNE','IMPRESSION'],spec=H1,tag='h1',group='h1',minarea=40),
  dict(region=(66,612,492,686),cls='w',lines=['Vêtements et objets personnalisés','pour donner forme à vos idées.'],spec=SUB,tag='p',group='sub'),
  dict(region=(104,738,332,778),cls='k',lines=['Demander un devis'],spec=CTA,link=('#contact',(78,718,416,802)),group='cta'),
  dict(region=(1335,845,1366,873),cls='w',lines=['01'],spec=NAVB,id='count',group='count'),
  dict(region=(1366,845,1410,873),cls='w',lines=['/ 05'],spec=NAV,group='count'),
 ],erase=CAROUSEL_ERASE,carousel=True),
'services':dict(nav=1,blocks=nav(1)+[
  dict(region=(62,175,476,548),cls='w',lines=['DE L’IDÉE','À LA','MATIÈRE'],spec=H1,tag='h1',group='h1',minarea=40),
  *[dict(region=r,cls='b',lines=[t],spec=NUM,group='num') for r,t in [((70,582,134,644),'01'),((70,677,134,739),'02'),((70,772,134,834),'03'),((444,582,506,644),'04'),((444,677,506,739),'05'),((444,772,506,834),'06')]],
  *[dict(region=r,cls='w',lines=L,spec=[TITLE]*nt+[DESC]*(len(L)-nt),group='svc') for r,L,nt in [
     ((168,580,410,662),['DESIGN GRAPHIQUE','Des visuels qui marquent','votre identité.'],1),
     ((168,675,410,758),['IMPRESSION','Des supports de qualité','pour vos projets.'],1),
     ((168,770,410,873),['VÊTEMENTS','PERSONNALISÉS','Des textiles uniques','à votre image.'],2),
     ((545,580,805,662),['IMPRESSION 3D','Des idées qui prennent','forme.'],1),
     ((545,675,805,758),['SITES WEB','Des plateformes sur mesure','pour propulser votre marque.'],1),
     ((545,770,792,853),['APPLICATIONS','Des outils performants','pour vos besoins spécifiques.'],1)]],
  dict(region=(112,892,382,943),cls='k',lines=['Parler de mon projet'],spec=CTA,link=('#contact',(84,878,478,958)),group='cta'),
 ]),
'realisations':dict(nav=2,blocks=nav(2)+[
  dict(region=(62,195,448,578),exclude=[(180,180,460,224),(412,190,470,332)],cls='w',lines=['LE','TRAVAIL','PARLE'],spec=H1,tag='h1',group='h1',minarea=40),
  dict(region=(66,628,425,664),cls='w',lines=['Des idées devenues réelles.'],spec=SUB,tag='p',group='sub'),
  dict(region=(122,738,310,780),cls='k',lines=['Voir le projet'],spec=CTA,link=('#',(78,718,418,802)),id='voir',group='cta'),
  dict(region=(1335,845,1366,873),cls='w',lines=['01'],spec=NAVB,id='count',group='count'),
  dict(region=(1366,845,1410,873),cls='w',lines=['/ 05'],spec=NAV,group='count'),
 ],erase=CAROUSEL_ERASE,carousel=True),
'catalogue':dict(nav=3,blocks=nav(3)+[
  dict(region=(62,160,636,388),cls='w',lines=['CHOISISSEZ','VOTRE SUPPORT'],spec=H1,tag='h1',group='h1',minarea=40),
  dict(region=(66,405,450,468),cls='w',lines=['Des fournisseurs de confiance','pour concrétiser vos idées.'],spec=SUB,tag='p',group='sub'),
  dict(region=(428,514,606,547),cls='w',lines=['Voir le fournisseur'],spec={'f':'Archivo','w':600,'mode':'ls'},group='vf',id='vf',minarea=2),
  *[dict(region=r,cls='w',lines=[t],spec=TITLE,group='sup',row=i) for i,(r,t) in enumerate([((96,506,345,556),'S&S ACTIVEWEAR'),((96,574,396,624),'CANADA SPORTSWEAR'),((96,640,210,690),'FABRIK'),((96,705,186,755),'ESIDE'),((96,770,316,820),'JUST LIKE HERO'),((96,836,216,886),'PROJOB')])],
 ]),
'a-propos':dict(nav=4,blocks=nav(4)+[
  dict(region=(1024,222,1524,558),cls='w',lines=['LES GENS','DERRIÈRE','L’IMPRESSION'],spec=H1,tag='h1',group='h1',minarea=40),
  dict(region=(1026,622,1256,662),cls='w',lines=['EDUARDO MAZZONNA'],spec=TITLE,group='name'),
  dict(region=(1320,622,1486,662),cls='w',lines=['VINCE MARIANI'],spec=TITLE,group='name'),
  dict(region=(1026,664,1258,692),cls='w',lines=['DESIGN GRAPHIQUE'],spec=ROLE,group='role'),
  dict(region=(1320,664,1556,692),cls='w',lines=['GESTION DE PROJETS'],spec=ROLE,group='role'),
  dict(region=(1128,786,1396,832),cls='k',lines=['Découvrir notre équipe'],spec=CTA,link=('#',(1086,764,1484,856)),group='cta'),
 ]),
'contact':dict(nav=5,blocks=nav(5)+[
  dict(region=(68,148,428,400),cls='w',lines=['ON EN','PARLE ?'],spec=H1,tag='h1',group='h1',minarea=40),
  dict(region=(70,410,460,497),cls='w',lines=['Un projet, une idée, une question ?','On est là pour en discuter. Écrivez-nous','et on vous répond rapidement.'],spec=SUB,tag='p',group='sub'),
  dict(region=(140,536,430,598),cls='w',lines=['5825, rue Jean-Talon Est','Saint-Léonard, QC H1S 1M4'],spec=ADDR,tag='address',group='addr'),
  dict(region=(95,866,194,898),cls='w',lines=['Itinéraire'],spec=ADDR,link=('https://goo.gl/maps/oVVn3rjDxX8nbqMw5',(74,852,248,908)),group='addr'),
  dict(region=(948,172,1470,250),cls='k',lines=['DEMANDE DE DEVIS'],spec=H1K,tag='h2',group='h2',minarea=40),
  *[dict(region=r,cls='k',lines=[t],spec=LBL,group='lbl',label=f) for r,t,f in [((950,264,1012,292),'Nom *','nom'),((950,355,1037,383),'Courriel *','courriel'),((950,447,1070,475),'Votre projet *','projet'),((950,605,1152,634),'Quantité approximative','qte'),((950,697,1100,725),'Joindre un visuel','fichier')]],
  *[dict(region=r,cls='g',lines=[t],spec=PH,group='ph',ph=f,minarea=2) for r,t,f in [((968,303,1062,330),'Votre nom','nom'),((968,395,1128,422),'votre@courriel.com','courriel'),((968,488,1336,514),'Décrivez-nous votre projet en quelques mots...','projet'),((968,645,1146,672),'Ex. : 50, 100, 500, etc.','qte')]],
  dict(region=(1014,744,1150,770),cls='k',lines=['Choisir un fichier'],spec=LBL,id='filelabel',group='file'),
  dict(region=(1014,767,1212,790),cls='g',lines=['JPG, PNG, PDF (max 10 Mo)'],spec=PH,id='filehint',group='file'),
  dict(region=(1110,828,1302,858),cls='wt',lines=['Demander un devis'],spec=BTN,group='btn'),
  dict(region=(1026,882,1422,920),cls='k2',lines=['En soumettant ce formulaire, vous nous permettez de vous contacter','concernant votre demande.'],spec=SMALL,group='small'),
 ],form=True),
}
