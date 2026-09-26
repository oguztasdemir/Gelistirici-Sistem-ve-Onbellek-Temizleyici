#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cache Cleaner - Geliştirici Sistem & Önbellek Temizleyici
Modern Masaüstü Önbellek ve Disk Alanı Geri Kazanım Aracı
"""

import sys
import subprocess

# Gerekli kütüphaneleri kontrol et ve gerekirse otomatik kur
try:
    import customtkinter
except ImportError:
    print("[Cache Cleaner] 'customtkinter' kütüphanesi bulunamadı. Otomatik yükleniyor...")
    subprocess.run([sys.executable, "-m", "pip", "install", "customtkinter>=5.2.0"], check=True)

try:
    from src.ui.app import CacheCleanerApp
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from src.ui.app import CacheCleanerApp


def main():
    """Uygulama ana başlatıcı fonksiyonu."""
    app = CacheCleanerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
