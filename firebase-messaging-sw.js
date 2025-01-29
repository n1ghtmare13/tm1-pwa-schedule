import { initializeApp } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-app.js";
import { getMessaging, onBackgroundMessage } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-messaging.js";

const firebaseConfig = {
        apiKey: "AIzaSyAujO6hUv2-G18r132CqP4cvXpGhhOsXa8",
        authDomain: "tm1-pwa-schedule.firebaseapp.com",
        projectId: "tm1-pwa-schedule",
        storageBucket: "tm1-pwa-schedule.firebasestorage.app",
        messagingSenderId: "39753485339",
        appId: "1:39753485339:web:995bd4f54267698d883cbe",
        measurementId: "G-59X84T0KB1"
};

const app = initializeApp(firebaseConfig);

const messaging = getMessaging(app);

onBackgroundMessage(messaging, (payload) => {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);

    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: payload.notification.image || 'assets/icon.png',
    };

    return self.registration.showNotification(notificationTitle, notificationOptions);
});
