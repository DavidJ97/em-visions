# Cuit le masque du logo pour l'effet de verre de l'accueil -> out/img/logo-verre.webp (1024 x 512, sans perte).
#   rouge = la forme du logo, vert = son relief (arrondi des bords), bleu = la forme très adoucie (ombre et loupe).
# À relancer seulement si le logo change :  python3 verre.py
import asyncio,io
from playwright.async_api import async_playwright
from PIL import Image
import numpy as np
from scipy import ndimage as nd
V=open('logo_vb.txt').read().strip(); D=open('logo_path.txt').read().strip()
W,H,LW=1024,512,920
x,y,w,h=map(float,V.split()); LH=round(LW*h/w)
async def shot():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':W,'height':H})
        await pg.set_content(f'<body style="margin:0;background:#000"><svg viewBox="{V}" width="{LW}" height="{LH}" style="position:absolute;left:{(W-LW)//2}px;top:{(H-LH)//2}px"><path fill="#fff" fill-rule="evenodd" d="{D}"/></svg>')
        png=await pg.screenshot(); await b.close(); return png
a=np.asarray(Image.open(io.BytesIO(asyncio.run(shot()))).convert('L')).astype(np.float32)/255
d=np.clip(nd.distance_transform_edt(a>.5)/11,0,1); relief=nd.gaussian_filter(d*d*(3-2*d),1.8)
large=np.clip(nd.gaussian_filter(a,22)*2.2,0,1)
Image.fromarray((np.dstack([a,relief,large])*255).round().astype(np.uint8),'RGB').save('out/img/logo-verre.webp',lossless=True,method=6)
