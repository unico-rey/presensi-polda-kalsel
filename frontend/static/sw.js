// ============================================
// Service Worker - Presensi Polda Kalsel
// Handles Push Notifications for attendance
// ============================================

self.addEventListener("install", function (event) {
    console.log("[SW] Service Worker installed");
    self.skipWaiting();
});

self.addEventListener("activate", function (event) {
    console.log("[SW] Service Worker activated");
    event.waitUntil(clients.claim());
});

self.addEventListener("push", function (event) {
    console.log("[SW] Push event received");

    let data = {
        title: "Pengingat Presensi",
        body: "Jangan lupa presensi hari ini!",
    };

    if (event.data) {
        try {
            data = event.data.json();
        } catch (e) {
            data.body = event.data.text();
        }
    }

    const options = {
        body: data.body,
        icon: "/static/logo-polri.png",
        badge: "/static/logo-polri.png",
        vibrate: [200, 100, 200, 100, 200, 100, 200],
        tag: "presensi-reminder",
        renotify: true,
        actions: [
            {
                action: "absen-sekarang",
                title: "🔓 Buka Presensi",
            },
            {
                action: "dismiss",
                title: "❌ Tutup",
            },
        ],
        requireInteraction: true,
        data: {
            url: "/absensi/",
        },
    };

    event.waitUntil(self.registration.showNotification(data.title, options));
});

self.addEventListener("notificationclick", function (event) {
    event.notification.close();

    if (event.action === "dismiss") {
        return;
    }

    // Default action or 'absen-sekarang': open the attendance page
    const targetUrl = event.notification.data?.url || "/absensi/";

    event.waitUntil(
        clients.matchAll({ type: "window", includeUncontrolled: true }).then(function (clientList) {
            // If there's already an open window, focus it
            for (let i = 0; i < clientList.length; i++) {
                const client = clientList[i];
                if (client.url.includes("/absensi") && "focus" in client) {
                    return client.focus();
                }
            }
            // Otherwise open new window
            if (clients.openWindow) {
                return clients.openWindow(targetUrl);
            }
        })
    );
});
