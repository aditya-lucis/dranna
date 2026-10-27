# anna/src/pix/pwa_manifest.py — generator konfigurasi Progressive Web App (PWA)
"""
PWA Manifest & Offline Resilience (Bab 126):
- Konfigurasi Web App Manifest untuk instalasi multi-device (Android, iOS, Desktop)
- Mendukung mode tampilan Standalone dengan palet warna Zen & Warmth
- Menautkan ikon resmi karakter Dr. Anna Reed
"""
import json


def buat_pwa_manifest() -> dict:
    """Menghasilkan spesifikasi standar W3C Web App Manifest untuk Dr. Anna Reed."""
    return {
        "name": "Dr. Anna Reed — AI Companion & Mental Health",
        "short_name": "Dr. Anna",
        "description": "Pendamping Emosional Klinis & Psikoedukasi Berbasis Bukti",
        "start_url": "/",
        "display": "standalone",
        "orientation": "portrait-primary",
        "background_color": "#FAF7F5",
        "theme_color": "#F43F5E",
        "categories": ["health", "lifestyle", "medical"],
        "icons": [
            {
                "src": "/assets/img/01134ab7-5052-4e91-9d6a-7753694fe140.webp",
                "sizes": "192x192",
                "type": "image/webp",
                "purpose": "any maskable",
            },
            {
                "src": "/assets/img/44485f8a-4449-4275-975b-e84db6ed1be9.webp",
                "sizes": "512x512",
                "type": "image/webp",
                "purpose": "any maskable",
            },
        ],
    }
