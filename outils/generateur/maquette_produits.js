// Les vingt produits du modélisateur. Chaque produit décrit sa forme, ses couleurs et la zone d'impression.
// Vêtements et sacs (« soft ») : dessinés à plat dans un repère 1000 × 1250, puis gonflés en volume.
const APPAREL=[['Noir','Black','#17181b'],['Blanc','White','#f1f0ec'],['Gris chiné','Heather grey','#9a9da3'],['Marine','Navy','#1c2a4a'],['Bleu royal','Royal blue','#1f49c7'],['Rouge','Red','#b3202a'],['Vert forêt','Forest green','#1f4d36'],['Sable','Sand','#cdbb9a']];
const HIVIS=[['Jaune fluo','Hi-vis yellow','#d9ef1f'],['Orange fluo','Hi-vis orange','#ff6a13']];
const WORK=[['Marine','Navy','#1c2a4a'],['Noir','Black','#17181b'],['Orange fluo','Hi-vis orange','#ff6a13'],['Jaune fluo','Hi-vis yellow','#d9ef1f']];
const BAGS=[['Naturel','Natural','#e6dcc6'],['Noir','Black','#17181b'],['Marine','Navy','#1c2a4a'],['Rouge','Red','#b3202a'],['Bleu royal','Royal blue','#1f49c7']];
const HARD=[['Blanc','White','#f4f4f1'],['Noir','Black','#17181b'],['Bleu royal','Royal blue','#1f49c7'],['Rouge','Red','#b3202a'],['Vert forêt','Forest green','#1f4d36'],['Acier','Steel','#b9bdc2']];

const lum=h=>{const n=parseInt(h.slice(1),16);return(.299*(n>>16)+.587*(n>>8&255)+.114*(n&255))/255};
const ink=(col,a=1)=>lum(col)>.5?`rgba(0,0,0,${.2*a})`:`rgba(255,255,255,${.16*a})`;
const fillP=(c,d)=>{const p=new Path2D(d);c.fill(p);c.stroke(p)};
const line=(c,d,w=4)=>{c.lineWidth=w;c.stroke(new Path2D(d))};
const TEE=n=>`M395 110 L262 148 L62 318 L140 452 L222 388 C220 600 220 800 222 985 Q500 1012 778 985 C780 800 780 600 778 388 L860 452 L938 318 L738 148 L605 110 Q500 ${n} 395 110 Z`;
const LONG=(n,t=110)=>`M395 ${t} L262 148 L150 250 L40 820 L140 850 L225 420 C222 620 222 820 224 1000 Q500 1028 776 1000 C778 820 778 620 775 420 L860 850 L960 820 L850 250 L738 148 L605 ${t} Q500 ${n} 395 ${t} Z`;
const cuffs=(c,col)=>{c.strokeStyle=ink(col);line(c,'M50 778 L148 808',5);line(c,'M950 778 L852 808',5);line(c,'M224 948 Q500 974 776 948',5)};
const band=(c,d,w,a,b)=>{c.lineCap='butt';c.strokeStyle=a;line(c,d,w);c.strokeStyle=b;line(c,d,w*.42)};
const seams=(c,col,y)=>{c.strokeStyle=ink(col,.5);line(c,`M224 ${y} L262 152`,3);line(c,`M776 ${y} L738 152`,3)};

export const PRODUCTS=[
{id:'tshirt',n:['T-shirt','T-shirt'],kind:'soft',colors:APPAREL,thick:.07,sides:['front','back'],
 area:{front:[350,290,300,400],back:[330,240,340,480]},
 shape:(c,s)=>fillP(c,TEE(s==='front'?198:142)),
 details:(c,s,col)=>{c.strokeStyle=ink(col);line(c,s==='front'?'M383 120 Q500 224 617 120':'M387 116 Q500 166 613 116',9);line(c,'M76 342 L156 474',4);line(c,'M924 342 L844 474',4);line(c,'M222 950 Q500 976 778 950',4);seams(c,col,388)}},
{id:'longsleeve',n:['T-shirt manches longues','Long-sleeve tee'],kind:'soft',colors:APPAREL,thick:.07,sides:['front','back'],
 area:{front:[350,290,300,400],back:[330,240,340,480]},
 shape:(c,s)=>fillP(c,LONG(s==='front'?198:142)),
 details:(c,s,col)=>{c.strokeStyle=ink(col);line(c,s==='front'?'M383 120 Q500 224 617 120':'M387 116 Q500 166 613 116',9);line(c,'M46 792 L144 822',4);line(c,'M954 792 L856 822',4);line(c,'M224 964 Q500 990 776 964',4);seams(c,col,420)}},
{id:'tank',n:['Camisole','Tank top'],kind:'soft',colors:APPAREL,thick:.065,sides:['front','back'],
 area:{front:[355,360,290,400],back:[355,300,290,460]},
 shape:(c,s)=>fillP(c,`M430 92 L350 92 C348 250 320 330 245 392 C245 600 246 800 248 985 Q500 1012 752 985 C754 800 755 600 755 392 C680 330 652 250 650 92 L570 92 Q500 ${s==='front'?340:210} 430 92 Z`),
 details:(c,s,col)=>{c.strokeStyle=ink(col);line(c,`M418 96 Q500 ${s==='front'?356:226} 582 96`,8);line(c,'M362 96 C360 250 334 336 258 398',7);line(c,'M638 96 C640 250 666 336 742 398',7);line(c,'M248 950 Q500 976 752 950',4)}},
{id:'polo',n:['Polo','Polo shirt'],kind:'soft',colors:APPAREL,thick:.07,sides:['front','back'],
 area:{front:[560,300,150,150],back:[330,250,340,460]},
 shape:(c,s)=>fillP(c,TEE(s==='front'?172:134)),
 details:(c,s,col)=>{c.strokeStyle=ink(col);line(c,'M76 342 L156 474',7);line(c,'M924 342 L844 474',7);line(c,'M222 950 Q500 976 778 950',4);seams(c,col,388);
  if(s==='front'){c.fillStyle=ink(col,.9);c.fill(new Path2D('M388 106 L500 198 L450 266 L350 150 Z'));c.fill(new Path2D('M612 106 L500 198 L550 266 L650 150 Z'));c.strokeStyle=ink(col);line(c,'M476 216 L476 380 L524 380 L524 216',4);c.fillStyle=ink(col,1.6);[254,318].forEach(y=>{c.beginPath();c.arc(500,y,8,0,7);c.fill()})}
  else{c.fillStyle=ink(col,.9);c.fill(new Path2D('M382 100 Q500 62 618 100 L626 152 Q500 110 374 152 Z'))}}},
{id:'crewneck',n:['Coton ouaté col rond','Crewneck sweatshirt'],kind:'soft',colors:APPAREL,thick:.095,sides:['front','back'],
 area:{front:[345,300,310,400],back:[330,250,340,470]},
 shape:(c,s)=>fillP(c,LONG(s==='front'?192:142)),
 details:(c,s,col)=>{c.strokeStyle=ink(col);line(c,s==='front'?'M378 116 Q500 228 622 116':'M382 114 Q500 172 618 114',16);cuffs(c,col);seams(c,col,420)}},
{id:'hoodie',n:['Chandail à capuchon','Hoodie'],kind:'soft',colors:APPAREL,thick:.1,sides:['front','back'],
 area:{front:[355,335,290,310],back:[335,330,330,450]},
 shape:(c,s)=>{fillP(c,LONG(150,150));fillP(c,'M384 160 C330 50 440 14 500 14 C560 14 670 50 616 160 Q500 200 384 160 Z')},
 details:(c,s,col)=>{cuffs(c,col);seams(c,col,420);
  if(s==='front'){c.fillStyle=lum(col)>.5?'rgba(0,0,0,.34)':'rgba(0,0,0,.5)';c.fill(new Path2D('M412 150 C420 66 580 66 588 150 Q500 232 412 150 Z'));c.strokeStyle=ink(col);line(c,'M398 158 Q500 250 602 158',9);line(c,'M462 204 L456 330',5);line(c,'M538 204 L544 330',5);line(c,'M338 900 L316 740 Q500 708 684 740 L662 900 Z',5)}
  else{c.strokeStyle=ink(col);line(c,'M500 18 L500 190',4);line(c,'M390 170 Q500 214 610 170',6)}}},
{id:'jacket',n:['Manteau haute visibilité','Hi-vis work jacket'],kind:'soft',colors:WORK,thick:.11,sides:['front','back'],
 area:{front:[560,290,150,150],back:[350,700,300,220]},
 shape:(c,s)=>{fillP(c,LONG(120,96));fillP(c,'M382 110 L402 56 Q500 36 598 56 L618 110 Z')},
 details:(c,s,col)=>{const y='#d7f000',g='#c3c6ca',o=lum(col)>.6?'#1c2a4a':y;cuffs(c,col);band(c,'M224 640 L776 640',64,o,g);band(c,'M82 588 L190 622',58,o,g);band(c,'M918 588 L810 622',58,o,g);
  if(s==='front'){band(c,'M340 150 L340 608',52,o,g);band(c,'M660 150 L660 608',52,o,g);c.strokeStyle=ink(col,1.4);line(c,'M500 70 L500 1016',6);line(c,'M394 98 L500 152 L606 98',6)}
  else{band(c,'M300 150 L700 608',56,o,g);band(c,'M700 150 L300 608',56,o,g)}}},
{id:'vest',n:['Dossard haute visibilité','Hi-vis safety vest'],kind:'soft',colors:HIVIS,thick:.055,sides:['front','back'],
 area:{front:[560,420,140,140],back:[395,380,210,250]},
 shape:(c,s)=>fillP(c,`M420 100 L320 100 C325 250 300 330 235 400 L235 960 Q500 985 765 960 L765 400 C700 330 675 250 680 100 L580 100 ${s==='front'?'L500 330':'Q500 170 420 100'} Z`),
 details:(c,s,col)=>{const g='#c3c6ca',o=lum(col)>.7?'#ff6a13':'#d9ef1f';band(c,'M330 104 L330 980',60,o,g);band(c,'M670 104 L670 980',60,o,g);band(c,'M235 720 L765 720',60,o,g);if(s==='front'){c.strokeStyle=ink(col,1.4);line(c,'M500 330 L500 974',6)}}},
{id:'apron',n:['Tablier','Apron'],kind:'soft',colors:APPAREL,thick:.045,sides:['front'],
 area:{front:[385,250,230,230]},
 shape:(c)=>{fillP(c,'M400 150 L600 150 C610 330 660 450 790 520 L770 1150 Q500 1170 230 1150 L210 520 C340 450 390 330 400 150 Z');c.lineWidth=30;c.lineCap='round';c.stroke(new Path2D('M414 160 C400 20 600 20 586 160'));c.stroke(new Path2D('M222 520 C150 540 110 580 70 660'));c.stroke(new Path2D('M778 520 C850 540 890 580 930 660'))},
 details:(c,s,col)=>{c.strokeStyle=ink(col);line(c,'M360 720 L640 720 L630 900 L370 900 Z',5);line(c,'M500 720 L500 900',4);line(c,'M404 176 L596 176',4)}},
{id:'short',n:['Short','Shorts'],kind:'soft',colors:APPAREL,thick:.08,sides:['front','back'],
 area:{front:[285,620,170,180],back:[545,620,170,180]},
 shape:(c)=>fillP(c,'M262 300 L738 300 C760 520 790 740 812 960 L532 980 L500 660 L468 980 L188 960 C210 740 240 520 262 300 Z'),
 details:(c,s,col)=>{c.strokeStyle=ink(col);line(c,'M258 364 L742 364',6);line(c,'M192 922 L470 942',4);line(c,'M808 922 L530 942',4);if(s==='front'){line(c,'M478 330 C470 420 480 440 462 470',5);line(c,'M522 330 C530 420 520 440 538 470',5)}c.strokeStyle=ink(col,.6);line(c,'M500 364 L500 660',4)}},
{id:'tote',n:['Sac fourre-tout','Tote bag'],kind:'soft',colors:BAGS,thick:.04,sides:['front','back'],
 area:{front:[315,580,370,400],back:[315,580,370,400]},
 shape:(c)=>{fillP(c,'M240 470 L760 470 L778 1090 Q500 1106 222 1090 Z');c.lineWidth=46;c.lineCap='butt';c.stroke(new Path2D('M362 490 C350 170 650 170 638 490'))},
 details:(c,s,col)=>{c.strokeStyle=ink(col);line(c,'M240 514 L760 514',4);line(c,'M338 480 L338 562 L386 562 L386 480',4);line(c,'M614 480 L614 562 L662 562 L662 480',4)}},
{id:'drawstring',n:['Sac à cordon','Drawstring bag'],kind:'soft',colors:BAGS,thick:.085,sides:['front','back'],
 area:{front:[330,470,340,440],back:[330,470,340,440]},
 shape:(c)=>{fillP(c,'M270 300 Q500 275 730 300 C790 520 800 880 780 1060 Q500 1098 220 1060 C200 880 210 520 270 300 Z');c.lineWidth=16;c.lineCap='round';c.stroke(new Path2D('M292 312 C140 540 160 920 232 1064'));c.stroke(new Path2D('M708 312 C860 540 840 920 768 1064'))},
 details:(c,s,col)=>{c.strokeStyle=ink(col);line(c,'M266 350 Q500 326 734 350',5);for(let x=300;x<=700;x+=36)line(c,`M${x} 300 L${x+4} 348`,3)}},
{id:'cap',n:['Casquette','Trucker cap'],kind:'cap',colors:[['Bleu royal','Royal blue','#1f49c7'],['Noir','Black','#17181b'],['Marine','Navy','#1c2a4a'],['Rouge','Red','#b3202a'],['Vert forêt','Forest green','#1f4d36']],sides:['front']},
{id:'tuque',n:['Tuque','Beanie'],kind:'tuque',colors:APPAREL,sides:['front']},
{id:'mug',n:['Tasse','Mug'],kind:'mug',colors:HARD.slice(0,5),sides:['front']},
{id:'bottle',n:['Bouteille','Water bottle'],kind:'bottle',colors:HARD,sides:['front']},
{id:'tumbler',n:['Gobelet isotherme','Insulated tumbler'],kind:'tumbler',colors:HARD,sides:['front']},
{id:'koozie',n:['Porte-canette','Can cooler'],kind:'koozie',colors:[['Noir','Black','#17181b'],['Bleu royal','Royal blue','#1f49c7'],['Rouge','Red','#b3202a'],['Blanc','White','#f1f0ec'],['Vert forêt','Forest green','#1f4d36']],sides:['front']},
{id:'sign',n:['Enseigne','Sign'],kind:'sign',colors:[['Blanc','White','#f4f4f1'],['Noir','Black','#17181b'],['Marine','Navy','#1c2a4a'],['Aluminium','Aluminium','#c4c7cb']],sides:['front']},
{id:'sticker',n:['Autocollant','Sticker'],kind:'sticker',colors:[['Blanc','White','#fbfbf8'],['Noir','Black','#17181b'],['Transparent','Clear','#e8eef0']],sides:['front']},
];
