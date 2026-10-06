// Prépare les modèles 3D du modélisateur : allège la géométrie, retire ou neutralise les couleurs
// d'origine des matières à teinter, compresse textures et maillage.
// Entrée : raw/<uid>.glb (modèles Sketchfab sous licence CC BY, copie Objaverse) ; sortie : ../../site/models/<id>.glb
import {NodeIO,Logger} from '@gltf-transform/core';import {ALL_EXTENSIONS} from '@gltf-transform/extensions';
import {dedup,flatten,join,weld,simplify,prune,textureCompress,meshopt} from '@gltf-transform/functions';
import {MeshoptSimplifier,MeshoptEncoder,MeshoptDecoder} from 'meshoptimizer';import sharp from 'sharp';import fs from 'fs';
await MeshoptSimplifier.ready;await MeshoptEncoder.ready;await MeshoptDecoder.ready;
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.decoder':MeshoptDecoder,'meshopt.encoder':MeshoptEncoder});
const M=JSON.parse(fs.readFileSync('models.json','utf8')),OUT=process.env.OUT||'../../site/models';fs.mkdirSync(OUT,{recursive:true});
const only=process.argv.slice(2),rep={};let fail=0;
const count=root=>{let t=0;for(const mesh of root.listMeshes())for(const p of mesh.listPrimitives()){const i=p.getIndices();t+=(i?i.getCount():p.getAttribute('POSITION').getCount())/3}return Math.round(t)};
for(const [id,c] of Object.entries(M)){if(only.length&&!only.includes(id))continue;try{
 const doc=await io.read(`raw/${c.uid}.glb`),root=doc.getRoot();doc.setLogger(new Logger(Logger.Verbosity.SILENT));const is=(n,l)=>(l||[]).some(r=>new RegExp(r).test(n));
 for(const n of root.listNodes())if(is(n.getName(),c.drop))n.dispose();
 for(const m of root.listMaterials()){const n=m.getName();m.setDoubleSided(true);const mode=is(n,c.solid)?'solid':is(n,c.gray)?'gray':is(n,c.mul)?'mul':'';
  if(mode==='solid')m.setBaseColorTexture(null).setBaseColorFactor([1,1,1,1]);
  if(mode==='gray'){const t=m.getBaseColorTexture();if(t){const img=sharp(Buffer.from(t.getImage())).resize(1024,1024,{fit:'inside'}).removeAlpha().grayscale(),mean=(await img.clone().stats()).channels[0].mean||128;
    t.setImage(await img.linear(Math.min(6,208/mean),0).png().toBuffer()).setMimeType('image/png')}m.setBaseColorFactor([1,1,1,1])}
  if(mode)m.setExtras({...m.getExtras(),tint:mode})}
 await doc.transform(prune(),dedup(),flatten(),join({keepNamed:false}),weld());const tris=count(root);
 if(tris>c.tris*1.15)await doc.transform(simplify({simplifier:MeshoptSimplifier,ratio:c.tris/tris,error:0.004}));
 await doc.transform(prune(),textureCompress({encoder:sharp,targetFormat:'webp',resize:[1024,1024],quality:80}),meshopt({encoder:MeshoptEncoder,level:'medium'}));
 await io.write(`${OUT}/${id}.glb`,doc);rep[id]={tris,after:count(root),ko:Math.round(fs.statSync(`${OUT}/${id}.glb`).size/1024)};console.log(id,JSON.stringify(rep[id]))}
 catch(e){fail++;console.log(id,'ÉCHEC',String(e).slice(0,300))}}
console.log('terminé,',Object.keys(rep).length,'modèles,',fail,'échec(s)');process.exit(fail?1:0)
