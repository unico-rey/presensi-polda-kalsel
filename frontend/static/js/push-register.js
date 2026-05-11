// ============================================
// Push Notification Registration Script
// Presensi Polda Kalsel
// ============================================

(function () {
    "use strict";

    function urlBase64ToUint8Array(base64String) {
        const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
        const base64 = (base64String + padding).replace(/\-/g, "+").replace(/_/g, "/");
        const rawData = atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }

    async function registerPush(idAnggota = null) {
        if (!("serviceWorker" in navigator) || !("PushManager" in window)) {
            console.warn("Push not supported");
            return false;
        }

        try {
            const registration = await navigator.serviceWorker.register("/sw.js", { scope: "/" });
            await navigator.serviceWorker.ready;

            let permission = Notification.permission;
            if (permission === "default") {
                permission = await Notification.requestPermission();
            }

            if (permission !== "granted") return false;

            const vapidRes = await fetch("/anggota/push/vapid-public-key");
            const vapidData = await vapidRes.json();
            const applicationServerKey = urlBase64ToUint8Array(vapidData.public_key);

            let subscription = await registration.pushManager.getSubscription();
            if (!subscription) {
                subscription = await registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: applicationServerKey,
                });
            }

            // Pilih endpoint: privat (dengan cookie) atau publik (dengan id_anggota)
            let endpoint = "/anggota/push/subscribe";
            let body = {
                endpoint: subscription.endpoint,
                keys: {
                    p256dh: btoa(String.fromCharCode.apply(null, new Uint8Array(subscription.getKey("p256dh")))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""),
                    auth: btoa(String.fromCharCode.apply(null, new Uint8Array(subscription.getKey("auth")))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""),
                }
            };

            if (idAnggota) {
                endpoint = `/anggota/push/subscribe-public?id_anggota=${idAnggota}`;
            }

            const response = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            });

            return response.ok;
        } catch (err) {
            console.error("Push Error:", err);
            return false;
        }
    }

    window.registerPushNotification = registerPush;
})();
