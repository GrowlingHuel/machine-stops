// This service worker unregisters itself and clears all caches.
// It exists solely to clean up previously registered service workers.
self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.map(k => caches.delete(k))))
      .then(() => self.registration.unregister())
      .then(() => self.clients.matchAll())
      .then(clients => clients.forEach(c => c.navigate(c.url)))
  );
});
