// Les produits du modélisateur : vrais modèles 3D (dossier models/), couleurs proposées et zones d'impression.
// print.front / print.back : c = centre [x, y] en fraction de la demi-largeur et de la demi-hauteur du produit,
// w = largeur de la zone en fraction de la largeur du produit, ar = hauteur / largeur de la zone.
// Objets ronds (cyl) : w = largeur en radians autour de l'axe, a = angle où se trouve le devant.
const APPAREL=[['Noir','Black','#1e1f23'],['Blanc','White','#f1f0ec'],['Gris chiné','Heather grey','#9a9da3'],['Marine','Navy','#1c2a4a'],['Bleu royal','Royal blue','#1f49c7'],['Rouge','Red','#b3202a'],['Vert forêt','Forest green','#1f4d36'],['Sable','Sand','#cdbb9a']];
const WORK=[['Marine','Navy','#1c2a4a'],['Noir','Black','#17181b'],['Gris','Grey','#7d8187'],['Orange fluo','Hi-vis orange','#ff6a13'],['Jaune fluo','Hi-vis yellow','#d9ef1f']];
const BAGS=[['Naturel','Natural','#e6dcc6'],['Noir','Black','#17181b'],['Marine','Navy','#1c2a4a'],['Rouge','Red','#b3202a'],['Bleu royal','Royal blue','#1f49c7']];
const HARD=[['Blanc','White','#f4f4f1'],['Noir','Black','#17181b'],['Bleu royal','Royal blue','#1f49c7'],['Rouge','Red','#b3202a'],['Vert forêt','Forest green','#1f4d36']];
const HELMET=[['Blanc','White','#f4f4f1'],['Jaune','Yellow','#f2c81d'],['Orange','Orange','#f26a1b'],['Bleu royal','Royal blue','#1f49c7'],['Rouge','Red','#b3202a'],['Vert','Green','#2f8f4a']];
const STEEL=[['Acier','Steel','#ffffff'],['Noir','Black','#2a2b2f'],['Marine','Navy','#3a4f86'],['Rouge','Red','#c8424a'],['Vert forêt','Forest green','#3f7a5c']];
const PRINT=[['Blanc','White','#f6f6f3'],['Noir','Black','#17181b'],['Bleu royal','Royal blue','#1f49c7'],['Rouge','Red','#b3202a']];

export const PRODUCTS=[
{id:'tshirt',n:['T-shirt','T-shirt'],colors:APPAREL,fabric:1,print:{front:{c:[0,.2],w:.3,ar:1.25},back:{c:[0,.25],w:.34,ar:1.3}}},
{id:'longsleeve',n:['T-shirt manches longues','Long-sleeve tee'],colors:APPAREL,fabric:1,print:{front:{c:[0,.05],w:.2,ar:1.1},back:{c:[0,.1],w:.24,ar:1.2}}},
{id:'tank',n:['Camisole','Tank top'],colors:APPAREL,fabric:1,print:{front:{c:[0,.1],w:.5,ar:1.2},back:{c:[0,.1],w:.5,ar:1.2}}},
{id:'polo',n:['Polo','Polo shirt'],colors:APPAREL,fabric:1,print:{front:{c:[.2,.3],w:.14,ar:1},back:{c:[0,.25],w:.34,ar:1.2}}},
{id:'crewneck',n:['Coton ouaté','Crewneck sweatshirt'],colors:APPAREL,fabric:1,print:{front:{c:[0,.2],w:.3,ar:1.1},back:{c:[0,.25],w:.34,ar:1.2}}},
{id:'hoodie',n:['Chandail à capuchon','Hoodie'],colors:APPAREL,fabric:1,print:{front:{c:[0,-.02],w:.3,ar:1},back:{c:[0,-.05],w:.36,ar:1.2}}},
{id:'jacket',n:['Manteau de travail','Work jacket'],colors:WORK,fabric:1,print:{front:{c:[.17,.2],w:.1,ar:.8},back:{c:[0,.15],w:.26,ar:.9}}},
{id:'vest',n:['Dossard haute visibilité','Hi-vis vest'],colors:[['Jaune fluo','Hi-vis yellow','#d9ef1f']],print:{front:{c:[.25,.4],w:.16,ar:1},back:{c:[0,.3],w:.4,ar:.8}}},
{id:'pants',n:['Pantalon de jogging','Joggers'],colors:APPAREL,fabric:1,print:{front:{c:[.5,.45],w:.22,ar:1.3}}},
{id:'cap',n:['Casquette','Cap'],colors:APPAREL,fabric:1,print:{front:{c:[0,.2],w:.4,ar:.6}}},
{id:'bucket',n:['Chapeau bob','Bucket hat'],colors:APPAREL,fabric:1,print:{front:{c:[0,.2],w:.3,ar:.6}}},
{id:'beanie',n:['Tuque','Beanie'],colors:APPAREL,fabric:1,print:{front:{c:[0,-.21],w:.3,ar:.4,depth:.15,nt:-.3}}},
{id:'hardhat',n:['Casque de chantier','Hard hat'],colors:HELMET,mat:{metalness:0,roughness:.3,metalnessMap:null,roughnessMap:null},print:{front:{c:[0,.2],w:.3,ar:.7}}},
{id:'tote',n:['Sac fourre-tout','Tote bag'],colors:BAGS,fabric:1,rot:[0,Math.PI/2,0],print:{front:{c:[0,-.45],w:.62,ar:1.1},back:{c:[0,-.45],w:.62,ar:1.1}}},
{id:'drawstring',n:['Sac à cordon','Drawstring bag'],colors:BAGS,fabric:1,print:{front:{c:[0,-.25],w:.4,ar:1}}},
{id:'mug',n:['Tasse','Mug'],colors:HARD,rot:[0,-Math.PI/2,0],print:{front:{cyl:1,axis:[-.33,0],c:[0,0],w:1.7,ar:.95}}},
{id:'bottle',n:['Bouteille isotherme','Insulated bottle'],colors:STEEL,print:{front:{cyl:1,c:[0,-.1],w:1.5,ar:1.4}}},
{id:'travel',n:['Tasse de voyage','Travel mug'],colors:HARD,rot:[0,-Math.PI/2,0],print:{front:{cyl:1,axis:[-.31,0],c:[0,-.4],w:1.5,ar:1}}},
{id:'pillow',n:['Coussin','Cushion'],colors:BAGS,fabric:1,print:{front:{c:[0,0],w:.5,ar:1,depth:.5,nt:-.2}}},
{id:'umbrella',n:['Parapluie','Umbrella'],colors:HARD,fabric:1,upv:[.65,.7,-.31],rot:[0,Math.PI/8,0],view:{pitch:.45},print:{front:{n:[0,.72,.69],c:[0,-.1],w:.26,ar:.7,depth:.4}}},
{id:'rollup',n:['Bannière rétractable','Roll-up banner'],colors:PRINT,rot:[0,-Math.PI/2,0],print:{front:{c:[0,.03],w:.9,ar:2.2}}},
{id:'banner',n:['Bannière suspendue','Hanging banner'],colors:PRINT,fabric:1,rot:[0,Math.PI/2,0],print:{front:{c:[0,-.08],w:.8,ar:.95}}},
];
