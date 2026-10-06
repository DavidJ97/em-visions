// Modélisateur 3D EM Visions : choisir un produit, poser son image, le faire pivoter,
// puis joindre la maquette à la demande de devis. Aucune donnée n'est envoyée depuis cette page.
// Les produits sont de vrais modèles 3D (dossier models/) ; l'image est projetée sur leur surface,
// elle suit donc les plis et la lumière comme une vraie impression.
import * as THREE from '../vendor/three.module.min.js';
import {RoomEnvironment} from '../vendor/RoomEnvironment.js';
import {GLTFLoader} from '../vendor/GLTFLoader.js';
import {MeshoptDecoder} from '../vendor/meshopt_decoder.module.js';
import {PRODUCTS} from './produits.js';

const EN=document.documentElement.lang==='en',t=(fr,en)=>EN?en:fr,$=s=>document.querySelector(s);
const mk=(w,h)=>{const c=document.createElement('canvas');c.width=w;c.height=h;return c};
const SIDES=['front','back'],SIDE={front:t('Devant','Front'),back:t('Dos','Back')};
const sidesOf=p=>SIDES.filter(s=>p.print[s]);

// ---------- état ----------
const S={pi:0,ci:{},side:'front',art:{front:null,back:null},yaw:-.5,pitch:.1,zoom:1,auto:true,tyaw:null,guide:true};
let cur=null,dirty=true,seq=0;

// ---------- scène ----------
const cv=$('#view');
const R=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true,preserveDrawingBuffer:false});
R.setPixelRatio(Math.min(devicePixelRatio||1,2));R.toneMapping=THREE.NeutralToneMapping;R.toneMappingExposure=1;
R.shadowMap.enabled=true;R.shadowMap.type=THREE.PCFSoftShadowMap;
const scene=new THREE.Scene(),cam=new THREE.PerspectiveCamera(26,1,.1,50);
scene.environment=new THREE.PMREMGenerator(R).fromScene(new RoomEnvironment(),.04).texture;scene.environmentIntensity=.5;
const key=new THREE.DirectionalLight(0xfff6ea,1.7);key.position.set(1.8,3.2,3.6);key.castShadow=true;key.shadow.mapSize.set(1024,1024);key.shadow.bias=-.0004;key.shadow.normalBias=.012;key.shadow.radius=5;
Object.assign(key.shadow.camera,{left:-1.3,right:1.3,top:1.3,bottom:-1.3,near:.5,far:12});scene.add(key);
const rim=new THREE.DirectionalLight(0xbfd0ff,1);rim.position.set(-3,1.6,-3);scene.add(rim);
const fill=new THREE.DirectionalLight(0xffffff,.3);fill.position.set(-2.5,.6,2.5);scene.add(fill);
const pivot=new THREE.Group();scene.add(pivot);
const shadow=(()=>{const c=mk(256,256),x=c.getContext('2d'),g=x.createRadialGradient(128,128,8,128,128,126);g.addColorStop(0,'rgba(0,0,0,.55)');g.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=g;x.fillRect(0,0,256,256);
 const m=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(c),transparent:true,depthWrite:false,opacity:.6}));m.rotation.x=-Math.PI/2;scene.add(m);return m})();

// ---------- image projetée sur le produit ----------
// Deux emplacements (devant, dos). Chacun a son repère (uPM : produit -> repère d'impression), sa texture et sa
// matrice 2D (uUV : position, taille, rotation). uCfg = actif, rayon (0 = à plat, sinon enroulé), profondeur mini, seuil d'orientation.
const VERT_DECL='uniform mat4 uPM[2];varying vec3 vPP0;varying vec3 vPP1;varying vec3 vPN0;varying vec3 vPN1;';
const VERT_BODY='{mat4 m0=uPM[0]*modelMatrix;mat4 m1=uPM[1]*modelMatrix;vPP0=(m0*vec4(position,1.)).xyz;vPP1=(m1*vec4(position,1.)).xyz;vPN0=mat3(m0)*normal;vPN1=mat3(m1)*normal;}';
const FRAG_DECL=`uniform sampler2D uArt0;uniform sampler2D uArt1;uniform vec4 uCfg[2];uniform mat3 uUV[2];varying vec3 vPP0;varying vec3 vPP1;varying vec3 vPN0;varying vec3 vPN1;
vec4 emPrint(sampler2D tx,vec3 p,vec3 n,vec4 cfg,mat3 m){
 vec3 nn=normalize(n);float cyl=step(.00001,cfg.y),rad=length(p.xz);
 vec2 q=mix(p.xy,vec2(atan(p.x,p.z)*cfg.y,p.y),cyl);
 float face=mix(nn.z,dot(nn,vec3(p.x,0.,p.z)/max(rad,.0001)),cyl),depth=mix(p.z,rad,cyl);
 vec2 uv=(m*vec3(q,1.)).xy;
 float k=cfg.x*max(float(gl_FrontFacing),step(cfg.w,-1.5))*step(cfg.w,face)*step(cfg.z,depth)*step(0.,uv.x)*step(uv.x,1.)*step(0.,uv.y)*step(uv.y,1.);
 vec4 c=texture2D(tx,uv);vec3 s=c.a>.001?c.rgb/c.a:vec3(0.);
 s=mix(s/12.92,pow((s+.055)/1.055,vec3(2.4)),step(.04045,s));return vec4(s,c.a*k);}`;
const FRAG_BODY='float emK=0.;{vec4 a=emPrint(uArt0,vPP0,vPN0,uCfg[0],uUV[0]);vec4 b=emPrint(uArt1,vPP1,vPN1,uCfg[1],uUV[1]);diffuseColor.rgb=mix(diffuseColor.rgb,a.rgb,a.a);diffuseColor.rgb=mix(diffuseColor.rgb,b.rgb,b.a);emK=max(a.a,b.a);}';
function hook(mat,U){mat.onBeforeCompile=sh=>{Object.assign(sh.uniforms,U);
  sh.vertexShader=sh.vertexShader.replace('#include <common>','#include <common>\n'+VERT_DECL).replace('#include <begin_vertex>','#include <begin_vertex>\n'+VERT_BODY);
  sh.fragmentShader=sh.fragmentShader.replace('#include <common>','#include <common>\n'+FRAG_DECL).replace('#include <map_fragment>','#include <map_fragment>\n'+FRAG_BODY)
   .replace('#include <metalnessmap_fragment>','#include <metalnessmap_fragment>\nmetalnessFactor*=1.-.9*emK;')};
 mat.customProgramCacheKey=()=>'em-print';mat.needsUpdate=true}
const artTex=c=>{const x=new THREE.CanvasTexture(c);x.premultiplyAlpha=true;x.colorSpace=THREE.NoColorSpace;x.anisotropy=8;return x};
function imageTex(im){const w0=im.naturalWidth||im.width||1000,h0=im.naturalHeight||im.height||1000,k=Math.min(1,2048/Math.max(w0,h0)),c=mk(Math.max(2,Math.round(w0*k)),Math.max(2,Math.round(h0*k)));
 c.getContext('2d').drawImage(im,0,0,c.width,c.height);return{tex:artTex(c),ar:c.width/c.height}}
const guides={};
function guideTex(ar){const k=Math.round(ar*20);if(guides[k])return guides[k];const w=512,h=Math.max(64,Math.round(512/ar)),c=mk(w,h),x=c.getContext('2d'),u=Math.min(w,h);
 x.setLineDash([u*.07,u*.05]);x.lineWidth=Math.max(4,u*.02);x.strokeStyle=x.fillStyle='rgba(120,145,255,.95)';x.strokeRect(x.lineWidth,x.lineWidth,w-2*x.lineWidth,h-2*x.lineWidth);
 x.setLineDash([]);x.textAlign='center';x.textBaseline='middle';x.font=`600 ${Math.max(22,Math.min(w*.11,h*.3))}px Kumbh Sans,sans-serif`;x.fillText(t('Votre image','Your image'),w/2,h/2);return guides[k]=artTex(c)}

// ---------- chargement et préparation d'un produit ----------
const loader=new GLTFLoader();loader.setMeshoptDecoder(MeshoptDecoder);
const cache={},V=()=>new THREE.Vector3();
function build(p){return new Promise((ok,ko)=>loader.load(new URL('../models/'+p.id+'.glb',import.meta.url).href,g=>{try{ok(prepare(p,g.scene))}catch(e){ko(e)}},undefined,ko))}
function prepare(p,src){const g=new THREE.Group(),inner=new THREE.Group();if(p.upv)src.quaternion.setFromUnitVectors(new THREE.Vector3(...p.upv).normalize(),new THREE.Vector3(0,1,0));if(p.rot)src.quaternion.premultiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(p.rot[0],p.rot[1],p.rot[2])));inner.add(src);g.add(inner);g.updateMatrixWorld(true);
 const b=new THREE.Box3().setFromObject(src),sz=b.getSize(V()),k=1.3/Math.max(sz.x,sz.y,sz.z);inner.scale.setScalar(k);inner.position.copy(b.getCenter(V())).multiplyScalar(-k);g.updateMatrixWorld(true);
 const size=sz.multiplyScalar(k),set=new Set();
 src.traverse(m=>{if(!m.isMesh)return;m.castShadow=m.receiveShadow=true;if(!m.geometry.attributes.normal)m.geometry.computeVertexNormals();[].concat(m.material).forEach(x=>set.add(x))});
 const mats=[...set],tinted=mats.filter(m=>m.userData.tint),on=p.on?mats.filter(m=>new RegExp(p.on).test(m.name)):tinted.length?tinted:mats;
 for(const m of mats){if(m.userData.tint&&p.fabric){m.roughnessMap=m.metalnessMap=null;m.roughness=.9;m.metalness=0;}if(p.mat&&m.userData.tint)Object.assign(m,p.mat);if(m.normalMap&&p.bump)m.normalScale.setScalar(p.bump)}
 const U={uPM:{value:[new THREE.Matrix4(),new THREE.Matrix4()]},uUV:{value:[new THREE.Matrix3(),new THREE.Matrix3()]},uCfg:{value:[new THREE.Vector4(),new THREE.Vector4()]},uArt0:{value:null},uArt1:{value:null}};
 on.forEach(m=>hook(m,U));
 // repères d'impression : à plat (devant, dos, ou direction donnée) ou enroulé autour d'un axe vertical
 const frames={},ray=new THREE.Raycaster(),ext=a=>Math.abs(a.x)*size.x/2+Math.abs(a.y)*size.y/2+Math.abs(a.z)*size.z/2;
 for(const s of sidesOf(p)){const d=p.print[s],f={};let X,Y,N,o;
  if(d.cyl){const a=d.a||0;N=new THREE.Vector3(Math.sin(a),0,Math.cos(a));Y=new THREE.Vector3(0,1,0);X=V().crossVectors(Y,N);o=new THREE.Vector3((d.axis?d.axis[0]:0)*size.x/2,d.c[1]*size.y/2,(d.axis?d.axis[1]:0)*size.z/2);
   ray.set(o.clone().addScaledVector(N,3),N.clone().negate());const h=ray.intersectObject(g,true)[0];f.R=h?3-h.distance:Math.min(size.x,size.z)/2;f.zmin=f.R-(d.depth||.03);f.w=d.w*f.R}
  else{N=new THREE.Vector3(...(d.n||(s==='back'?[0,0,-1]:[0,0,1]))).normalize();X=V().crossVectors(new THREE.Vector3(...(d.up||[0,1,0])),N).normalize();Y=V().crossVectors(N,X);
   o=V().addScaledVector(X,d.c[0]*ext(X)).addScaledVector(Y,d.c[1]*ext(Y));ray.set(o.clone().addScaledVector(N,3),N.clone().negate());const h=ray.intersectObject(g,true)[0];
   f.R=0;f.zmin=h?3-h.distance-(d.depth||.12):-9;f.w=d.w*2*ext(X)}
  f.h=f.w*d.ar;f.nt=d.nt===undefined?.05:d.nt;f.inv=new THREE.Matrix4().makeBasis(X,Y,N).setPosition(o).invert();frames[s]=f}
 const gi=new THREE.Matrix4();
 return{p,group:g,size,tinted,frames,U,sync(){gi.copy(g.matrixWorld).invert();SIDES.forEach((s,i)=>{if(frames[s])U.uPM.value[i].multiplyMatrices(frames[s].inv,gi)})}}}
function colorOf(p){return p.colors[S.ci[p.id]||0]}
// applique la couleur choisie et place les images (ou le repère « Votre image »)
function apply(guide=S.guide){if(!cur)return;const p=cur.p,col=colorOf(p)[2];for(const m of cur.tinted)m.color.set(col);
 SIDES.forEach((s,i)=>{const f=cur.frames[s],a=S.art[s],cfg=cur.U.uCfg.value[i];let tex=null,dw,dh,ox=0,oy=0,r=0;
  if(f&&a){tex=a.tex;if(a.ar>f.w/f.h){dw=f.w;dh=f.w/a.ar}else{dh=f.h;dw=f.h*a.ar}dw*=a.size;dh*=a.size;ox=a.cx*f.w/2;oy=-a.cy*f.h/2;r=-a.rot*Math.PI/180}
  else if(f&&guide&&S.side===s){tex=guideTex(f.w/f.h);dw=f.w;dh=f.h}
  cur.U['uArt'+i].value=tex;if(!tex){cfg.set(0,0,0,0);return}
  const c=Math.cos(r),n=Math.sin(r);cur.U.uUV.value[i].set(c/dw,n/dw,.5-(c*ox+n*oy)/dw,-n/dh,c/dh,.5-(-n*ox+c*oy)/dh,0,0,1);cfg.set(1,f.R,f.zmin,f.nt)});dirty=true}

// ---------- affichage ----------
const ld=$('#ld');
async function load(){const p=PRODUCTS[S.pi],n=++seq;let c;if(ld)ld.hidden=false;
 try{c=await(cache[p.id]||(cache[p.id]=build(p)))}catch(e){console.error(e);delete cache[p.id];if(n===seq){if(ld)ld.hidden=true;toast(t('Ce produit n’a pas pu être chargé. Réessayez.','This product could not be loaded. Please try again.'))}return}
 if(n!==seq)return;if(ld)ld.hidden=true;if(cur)pivot.remove(cur.group);cur=c;pivot.add(c.group);if(!c.frames[S.side])S.side='front';
 const sz=c.size;shadow.position.y=-sz.y/2-.02;const sw=Math.max(sz.x,sz.z)*1.25;shadow.scale.set(sw,Math.max(sw*.5,sz.z*1.6),1);apply();fit();uiAll();dirty=true}
function fit(){if(!cur)return;const a=cam.aspect,f=Math.tan(cam.fov*Math.PI/360),sz=cur.size,rw=Math.hypot(sz.x,sz.z)/2,d=Math.max((sz.y/2+.1)/f,(rw+.06)/(f*a))*1.1/S.zoom;cam.position.set(0,0,d);cam.lookAt(0,0,0);cam.updateProjectionMatrix()}
function resize(){const r=cv.parentElement.getBoundingClientRect();if(!r.width)return;R.setSize(r.width,r.height,false);cam.aspect=r.width/r.height;fit();dirty=true}
new ResizeObserver(resize).observe(cv.parentElement);
function draw(){pivot.updateMatrixWorld(true);if(cur)cur.sync();R.render(scene,cam)}
function frame(now){requestAnimationFrame(frame);
 if(S.auto){S.yaw=-.15+.5*Math.sin(now*.0007);dirty=true}
 if(S.tyaw!==null){const d=S.tyaw-S.yaw;if(Math.abs(d)<.01){S.yaw=S.tyaw;S.tyaw=null}else S.yaw+=d*.14;dirty=true}
 if(!dirty||!cur)return;dirty=false;pivot.rotation.set(S.pitch,S.yaw,0);draw()}

// ---------- pivoter ----------
const pts=new Map();let pinch=0;
cv.addEventListener('pointerdown',e=>{pts.set(e.pointerId,[e.clientX,e.clientY]);cv.setPointerCapture(e.pointerId);S.auto=false;S.tyaw=null;cv.classList.add('grab')});
cv.addEventListener('pointermove',e=>{const p=pts.get(e.pointerId);if(!p)return;
 if(pts.size===2){pts.set(e.pointerId,[e.clientX,e.clientY]);const[a,b]=[...pts.values()],d=Math.hypot(a[0]-b[0],a[1]-b[1]);if(pinch)zoom(d/pinch);pinch=d;return}
 S.yaw+=(e.clientX-p[0])*.011;if(e.pointerType==='mouse')S.pitch=Math.max(-.7,Math.min(.9,S.pitch+(e.clientY-p[1])*.008));pts.set(e.pointerId,[e.clientX,e.clientY]);dirty=true});
const up=e=>{pts.delete(e.pointerId);pinch=0;cv.classList.remove('grab')};cv.addEventListener('pointerup',up);cv.addEventListener('pointercancel',up);
function zoom(k){S.zoom=Math.max(.7,Math.min(2.4,S.zoom*k));fit();dirty=true}
cv.addEventListener('wheel',e=>{if(!e.ctrlKey&&Math.abs(e.deltaY)<40)return;e.preventDefault();S.auto=false;zoom(e.deltaY<0?1.08:.93)},{passive:false});
cv.addEventListener('keydown',e=>{const k={ArrowLeft:-.2,ArrowRight:.2}[e.key];if(k){S.auto=false;S.yaw+=k;dirty=true;e.preventDefault()}});

// ---------- interface ----------
const toastEl=$('#toast');let tt;const toast=m=>{toastEl.textContent=m;toastEl.classList.add('on');clearTimeout(tt);tt=setTimeout(()=>toastEl.classList.remove('on'),2800)};
const view=p=>p.view||{};
const face=s=>(s==='back'?Math.PI:0)+(view(PRODUCTS[S.pi]).yaw||0);
function pick(i){S.pi=i;S.auto=false;const v=view(PRODUCTS[i]);S.tyaw=(v.yaw||0)-.45;S.pitch=v.pitch===undefined?.1:v.pitch;S.zoom=1;uiAll();load()}
function uiProducts(){const box=$('#prods');box.innerHTML='';PRODUCTS.forEach((p,i)=>{const b=document.createElement('button');b.type='button';b.className='prod';b.setAttribute('aria-pressed',i===S.pi);b.dataset.i=i;
  b.innerHTML=`<img alt="" width="96" height="96" loading="lazy" src="${new URL('../img/m3d/'+p.id+'.webp',import.meta.url).href}"><span>${p.n[EN?1:0]}</span>`;b.onclick=()=>pick(i);box.appendChild(b)})}
function uiColors(){const p=PRODUCTS[S.pi],box=$('#cols');box.innerHTML='';p.colors.forEach((c,i)=>{const b=document.createElement('button');b.type='button';b.className='sw';b.style.background=c[2];b.title=c[EN?1:0];b.setAttribute('aria-label',c[EN?1:0]);
  b.setAttribute('aria-pressed',i===(S.ci[p.id]||0));b.onclick=()=>{S.ci[p.id]=i;apply();uiAll()};box.appendChild(b)});$('#colname').textContent=colorOf(p)[EN?1:0]}
function uiSides(){const p=PRODUCTS[S.pi],sd=sidesOf(p),box=$('#tabs');box.innerHTML='';box.hidden=sd.length<2;sd.forEach(s=>{const b=document.createElement('button');b.type='button';b.textContent=SIDE[s]+(S.art[s]?' ●':'');b.setAttribute('aria-pressed',s===S.side);
  b.onclick=()=>{S.side=s;S.auto=false;S.tyaw=face(s)-.3;apply();uiAll()};box.appendChild(b)})}
function uiArt(){const a=S.art[S.side];$('#adj').hidden=!a;$('#upname').textContent=a?a.name:t('Choisir une image','Choose an image');if(!a)return;
 for(const k of['size','cx','cy','rot'])$('#s-'+k).value=a[k]}
function uiAll(){document.querySelectorAll('.prod').forEach(b=>b.setAttribute('aria-pressed',+b.dataset.i===S.pi));uiColors();uiSides();uiArt();$('#pname').textContent=PRODUCTS[S.pi].n[EN?1:0]}
$('#file').addEventListener('change',e=>{const f=e.target.files[0];if(!f)return;if(!/^image\//.test(f.type)){toast(t('Choisissez une image (PNG, JPG ou SVG).','Please choose an image (PNG, JPG or SVG).'));return}
 if(f.size>12e6){toast(t('Image trop lourde (max 12 Mo).','Image too large (max 12 MB).'));return}
 const im=new Image();im.onload=()=>{const old=S.art[S.side];if(old)old.tex.dispose();S.art[S.side]={name:f.name,file:f,size:.9,cx:0,cy:0,rot:0,...imageTex(im)};S.auto=false;S.tyaw=face(S.side)-.25;apply();uiAll()};
 im.onerror=()=>toast(t('Impossible de lire cette image.','This image could not be read.'));im.src=URL.createObjectURL(f);e.target.value=''});
for(const k of['size','cx','cy','rot'])$('#s-'+k).addEventListener('input',e=>{const a=S.art[S.side];if(!a)return;a[k]=+e.target.value;apply()});
$('#rm').onclick=()=>{const a=S.art[S.side];if(a)a.tex.dispose();S.art[S.side]=null;apply();uiAll()};

// ---------- rendu hors écran (captures, vignettes) : même pipeline que la vue principale ----------
function snap(size,yaw,pitch,withShadow,fill=1.08){const pr=R.getPixelRatio(),s=R.getSize(new THREE.Vector2()),a=cam.aspect,rot=pivot.rotation.clone(),sv=shadow.visible,cp=cam.position.clone(),sz=cur.size;
 shadow.visible=withShadow;R.setPixelRatio(1);R.setSize(size,size,false);cam.aspect=1;const f=Math.tan(cam.fov*Math.PI/360);cam.position.set(0,0,Math.max(sz.y/2+.08,Math.hypot(sz.x,sz.z)/2+.06)/f*fill);cam.updateProjectionMatrix();
 pivot.rotation.set(pitch,yaw,0);draw();const c=mk(size,size);c.getContext('2d').drawImage(cv,0,0);
 shadow.visible=sv;R.setPixelRatio(pr);R.setSize(s.x,s.y,false);cam.aspect=a;cam.position.copy(cp);cam.updateProjectionMatrix();pivot.rotation.copy(rot);draw();return c}
const shot=(yaw,size=820)=>snap(size,yaw,.08,true);

// ---------- joindre à la demande de devis ----------
function summary(){const p=PRODUCTS[S.pi],sd=sidesOf(p),sides=sd.filter(s=>S.art[s]).map(s=>SIDE[s].toLowerCase());
 let m=`${t('Maquette 3D :','3D mockup:')} ${p.n[EN?1:0]}, ${colorOf(p)[EN?1:0].toLowerCase()}`;
 if(sides.length)m+=sd.length>1?`, ${t('impression','print')} ${sides.join(' + ')}`:`, ${t('avec mon image','with my image')}`;return m+'.'}
const idb=()=>new Promise((ok,ko)=>{const r=indexedDB.open('em-visions',1);r.onupgradeneeded=()=>r.result.createObjectStore('kv');r.onsuccess=()=>ok(r.result);r.onerror=()=>ko(r.error)});
async function send(){const p=PRODUCTS[S.pi],btn=$('#send');if(!cur||cur.p!==p)return;btn.disabled=true;
 try{apply(false);const y=view(p).yaw||0,hasBack=cur.frames.back&&S.art.back,a=shot(y-.32),b=shot(y+(hasBack?Math.PI-.32:.75));apply();
  const c=mk(1680,940),x=c.getContext('2d');x.fillStyle='#111214';x.fillRect(0,0,1680,940);x.drawImage(a,10,20);x.drawImage(b,850,20);
  x.fillStyle='#f4f4f2';x.font='600 30px Kumbh Sans,sans-serif';x.textBaseline='middle';x.fillText('EM Visions — '+summary(),40,895);
  const snapB=await new Promise(r=>c.toBlob(r,'image/jpeg',.88)),orig=[];
  let tot=0;for(const s of sidesOf(p)){const ar=S.art[s];if(ar&&ar.file&&tot+ar.file.size<8e6){tot+=ar.file.size;orig.push({name:ar.file.name,type:ar.file.type,blob:ar.file})}}
  const db=await idb();await new Promise((ok,ko)=>{const tx=db.transaction('kv','readwrite');tx.objectStore('kv').put({snap:snapB,snapName:`maquette-${p.id}.jpg`,orig,summary:summary(),at:Date.now()},'maquette');tx.oncomplete=ok;tx.onerror=()=>ko(tx.error)});
  location.href=$('#send').dataset.to}
 catch(err){console.error(err);apply();btn.disabled=false;toast(t('La maquette n’a pas pu être préparée. Réessayez.','The mockup could not be prepared. Please try again.'))}}
$('#send').onclick=send;addEventListener('pageshow',()=>{$('#send').disabled=false});

// ---------- démarrage ----------
const Q=new URLSearchParams(location.search);if(Q.get('p')){const i=PRODUCTS.findIndex(p=>p.id===Q.get('p'));if(i>=0)S.pi=i}
{const v=view(PRODUCTS[S.pi]);if(v.pitch!==undefined)S.pitch=v.pitch}
uiProducts();uiAll();resize();load();requestAnimationFrame(frame);
(document.fonts&&document.fonts.ready||Promise.resolve()).then(()=>{for(const k in guides){guides[k].dispose();delete guides[k]}apply()});
// outil de fabrication des vignettes (img/m3d/) et vérifications
window.__m3d={S,PRODUCTS,THREE,R,scene,key,fill,rim,load,pick,apply,uiAll,shot,snap,summary,imageTex,get cur(){return cur},ready:()=>cache[PRODUCTS[S.pi].id]};
