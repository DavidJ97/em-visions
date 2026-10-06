// Cherche des modèles candidats : interroge la recherche publique de Sketchfab (modèles téléchargeables sous
// licence libre), ne garde que ceux présents dans la copie publique Objaverse, les télécharge dans raw/ et écrit
// candidats.json (même format que models.json) pour pouvoir les préparer et les regarder.
// Usage : node chercher.mjs "hoodie" "sweatpants" ...
import fs from 'fs';import zlib from 'zlib';
const N=+(process.env.N||8),Q=process.argv.slice(2),out={};
const paths=JSON.parse(zlib.gunzipSync(Buffer.from(await (await fetch('https://huggingface.co/datasets/allenai/objaverse/resolve/main/object-paths.json.gz')).arrayBuffer())));
fs.mkdirSync('raw',{recursive:true});
for(const q of Q){let n=0;const slug=q.replace(/[^a-z0-9]+/gi,'-').toLowerCase();
 for(const lic of ['by','cc0']){let url=`https://api.sketchfab.com/v3/search?type=models&q=${encodeURIComponent(q)}&downloadable=true&license=${lic}&sort_by=-likeCount&count=24`;
  for(let page=0;page<3&&url&&n<N;page++){const r=await (await fetch(url)).json();url=r.next;
   for(const m of r.results||[]){if(n>=N)break;const p=paths[m.uid];if(!p||m.faceCount>1500000||m.animationCount>0)continue;
    const res=await fetch('https://huggingface.co/datasets/allenai/objaverse/resolve/main/'+p);if(!res.ok)continue;fs.writeFileSync(`raw/${m.uid}.glb`,Buffer.from(await res.arrayBuffer()));
    const id=`${slug}-${++n}`;out[id]={uid:m.uid,path:p,tris:40000,solid:['.*'],credit:[m.name,m.user.displayName,m.user.username],lic,faces:m.faceCount,likes:m.likeCount};
    console.log(id,m.uid,lic,m.faceCount,'|',m.name,'|',m.user.displayName)}}}}
fs.writeFileSync('candidats.json',JSON.stringify(out,null,1));
