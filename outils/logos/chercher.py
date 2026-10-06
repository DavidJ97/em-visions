"""Tâche ponctuelle : va chercher le logo officiel de chaque fournisseur sur son propre site."""
import re, os, json, urllib.request, urllib.parse, html
UA={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36','Accept-Language':'fr-CA,fr;q=0.9,en;q=0.8'}
SITES={'ss':['https://fr-ca.ssactivewear.com/','https://www.ssactivewear.com/'],'canada':['https://canadasportswear.com/'],'fabrik':['https://fabrik.ca/','https://fabrik.ca/en-ca/'],
       'eside':['https://eside.ca/fr/'],'jlh':['https://www.justlikehero.com/'],'projob':['https://www.projob.com/','https://www.projob.se/','https://texet.ca/pages/projob','https://texet.ca/']}
DIRECT={'canada':['https://canadasportswear.com/cdn/shop/files/Canada_Sportswear_logo_-_stacked_-_2_6d9f9168-b3b8-42cb-86bb-9e359c0c8c79.jpg'],
        'eside':['https://eside.ca/wp-content/uploads/2015/06/eside-logo-menu-1024x428.png','https://eside.ca/wp-content/uploads/2015/06/eside-icone.png'],
        'jlh':['https://www.justlikehero.com/cdn/shop/files/Just_Like_Hero_-_Black_Logo_Trans_BG_-_Low_Res..png']}
def get(u,binary=False):
    r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=25);d=r.read()
    return d if binary else d.decode('utf-8','replace')
os.makedirs('import/logos',exist_ok=True);rep={}
for k,urls in SITES.items():
    cand=list(DIRECT.get(k,[]));n=0;rep[k]=[]
    for u in urls:
        try: h=get(u)
        except Exception as e: rep[k].append(f'{u} : {e}');continue
        rep[k].append(f'{u} : {len(h)} octets')
        for m in re.finditer(r'''(?:src|data-src|href|content|srcset|data-srcset)=["']([^"']*logo[^"']*?\.(?:svg|png|webp|jpe?g)[^"' ]*)''',h,re.I):
            c=urllib.parse.urljoin(u,html.unescape(m.group(1)).split(' ')[0].split(',')[0])
            if c not in cand: cand.append(c)
        for m in re.finditer(r'''["'(]([^"'() ]*logo[^"'() ]*?\.(?:svg|png|webp))''',h,re.I):
            c=urllib.parse.urljoin(u,html.unescape(m.group(1)).replace('\\/','/'))
            if c not in cand: cand.append(c)
        # logos dessinés directement dans la page (SVG en ligne dans l'en-tête ou dans un lien « logo »)
        for i,m in enumerate(re.finditer(r'<svg\b[^>]*>.*?</svg>',h[:400000],re.S)):
            ctx=h[max(0,m.start()-400):m.start()].lower()
            if ('logo' in ctx or 'logo' in m.group(0)[:300].lower() or 'sketch' in m.group(0)[:600].lower()) and len(m.group(0))>600 and n<6:
                s=m.group(0)
                if 'xmlns=' not in s[:300]: s=s.replace('<svg','<svg xmlns="http://www.w3.org/2000/svg"',1)
                open(f'import/logos/{k}-inline{n}.svg','w').write(s);rep[k].append(f'  svg en ligne {n} : {len(s)} octets');n+=1
    for i,c in enumerate(cand[:10]):
        try:
            d=get(c,True);ext=re.search(r'\.(svg|png|webp|jpe?g)',c,re.I).group(1).lower();open(f'import/logos/{k}-{i}.{ext}','wb').write(d);rep[k].append(f'  {i} {c} : {len(d)} octets')
        except Exception as e: rep[k].append(f'  {i} {c} : {e}')
open('import/logos/rapport.json','w').write(json.dumps(rep,indent=1,ensure_ascii=False))
