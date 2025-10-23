// Simple service worker for offline play
const CACHE_NAME = 'tj-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/assets/icons/tom-icon.png',
  '/assets/icons/jerry-icon.png',
  '/assets/audio/chase-theme.mp3',
  '/assets/audio/win-sound.mp3',
  '/assets/audio/lose-sound.mp3',
  '/assets/sprites/house-bg.png',
  '/assets/sprites/tom-run.png',
  '/assets/sprites/jerry-run.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});
