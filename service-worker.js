const CACHE_NAME = 'plan-zastepstwa-cache-v1';
const urlsToCache = [
    'index.html',
    'style.css',
    'script.js',
    'manifest.json',
    'assets/icon.png',
    'schedule.html',
    'substitutions.html'
];

self.addEventListener('install', event => {
    event.waitUntil(
      caches.open(CACHE_NAME)
        .then(cache => {
          return cache.addAll(urlsToCache);
        })
    );
  });

  self.addEventListener('fetch', event => {
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          return response || fetch(event.request);
        })
    );
  });
