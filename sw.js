const CACHE='aura-shell-v19';
const SHELL=['./','./index.html','./manifest.webmanifest','./icon-32.png','./icon-180.png','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('aura-shell-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
 const u=new URL(e.request.url);
 if(e.request.method!=='GET'||u.origin!==self.location.origin||!u.pathname.startsWith(new URL(self.registration.scope).pathname))return;
 if(e.request.mode==='navigate'||u.pathname.endsWith('/index.html')){
 e.respondWith(fetch(e.request).then(r=>{if(r.ok){const copy=r.clone();e.waitUntil(caches.open(CACHE).then(c=>c.put('./index.html',copy)));}return r;}).catch(()=>caches.match('./index.html')));return;
 }
 if(u.pathname.endsWith('/data/guia.json'))return;
 if(SHELL.some(x=>new URL(x,self.registration.scope).pathname===u.pathname)){
 e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)));
 }
});
