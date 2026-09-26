# 🚀 Geliştirici Sistem & Önbellek Temizleme Aracı (Cache Cleaner) - Yenileme & Mimari Planı

Bu belge, **Cache Cleaner (Geliştirici Sistem & Önbellek Temizleme Aracı)** projesinin modüler mimariye dönüştürülmesi, arayüz sorunlarının giderilmesi, detaylı dosya denetimi/özel seçim özelliklerinin eklenmesi ve modernleştirilmesine yönelik yol haritasını içermektedir.

---

## 1. 🎯 Hedefler ve İyileştirmeler

1. **Modüler Klasör Yapısı ve `main.py` Giriş Noktası**:
   - `cache_cleaner.py` tek parça dosyasından profesyonel, modüler Python mimarisine geçiş.
   - Temiz ayrım: Çekirdek motor (`core/`), Arayüz bileşenleri (`ui/`), Yardımcı araçlar (`utils/`) ve Yapılandırma (`config.py`).
   - Ana başlatıcı `main.py` oluşturulması.

2. **Proje İsimlendirmesi ve Markalama**:
   - Eski "Cortex Cleaner" ibareleri tamamen kaldırılarak GitHub deposu ve dokümanlarıyla uyumlu **"Cache Cleaner - Geliştirici Sistem & Önbellek Temizleyici"** adına geçiş.

3. **Arayüz (UI/UX) Sorunlarının Çözülmesi & Responsive Tasarım**:
   - **Tıklanamama / Pencere Taşması Sorununun Çözümü:** Sabit boyutlu kısıtlı pencere yerine esnek (`responsive`), minimum boyut garantili (`minsize: 850x650`, varsayılan `960x720`) ve butonların her zaman ekranın alt kısmında sabit/tıklanabilir kaldığı grid/pack düzeni.
   - **Modern Glassmorphism & Dark Mode:** Özel renk paletleri, modern butonlar, durum rozetleri (badges).

4. **Yeni Özellikler & Detay Yönetimi (Granular File Inspector)**:
   - **🔍 Detaylı İnceleme Modalı (Detail Dialog):** Her önbellek hedefi için alt klasör ve dosyaları listeleme, boyutlarını gösterme.
   - **🛡️ Özel Seçim / Hariç Tutma (Exclusion):** Kullanıcının "bu alt klasörü veya dosyayı silme" diyebileceği seçilebilir onay kutuları (checkbox).
   - **📂 Dosya Gezgininde Aç:** Hedef dizini tek tıkla Windows Gezgini'nde açma.
   - **🏷️ Kategori Filtreleme & Hızlı Seçim:** "Tümünü Seç", "Hiçbirini Seçme", "Sadece Geliştirici Araçları", "Sadece Sistem".
   - **⚡ Genişletilmiş Temizleme Hedefleri:** Pip, NPM, PyTorch, HuggingFace, VS Code, Cursor, Docker, Conda, Gradle, Temp, DNS, Chrome, Edge, Spotify, Crash Dumps.
   - **📊 Canlı İstatistikler & Güvenli Temizlik:** Kilitli dosyaları atlayarak çökmeden devam etme, temizlenen toplam net alan raporu.

---

## 2. 📂 Yeni Klasör ve Modül Mimarisi

```text
önbellek temizleyici/
├── main.py                        # Uygulama ana giriş noktası
├── requirements.txt               # Bağımlılıklar (customtkinter, psutil vb.)
├── README.md                      # Proje tanıtım dokümanı
├── PLANLAMA.md                    # Bu mimari ve geliştirme planı
├── LICENSE                        # MIT Lisansı
├── docs/                          # Görseller ve dökümantasyon
└── src/
    ├── __init__.py
    ├── config.py                  # Sabitler, temalar, hedef tanımları ve kategoriler
    ├── core/
    │   ├── __init__.py
    │   ├── scanner.py             # Asenkron çok iş parçacıklı (threaded) dosya ve komut tarayıcısı
    │   └── cleaner.py             # Güvenli dosya silme, hariç tutulanları koruma, komut çalıştırma
    ├── ui/
    │   ├── __init__.py
    │   ├── app.py                 # Ana CustomTkinter penceresi ve ana döngü
    │   ├── components/
    │   │   ├── __init__.py
    │   │   ├── header.py          # Üst başlık, logo, özet bilgi ve kategori filtre butonları
    │   │   ├── target_card.py     # Önbellek hedef kartı (onay kutusu, boyut, detay & klasör butonu)
    │   │   ├── log_panel.py       # Katlanabilir/temizlenebilir işlem günlüğü konsolu
    │   │   └── footer.py          # İlerleme çubuğu ve her zaman görünür/tıklanabilir eylem butonları
    │   └── dialogs/
    │       ├── __init__.py
    │       └── detail_dialog.py   # Alt dosya/klasör listesi, hariç tutma seçimleri ve arama filtresi
    └── utils/
        ├── __init__.py
        ├── formatters.py          # Bayt formatlayıcı (B, KB, MB, GB), süre dönüştürücü
        └── system_helper.py       # Windows dizin yolları, yetki ve gezgin açma yardımcıları
```

---

## 3. 🛠️ Uygulama Aşamaları

1. **Adım 1:** `src/` mimarisinin oluşturulması ve `config.py`, `utils/` modüllerinin kodlanması.
2. **Adım 2:** `core/scanner.py` ve `core/cleaner.py` motorlarının yazılması (alt öğe ağacı tarama ve hariç tutma desteği ile).
3. **Adım 3:** `ui/dialogs/detail_dialog.py` detay inceleme ve filtreleme modalının kodlanması.
4. **Adım 4:** `ui/components/` ve `ui/app.py` responsive arayüzünün oluşturulması (tıklama ve taşma sorunlarının çözülmesi).
5. **Adım 5:** `main.py` giriş noktasının hazırlanması ve `cache_cleaner.py` dosyasının taşınması/arşivlenmesi.
6. **Adım 6:** Test ve doğrulama yapılması.
