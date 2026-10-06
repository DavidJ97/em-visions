// Modélisateur 3D EM Visions : choisir un produit, poser son image, le faire pivoter,
// puis joindre la maquette à la demande de devis. Aucune donnée n'est envoyée depuis cette page.
import * as THREE from '../vendor/three.module.min.js';
import {RoomEnvironment} from '../vendor/RoomEnvironment.js';
import {PRODUCTS} from './produits.js';

const EN=document.documentElement.lang==='en',t=(fr,en)=>EN?en:fr,$=s=>document.querySelector(s);
const mk=(w,h)=>{const c=document.createElement('canvas');c.width=w;c.height=h;return c};
const SIDE={front:t('Devant','Front'),back:t('Dos','Back')};

// ---------- état ----------
const S={pi:0,ci:{},side:'front',art:{front:null,back:null},yaw:-.5,pitch:.1,zoom:1,auto:true,tyaw:null,guide:true};
let cur=null,dirty=true;

// ---------- scène ----------
const cv=$('#view');
const R=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true});
R.setPixelRatio(Math.min(devicePixelRatio||1,2));R.toneMapping=THREE.ACESFilmicToneMapping;R.toneMappingExposure=1.05;
const scene=new THREE.Scene(),cam=new THREE.PerspectiveCamera(28,1,.1,50);
scene.environment=new THREE.PMREMGenerator(R).fromScene(new RoomEnvironment(),.04).texture;scene.environmentIntensity=.55;
const key=new THREE.DirectionalLight(0xffffff,2.1);key.position.set(2.2,3,4);scene.add(key);
const rim=new THREE.DirectionalLight(0x9db4ff,.9);rim.position.set(-3,1.5,-3);scene.add(rim);
scene.add(new THREE.HemisphereLight(0xffffff,0x202028,.5));
const pivot=new THREE.Group();scene.add(pivot);
const shadow=(()=>{const c=mk(256,256),x=c.getContext('2d'),g=x.createRadialGradient(128,128,8,128,128,126);g.addColorStop(0,'rgba(0,0,0,.55)');g.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g;x.fillRect(0,0,256,256);
 const m=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(c),transparent:true,depthWrite:false,opacity:.6}));m.rotation.x=-Math.PI/2;scene.add(m);return m})();
const noise=(()=>{const c=mk(128,128),x=c.getContext('2d'),d=x.createImageData(128,128);for(let i=0;i<d.data.length;i+=4){const v=118+Math.random()*20|0;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255}x.putImageData(d,0,0);
 const tx=new THREE.CanvasTexture(c);tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.repeat.set(9,9);return tx})();
const tex=c=>{const x=new THREE.CanvasTexture(c);x.colorSpace=THREE.SRGBColorSpace;x.anisotropy=8;return x};
const std=(o)=>new THREE.MeshStandardMaterial(o);

// ---------- image posée ----------
function drawArt(c,[x,y,w,h],a,guide){
 if(!a){if(!guide)return;c.save();c.setLineDash([w*.03,w*.022]);c.lineWidth=Math.max(2,w*.008);c.strokeStyle='rgba(120,140,255,.95)';c.strokeRect(x,y,w,h);
  c.setLineDash([]);c.fillStyle='rgba(120,140,255,.95)';c.textAlign='center';c.textBaseline='middle';c.font=`600 ${Math.max(12,w*.085)}px Kumbh Sans,sans-serif`;c.fillText(t('Votre image','Your image'),x+w/2,y+h/2);c.restore();return}
 const im=a.img,ar=im.width/im.height;let dw,dh;if(ar>w/h){dw=w;dh=w/ar}else{dh=h;dw=h*ar}dw*=a.size;dh*=a.size;
 c.save();c.translate(x+w/2+a.cx*w/2,y+h/2+a.cy*h/2);c.rotate(a.rot*Math.PI/180);c.drawImage(im,-dw/2,-dh/2,dw,dh);c.restore()}

// ---------- vêtements et sacs : silhouette gonflée ----------
const GW=177,GH=221,SS=4;
function inflate(p){const W=(GW-1)*SS+1,Hh=(GH-1)*SS+1,c=mk(W,Hh),x=c.getContext('2d');x.scale(W/1000,Hh/1250);x.fillStyle=x.strokeStyle='#000';x.lineJoin='round';x.lineWidth=12;p.shape(x,'front');
 const a=x.getImageData(0,0,W,Hh).data,d=new Float32Array(W*Hh),B=1e5;for(let i=0;i<W*Hh;i++)d[i]=a[i*4+3]>127?B:0;
 const at=(i,j)=>i<0||j<0||i>=W||j>=Hh?0:d[j*W+i],D=1.4142;
 for(let j=0;j<Hh;j++)for(let i=0;i<W;i++){const k=j*W+i;if(d[k])d[k]=Math.min(d[k],at(i-1,j)+1,at(i,j-1)+1,at(i-1,j-1)+D,at(i+1,j-1)+D)}
 for(let j=Hh-1;j>=0;j--)for(let i=W-1;i>=0;i--){const k=j*W+i;if(d[k])d[k]=Math.min(d[k],at(i+1,j)+1,at(i,j+1)+1,at(i+1,j+1)+D,at(i-1,j+1)+D)}
 const Rr=W*(p.round||.12),h=new Float32Array(GW*GH);let i0=GW,i1=0,j0=GH,j1=0;
 for(let j=0;j<GH;j++)for(let i=0;i<GW;i++){const raw=d[j*SS*W+i*SS],dd=Math.max(0,raw-SS*1.3);if(raw>0){if(i<i0)i0=i;if(i>i1)i1=i;if(j<j0)j0=j;if(j>j1)j1=j}const u=Math.min(dd/Rr,1);h[j*GW+i]=p.thick*Math.pow(1-(1-u)*(1-u),.62)}
 for(let n=0;n<2;n++){const s=h.slice();for(let j=1;j<GH-1;j++)for(let i=1;i<GW-1;i++){const k=j*GW+i;if(s[k]>p.thick*.25)h[k]=(s[k]*2+s[k-1]+s[k+1]+s[k-GW]+s[k+GW])/6}}
 h.box=new THREE.Box3(new THREE.Vector3(i0/(GW-1)-.5,(.5-j1/(GH-1))*1.25,-p.thick),new THREE.Vector3(i1/(GW-1)-.5,(.5-j0/(GH-1))*1.25,p.thick));return h}
function buildSoft(p,col){const TW=1024,TH=1280,g=new THREE.Group(),H=inflate(p),cs={};
 const sheet=side=>{const c=mk(TW,TH);cs[side]=c;const geo=new THREE.PlaneGeometry(1,1.25,GW-1,GH-1),pos=geo.attributes.position;for(let i=0;i<pos.count;i++)pos.setZ(i,H[i]);geo.computeVertexNormals();
  const m=new THREE.Mesh(geo,std({map:tex(c),alphaTest:.5,alphaToCoverage:true,roughness:.93,bumpMap:noise,bumpScale:.9}));if(side==='back')m.rotation.y=Math.PI;g.add(m);return m};
 const ms={front:sheet('front'),back:sheet('back')};
 const paint=(guide)=>{for(const side of['front','back']){const c=cs[side].getContext('2d');c.setTransform(1,0,0,1,0,0);c.clearRect(0,0,TW,TH);c.setTransform(TW/1000,0,0,TH/1250,0,0);
   c.fillStyle=c.strokeStyle=col;c.lineJoin='round';c.lineCap='butt';c.lineWidth=12;p.shape(c,side);c.globalCompositeOperation='source-atop';
   const has=p.sides.includes(side);if(has)p.details(c,side,col);c.lineCap='butt';if(has)drawArt(c,p.area[side],S.art[side],guide&&S.side===side);c.globalCompositeOperation='source-over';ms[side].material.map.needsUpdate=true}};
 return{group:g,paint,box:H.box}}

// ---------- objets : surface enroulée autour d'un cylindre ----------
function wrap(rTop,rBot,h,col,mat,areaW=.34,areaH=.78){const PX=560,ra=(rTop+rBot)/2,W=Math.round(2*Math.PI*ra*PX),Hh=Math.round(h*PX),c=mk(W,Hh);
 const m=new THREE.Mesh(new THREE.CylinderGeometry(rTop,rBot,h,96,1,true,Math.PI,Math.PI*2),std({map:tex(c),...mat}));
 const area=[W/2-W*areaW/2,Hh*(1-areaH)/2,W*areaW,Hh*areaH];
 const paint=(guide,deco)=>{const x=c.getContext('2d');x.fillStyle=col;x.fillRect(0,0,W,Hh);if(deco)deco(x,W,Hh);drawArt(x,area,S.art.front,guide);m.material.map.needsUpdate=true};return{mesh:m,paint}}
const disc=(r,y,mat,up=true)=>{const m=new THREE.Mesh(new THREE.CircleGeometry(r,64),mat);m.rotation.x=up?-Math.PI/2:Math.PI/2;m.position.y=y;return m};
const lathe=(pts,mat)=>(mat.side=THREE.DoubleSide,new THREE.Mesh(new THREE.LatheGeometry(pts.map(p=>new THREE.Vector2(p[0],p[1])),72),mat));
const metalOf=col=>col==='#b9bdc2'?{metalness:1,roughness:.3}:{metalness:.35,roughness:.42};

const BUILD={
 soft:buildSoft,
 mug(p,col){const g=new THREE.Group(),w=wrap(.42,.42,.95,col,{roughness:.2},.36,.74),in_=std({color:'#f6f5f1',roughness:.25,side:THREE.BackSide}),sol=std({color:col,roughness:.2});
  g.add(w.mesh,new THREE.Mesh(new THREE.CylinderGeometry(.385,.385,.9,64,1,true),in_),disc(.385,-.42,std({color:'#f6f5f1',roughness:.25})),disc(.42,-.475,sol,false));
  const rimm=new THREE.Mesh(new THREE.RingGeometry(.385,.42,64),sol);rimm.rotation.x=-Math.PI/2;rimm.position.y=.475;g.add(rimm);
  const hd=new THREE.Mesh(new THREE.TorusGeometry(.24,.05,16,40,Math.PI),sol);hd.rotation.z=-Math.PI/2;hd.scale.set(1,1.15,1);hd.position.set(.42,0,0);g.add(hd);return{group:g,paint:w.paint}},
 bottle(p,col){const g=new THREE.Group(),mt=metalOf(col),w=wrap(.3,.3,1.15,col,mt,.36,.8),sol=std({color:col,...mt}),dark=std({color:'#1b1c1f',roughness:.45});
  g.add(w.mesh);const sh=lathe([[.3,0],[.3,.02],[.275,.11],[.18,.23],[.145,.27],[.145,.36]],sol);sh.position.y=.575;g.add(sh);
  const bt=lathe([[0,0],[.27,0],[.3,.035]],sol);bt.position.y=-.61;g.add(bt);
  const cp=new THREE.Mesh(new THREE.CylinderGeometry(.158,.158,.15,48),dark);cp.position.y=1.0;g.add(cp);
  const lp=new THREE.Mesh(new THREE.TorusGeometry(.085,.022,12,32),dark);lp.position.y=1.12;g.add(lp);return{group:g,paint:w.paint}},
 tumbler(p,col){const g=new THREE.Group(),mt=metalOf(col),w=wrap(.37,.29,1.2,col,mt,.34,.74),sol=std({color:col,...mt});
  g.add(w.mesh,disc(.29,-.6,sol,false));const lid=new THREE.Mesh(new THREE.CylinderGeometry(.378,.372,.07,64),std({color:'#23252a',roughness:.35}));lid.position.y=.635;g.add(lid);
  const sl=new THREE.Mesh(new THREE.BoxGeometry(.16,.02,.09),std({color:'#3a3d44',roughness:.4}));sl.position.set(0,.675,.17);g.add(sl);return{group:g,paint:w.paint}},
 koozie(p,col){const g=new THREE.Group(),w=wrap(.36,.36,.82,col,{roughness:1,bumpMap:noise,bumpScale:1.2},.36,.76),alu=std({color:'#d5d8dc',metalness:1,roughness:.28});
  g.add(w.mesh,disc(.36,-.41,std({color:col,roughness:1}),false));const can=lathe([[.33,0],[.33,.3],[.29,.36],[.28,.385],[.27,.385],[.26,.37],[0,.37]],alu);can.position.y=.36;g.add(can);
  const rg=new THREE.Mesh(new THREE.RingGeometry(.33,.36,64),std({color:col,roughness:1}));rg.rotation.x=-Math.PI/2;rg.position.y=.41;g.add(rg);return{group:g,paint:w.paint}},
 tuque(p,col){const g=new THREE.Group(),rib=(x,W,H)=>{for(let i=0;i<W;i+=14){x.fillStyle='rgba(0,0,0,.16)';x.fillRect(i,0,5,H);x.fillStyle='rgba(255,255,255,.07)';x.fillRect(i+7,0,3,H)}};
  const w=wrap(.53,.525,.36,col,{roughness:1},.3,.74);w.mesh.position.y=.18;g.add(w.mesh);
  const rc=mk(512,64),rx=rc.getContext('2d');const dm=std({map:tex(rc),roughness:1});const dome=lathe([[.5,0],[.505,.2],[.5,.42],[.47,.6],[.4,.77],[.28,.9],[.13,.97],[0,.99]],dm);dome.position.y=.02;g.add(dome);
  const ed=new THREE.Mesh(new THREE.TorusGeometry(.527,.012,8,64),std({color:col,roughness:1}));ed.rotation.x=Math.PI/2;ed.position.y=.36;g.add(ed);
  const pm=new THREE.Mesh(new THREE.SphereGeometry(.13,24,16),std({color:col,roughness:1,bumpMap:noise,bumpScale:3}));pm.position.y=1.08;g.add(pm);
  const paint=guide=>{rx.fillStyle=col;rx.fillRect(0,0,512,64);for(let i=0;i<512;i+=8){rx.fillStyle='rgba(0,0,0,.14)';rx.fillRect(i,0,3,64)}dm.map.needsUpdate=true;pm.material.color.set(col);ed.material.color.set(col);w.paint(guide,rib)};return{group:g,paint}},
 cap(p,col){const g=new THREE.Group(),c=mk(1024,512),r=.5,sy=1.16,sz_=1.12;
  const front=new THREE.Mesh(new THREE.SphereGeometry(r,48,24,0,Math.PI,0,Math.PI/2),std({map:tex(c),roughness:.9}));
  const mc=mk(256,256),mx=mc.getContext('2d'),mt=tex(mc);mt.wrapS=mt.wrapT=THREE.RepeatWrapping;mt.repeat.set(9,5);
  const back=new THREE.Mesh(new THREE.SphereGeometry(r,48,24,Math.PI,Math.PI,0,Math.PI/2),std({map:mt,roughness:.85}));front.scale.set(1,sy,sz_);back.scale.set(1,sy,sz_);g.add(front,back);
  const sh=new THREE.Shape();sh.moveTo(-.47,0);sh.bezierCurveTo(-.5,.5,-.22,.62,0,.62);sh.bezierCurveTo(.22,.62,.5,.5,.47,0);sh.quadraticCurveTo(0,.2,-.47,0);
  const sol=std({color:col,roughness:.8}),vis=new THREE.Mesh(new THREE.ExtrudeGeometry(sh,{depth:.022,bevelEnabled:false,curveSegments:32}),sol);vis.rotation.x=Math.PI/2+.1;vis.position.set(0,.035,.44);g.add(vis);
  const bt=new THREE.Mesh(new THREE.SphereGeometry(.035,16,10),sol);bt.position.y=r*sy;g.add(bt);
  const bd=new THREE.Mesh(new THREE.TorusGeometry(r,.012,8,64),sol);bd.rotation.x=Math.PI/2;bd.position.y=.012;g.add(bd);
  const area=[337,215,350,215];
  const paint=guide=>{const x=c.getContext('2d');x.fillStyle='#f4f2eb';x.fillRect(0,0,1024,512);drawArt(x,area,S.art.front,guide);front.material.map.needsUpdate=true;
   mx.fillStyle=col;mx.fillRect(0,0,256,256);mx.fillStyle='rgba(0,0,0,.42)';for(let j=0;j<8;j++)for(let i=0;i<8;i++){mx.beginPath();mx.arc(i*32+(j%2?16:0)+8,j*32+16,9,0,7);mx.fill()}mt.needsUpdate=true;sol.color.set(col)};return{group:g,paint}},
 sign(p,col){const g=new THREE.Group(),c=mk(1200,800),side=std({color:col,roughness:.5,metalness:col==='#c4c7cb'?1:.1}),fr=std({map:tex(c),roughness:.42,metalness:col==='#c4c7cb'?.8:.05});
  g.add(new THREE.Mesh(new THREE.BoxGeometry(1.5,1,.03),[side,side,side,side,fr,side]));const st=std({color:'#c9ccd1',metalness:1,roughness:.25});
  for(const[x,y]of[[-.66,.41],[.66,.41],[-.66,-.41],[.66,-.41]]){const s=new THREE.Mesh(new THREE.CylinderGeometry(.03,.03,.03,24),st);s.rotation.x=Math.PI/2;s.position.set(x,y,.025);g.add(s)}
  const paint=guide=>{const x=c.getContext('2d');x.fillStyle=col;x.fillRect(0,0,1200,800);drawArt(x,[150,110,900,580],S.art.front,guide);fr.map.needsUpdate=true};return{group:g,paint}},
 sticker(p,col){const g=new THREE.Group(),c=mk(1024,1024),clear=col==='#e8eef0',fr=std({map:tex(c),roughness:.3,transparent:true});
  const bk=new THREE.Mesh(new THREE.PlaneGeometry(1.5,1.5),std({color:'#cfcabd',roughness:.9,side:THREE.DoubleSide}));bk.position.z=-.006;g.add(bk);
  const f=new THREE.Mesh(new THREE.CircleGeometry(.62,96),fr);g.add(f);
  const paint=guide=>{const x=c.getContext('2d');x.clearRect(0,0,1024,1024);x.globalAlpha=clear?.45:1;x.fillStyle=col;x.fillRect(0,0,1024,1024);x.globalAlpha=1;drawArt(x,[162,162,700,700],S.art.front,guide);
   x.strokeStyle='rgba(0,0,0,.12)';x.lineWidth=10;x.beginPath();x.arc(512,512,507,0,7);x.stroke();fr.map.needsUpdate=true};return{group:g,paint}},
};

// ---------- affichage ----------
function dispose(o){o.traverse(m=>{if(m.geometry)m.geometry.dispose();const ms=m.material?[].concat(m.material):[];ms.forEach(x=>{if(x.map&&x.map!==noise)x.map.dispose();x.dispose()})})}
function colorOf(p){return p.colors[S.ci[p.id]||0]}
function load(){const p=PRODUCTS[S.pi];if(cur){pivot.remove(cur.group);dispose(cur.group)}
 if(!p.sides.includes(S.side))S.side='front';
 cur=(BUILD[p.kind]||BUILD.soft)(p,colorOf(p)[2]);cur.p=p;
 const b=cur.box||new THREE.Box3().setFromObject(cur.group),ctr=b.getCenter(new THREE.Vector3()),sz=b.getSize(new THREE.Vector3());cur.group.position.sub(ctr);cur.size=sz;pivot.add(cur.group);
 shadow.position.y=-sz.y/2-.06;const sw=Math.max(sz.x,sz.z)*1.25;shadow.scale.set(sw,Math.max(sw*.5,sz.z*2),1);cur.paint(S.guide);fit();dirty=true}
function fit(){if(!cur)return;const a=cam.aspect,f=Math.tan(cam.fov*Math.PI/360),sz=cur.size,rw=Math.hypot(sz.x,sz.z)/2,d=Math.max((sz.y/2+.1)/f,(rw+.06)/(f*a))*1.1/S.zoom;cam.position.set(0,0,d);cam.lookAt(0,0,0);cam.updateProjectionMatrix()}
function resize(){const r=cv.parentElement.getBoundingClientRect();if(!r.width)return;R.setSize(r.width,r.height,false);cam.aspect=r.width/r.height;fit();dirty=true}
new ResizeObserver(resize).observe(cv.parentElement);
function frame(now){requestAnimationFrame(frame);
 if(S.auto){S.yaw=-.15+.5*Math.sin(now*.0007);dirty=true}
 if(S.tyaw!==null){const d=S.tyaw-S.yaw;if(Math.abs(d)<.01){S.yaw=S.tyaw;S.tyaw=null}else S.yaw+=d*.14;dirty=true}
 if(!dirty)return;dirty=false;pivot.rotation.set(S.pitch,S.yaw,0);R.render(scene,cam)}

// ---------- pivoter ----------
const pts=new Map();let pinch=0;
cv.addEventListener('pointerdown',e=>{pts.set(e.pointerId,[e.clientX,e.clientY]);cv.setPointerCapture(e.pointerId);S.auto=false;S.tyaw=null;cv.classList.add('grab')});
cv.addEventListener('pointermove',e=>{const p=pts.get(e.pointerId);if(!p)return;
 if(pts.size===2){pts.set(e.pointerId,[e.clientX,e.clientY]);const[a,b]=[...pts.values()],d=Math.hypot(a[0]-b[0],a[1]-b[1]);if(pinch)zoom(d/pinch);pinch=d;return}
 S.yaw+=(e.clientX-p[0])*.011;if(e.pointerType==='mouse')S.pitch=Math.max(-.7,Math.min(.7,S.pitch+(e.clientY-p[1])*.008));pts.set(e.pointerId,[e.clientX,e.clientY]);dirty=true});
const up=e=>{pts.delete(e.pointerId);pinch=0;cv.classList.remove('grab')};cv.addEventListener('pointerup',up);cv.addEventListener('pointercancel',up);
function zoom(k){S.zoom=Math.max(.7,Math.min(2,S.zoom*k));fit();dirty=true}
cv.addEventListener('wheel',e=>{if(!e.ctrlKey&&Math.abs(e.deltaY)<40)return;e.preventDefault();S.auto=false;zoom(e.deltaY<0?1.08:.93)},{passive:false});
cv.addEventListener('keydown',e=>{const k={ArrowLeft:-.2,ArrowRight:.2}[e.key];if(k){S.auto=false;S.yaw+=k;dirty=true;e.preventDefault()}});

// ---------- interface ----------
const toastEl=$('#toast');let tt;const toast=m=>{toastEl.textContent=m;toastEl.classList.add('on');clearTimeout(tt);tt=setTimeout(()=>toastEl.classList.remove('on'),2800)};
const repaint=()=>{cur.paint(S.guide);dirty=true};
function uiProducts(){const box=$('#prods');box.innerHTML='';PRODUCTS.forEach((p,i)=>{const b=document.createElement('button');b.type='button';b.className='prod';b.setAttribute('aria-pressed',i===S.pi);b.dataset.i=i;
  b.innerHTML=`<img alt="" width="96" height="96" loading="lazy" src="${new URL('../img/m3d/'+p.id+'.webp',import.meta.url).href}"><span>${p.n[EN?1:0]}</span>`;b.onclick=()=>{S.pi=i;S.auto=false;S.tyaw=-.45;S.pitch=.1;S.zoom=1;load();uiAll()};box.appendChild(b)})}
function uiColors(){const p=PRODUCTS[S.pi],box=$('#cols');box.innerHTML='';p.colors.forEach((c,i)=>{const b=document.createElement('button');b.type='button';b.className='sw';b.style.background=c[2];b.title=c[EN?1:0];b.setAttribute('aria-label',c[EN?1:0]);
  b.setAttribute('aria-pressed',i===(S.ci[p.id]||0));b.onclick=()=>{S.ci[p.id]=i;load();uiAll()};box.appendChild(b)});$('#colname').textContent=colorOf(p)[EN?1:0]}
function uiSides(){const p=PRODUCTS[S.pi],box=$('#tabs');box.innerHTML='';box.hidden=p.sides.length<2;p.sides.forEach(s=>{const b=document.createElement('button');b.type='button';b.textContent=SIDE[s]+(S.art[s]?' ●':'');b.setAttribute('aria-pressed',s===S.side);
  b.onclick=()=>{S.side=s;S.auto=false;S.tyaw=(s==='back'?Math.PI:0)-.3;repaint();uiAll()};box.appendChild(b)})}
function uiArt(){const a=S.art[S.side];$('#adj').hidden=!a;$('#upname').textContent=a?a.name:t('Choisir une image','Choose an image');if(!a)return;
 for(const k of['size','cx','cy','rot'])$('#s-'+k).value=a[k]}
function uiAll(){document.querySelectorAll('.prod').forEach(b=>b.setAttribute('aria-pressed',+b.dataset.i===S.pi));uiColors();uiSides();uiArt();$('#pname').textContent=PRODUCTS[S.pi].n[EN?1:0]}
$('#file').addEventListener('change',e=>{const f=e.target.files[0];if(!f)return;if(!/^image\//.test(f.type)){toast(t('Choisissez une image (PNG, JPG ou SVG).','Please choose an image (PNG, JPG or SVG).'));return}
 if(f.size>12e6){toast(t('Image trop lourde (max 12 Mo).','Image too large (max 12 MB).'));return}
 const im=new Image();im.onload=()=>{S.art[S.side]={img:im,name:f.name,file:f,size:.9,cx:0,cy:0,rot:0};S.auto=false;S.tyaw=(S.side==='back'?Math.PI:0)-.25;repaint();uiAll()};
 im.onerror=()=>toast(t('Impossible de lire cette image.','This image could not be read.'));im.src=URL.createObjectURL(f);e.target.value=''});
for(const k of['size','cx','cy','rot'])$('#s-'+k).addEventListener('input',e=>{const a=S.art[S.side];if(!a)return;a[k]=+e.target.value;repaint()});
$('#rm').onclick=()=>{S.art[S.side]=null;repaint();uiAll()};

// ---------- rendu hors écran (vignettes, captures) : même pipeline que la vue principale ----------
function snapGroup(g,sz,size,yaw,pitch,withShadow){const pr=R.getPixelRatio(),s=R.getSize(new THREE.Vector2()),a=cam.aspect,rot=pivot.rotation.clone(),vis=cur.group.visible,sv=shadow.visible,cp=cam.position.clone();
 if(g!==cur.group){cur.group.visible=false;pivot.add(g)}shadow.visible=withShadow;
 R.setPixelRatio(1);R.setSize(size,size,false);cam.aspect=1;const f=Math.tan(cam.fov*Math.PI/360);cam.position.set(0,0,Math.max(sz.y/2+.08,(Math.hypot(sz.x,sz.z)/2+.06)/1)/f*1.08);cam.updateProjectionMatrix();
 pivot.rotation.set(pitch,yaw,0);R.render(scene,cam);const c=mk(size,size);c.getContext('2d').drawImage(cv,0,0);
 if(g!==cur.group){pivot.remove(g);cur.group.visible=vis}shadow.visible=sv;R.setPixelRatio(pr);R.setSize(s.x,s.y,false);cam.aspect=a;cam.position.copy(cp);cam.updateProjectionMatrix();pivot.rotation.copy(rot);R.render(scene,cam);return c}
// Vignettes : fichiers fixes dans img/m3d/, produits une fois avec thumb() ci-dessous (outil de fabrication).
function thumb(i){const p=PRODUCTS[i],keep=[S.art,S.side];S.art={front:null,back:null};S.side='front';
 const tc=p.colors.find(c=>{const n=parseInt(c[2].slice(1),16),l=(.299*(n>>16)+.587*(n>>8&255)+.114*(n&255))/255;return l>.2&&l<.86})||p.colors[0],g=(BUILD[p.kind]||BUILD.soft)(p,tc[2]);g.paint(false);[S.art,S.side]=keep;
 const b=g.box||new THREE.Box3().setFromObject(g.group),sz=b.getSize(new THREE.Vector3());g.group.position.sub(b.getCenter(new THREE.Vector3()));
 const u=snapGroup(g.group,sz,256,-.5,.12,false).toDataURL('image/png');dispose(g.group);return u}

// ---------- joindre à la demande de devis ----------
const shot=(yaw,size=820)=>snapGroup(cur.group,cur.size,size,yaw,.08,true);
function summary(){const p=PRODUCTS[S.pi],sides=p.sides.filter(s=>S.art[s]).map(s=>SIDE[s].toLowerCase());
 let m=`${t('Maquette 3D :','3D mockup:')} ${p.n[EN?1:0]}, ${colorOf(p)[EN?1:0].toLowerCase()}`;
 if(sides.length)m+=p.sides.length>1?`, ${t('impression','print')} ${sides.join(' + ')}`:`, ${t('avec mon image','with my image')}`;return m+'.'}
const idb=()=>new Promise((ok,ko)=>{const r=indexedDB.open('em-visions',1);r.onupgradeneeded=()=>r.result.createObjectStore('kv');r.onsuccess=()=>ok(r.result);r.onerror=()=>ko(r.error)});
async function send(){const p=PRODUCTS[S.pi],btn=$('#send');btn.disabled=true;
 try{S.guide=false;cur.paint(false);const hasBack=p.sides.includes('back')&&S.art.back,a=shot(-.32),b=shot(hasBack?Math.PI-.32:.75);S.guide=true;cur.paint(true);
  const c=mk(1680,940),x=c.getContext('2d');x.fillStyle='#111214';x.fillRect(0,0,1680,940);x.drawImage(a,10,20);x.drawImage(b,850,20);
  x.fillStyle='#f4f4f2';x.font='600 30px Kumbh Sans,sans-serif';x.textBaseline='middle';x.fillText('EM Visions — '+summary(),40,895);
  const snap=await new Promise(r=>c.toBlob(r,'image/jpeg',.88)),orig=[];
  let tot=0;for(const s of p.sides){const ar=S.art[s];if(ar&&ar.file&&tot+ar.file.size<8e6){tot+=ar.file.size;orig.push({name:ar.file.name,type:ar.file.type,blob:ar.file})}}
  const db=await idb();await new Promise((ok,ko)=>{const tx=db.transaction('kv','readwrite');tx.objectStore('kv').put({snap,snapName:`maquette-${p.id}.jpg`,orig,summary:summary(),at:Date.now()},'maquette');tx.oncomplete=ok;tx.onerror=()=>ko(tx.error)});
  location.href=$('#send').dataset.to}
 catch(err){console.error(err);S.guide=true;btn.disabled=false;toast(t('La maquette n’a pas pu être préparée. Réessayez.','The mockup could not be prepared. Please try again.'))}}
$('#send').onclick=send;addEventListener('pageshow',()=>{$('#send').disabled=false});

// ---------- démarrage ----------
const Q=new URLSearchParams(location.search);if(Q.get('p')){const i=PRODUCTS.findIndex(p=>p.id===Q.get('p'));if(i>=0)S.pi=i}
uiProducts();load();uiAll();resize();requestAnimationFrame(frame);
(document.fonts&&document.fonts.ready||Promise.resolve()).then(()=>repaint());
window.__m3d={S,PRODUCTS,load,uiAll,shot,summary,thumb};
