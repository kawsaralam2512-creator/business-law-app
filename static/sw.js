const CACHE_NAME = 'business-law-cache-v2';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/manifest.json',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png'
];

// Install Service Worker
self.addEventListener('install', event => {
  self.skipWaiting(); // নতুন সার্ভিস ওয়ার্কারকে সাথে সাথে অ্যাক্টিভ হতে বলে
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch from Cache
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // যদি ক্যাশে থাকে, ক্যাশ থেকে দিবে, না থাকলে ইন্টারনেট থেকে লোড করবে
        return response || fetch(event.request);
      })
  );
});

// Activate and Clean old caches
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName); // পুরোনো ক্যাশ ডিলিট করে দিবে
          }
        })
      );
    }).then(() => self.clients.claim()) // নতুন ক্যাশকে সাথে সাথে নিয়ন্ত্রণ নিতে বলে
  );
});