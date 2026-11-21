# Petit serveur de test : sert le site avec les en-têtes de site/_headers (comme Netlify), compresse le texte, et répond 200 aux envois du formulaire.
import http.server,sys,os,json,fnmatch,gzip
ROOT=sys.argv[2] if len(sys.argv)>2 else '../../site'
def rules():
    R=[];cur=None
    for l in open(os.path.join(ROOT,'_headers')):
        if l.startswith('#') or not l.strip():continue
        if not l.startswith(' '):cur=(l.strip(),[]);R.append(cur)
        else:k,v=l.strip().split(':',1);cur[1].append((k,v.strip()))
    return R
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k):super().__init__(*a,directory=ROOT,**k)
    def end_headers(s):
        p=s.path.split('?')[0]
        for pat,hs in rules():
            if fnmatch.fnmatch(p,pat.replace('/*','/*')) or pat=='/*':
                for k,v in hs:s.send_header(k,v)
        super().end_headers()
    def send_error(s,code,msg=None,explain=None):
        if code==404 and os.path.exists(os.path.join(ROOT,'404.html')):
            b=open(os.path.join(ROOT,'404.html'),'rb').read();s.send_response(404);s.send_header('Content-Type','text/html; charset=utf-8');s.send_header('Content-Length',str(len(b)));s.end_headers();s.wfile.write(b);return
        super().send_error(code,msg,explain)
    def do_GET(s):
        # compression comme chez Netlify, pour les fichiers texte
        p=s.path.split('?')[0];f=os.path.join(ROOT,p.lstrip('/'))
        if os.path.isdir(f):f=os.path.join(f,'index.html')
        if 'gzip' in s.headers.get('Accept-Encoding','') and os.path.isfile(f) and f.endswith(('.html','.js','.css','.json','.svg','.glb')):
            b=gzip.compress(open(f,'rb').read(),6);ct={'html':'text/html; charset=utf-8','js':'text/javascript','css':'text/css','json':'application/json','svg':'image/svg+xml','glb':'model/gltf-binary'}[f.rsplit('.',1)[1]]
            s.send_response(200);s.send_header('Content-Type',ct);s.send_header('Content-Encoding','gzip');s.send_header('Content-Length',str(len(b)));s.end_headers();s.wfile.write(b);return
        return super().do_GET()
    def do_POST(s):
        n=int(s.headers.get('Content-Length',0));b=s.rfile.read(n)
        s.send_response(200);s.send_header('Content-Type','text/html');s.end_headers();s.wfile.write(b'ok')
    def log_message(s,*a):pass
http.server.ThreadingHTTPServer(('',int(sys.argv[1])),H).serve_forever()
