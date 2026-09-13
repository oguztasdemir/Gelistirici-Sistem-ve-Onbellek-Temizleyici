# 🧹 Geliştirici Disk & Sistem Önbellek Temizleme Aracı

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blue?style=for-the-badge)
![Windows Shell](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Multi-threading](https://img.shields.io/badge/Engine-Asynchronous_Threads-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

> ⚡ **Yazılım geliştirme ortamlarında şişen pip, npm, HuggingFace, PyTorch, tarayıcı ve işletim sistemi önbelleklerini derinlemesine tarayıp gigabaytlarca gereksiz veriyi tek tıkla güvenle temizleyen modern masaüstü aracı.**

---

## 📖 Genel Bakış & Problem Tanımı

Yapay zeka modelleri (**HuggingFace, PyTorch, Ollama**), derleme kalıntıları (**node_modules, .next, target**), **pip / npm** paket havuzları ve Windows geçici dizinleri geliştirici bilgisayarlarının SSD disklerini fark ettirmeden **30–50 GB** seviyesinde doldurur.

Geleneksel disk temizleme yazılımları geliştirici ortamlarının önbellek yollarını tanımaz veya hangi klasörün ne kadar yer kapladığını şeffafça göstermez. **Geliştirici Önbellek Temizleyici**, yazılımcılara özel olarak geliştirilmiş, sistem kilitlenmelerini engelleyen asenkron ve güvenli bir bakım motoru sunar.

---

## ✨ Öne Çıkan Özellikler

* **👨‍💻 Geliştirici Önbellekleri (Dev Ecosystem):**
  * Python `pip-cache` ve `.cache/pip` paket havuzları
  * Node.js `npm-cache` ve geçici paket artıkları
  * PyTorch & HuggingFace model indirme kalıntıları
* **🌐 Web Tarayıcı Önbellekleri (Browser Cache):**
  * Google Chrome, Microsoft Edge, Brave Browser önbellek ve çerez kalıntıları
* **🪟 Windows İşletim Sistemi Artıkları:**
  * `Windows Temp` (`%TEMP%` & `C:\Windows\Temp`)
  * `Prefetch` dizini ve Windows Hata Dökümleri (`CrashDumps`)
* **🎨 Modern CustomTkinter Arayüzü:**
  * Koyu tema (Dark Mode) destekli modern ve şık kullanıcı deneyimi
  * Gerçek zamanlı ilerleme çubukları ve anlık disk alanı geri kazanım sayacı
* **⚡ Donmayan Asenkron Motor:**
  * Çoklu iş parçacığı (Multi-threading) mimarisi sayesinde tarama ve silme sırasında arayüz asla donmaz.

---

## 🏗️ Taranan Dizinler & Rotalar

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      GELİŞTİRİCİ ÖNBELLEK TEMİZLEYİCİ                   │
├──────────────────────────┬──────────────────────────────────────────────┤
│ Hedef Alan               │ Dizin Yolu / Açıklama                         │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Python pip Cache         │ %LocalAppData%\pip\cache                     │
│ Node.js npm Cache        │ %AppData%\npm-cache                          │
│ Windows Kullanıcı Temp   │ %LocalAppData%\Temp                          │
│ Windows Sistem Temp      │ C:\Windows\Temp                              │
│ Windows Prefetch         │ C:\Windows\Prefetch                          │
│ Google Chrome Cache      │ %LocalAppData%\Google\Chrome\User Data\...   │
│ Microsoft Edge Cache     │ %LocalAppData%\Microsoft\Edge\User Data\...  │
│ Brave Browser Cache      │ %LocalAppData%\BraveSoftware\Brave-Browser.. │
└──────────────────────────┴──────────────────────────────────────────────┘
```

---

## 🚀 Kurulum ve Çalıştırma

### 1. Gereksinimler:
* Python 3.10 veya üzeri
* Windows 10 / 11

### 2. Başlatma:
```bash
# Bağımlılığı yükleyin (Gerekirse uygulama otomatik olarak da yükler):
pip install customtkinter

# Uygulamayı başlatın:
python cache_cleaner.py
```

---

## 👨‍💻 Geliştirici
**Oğuz Taşdemir**  
*Systems Architect & Full-Stack Developer*  
- GitHub: [@oguztasdemir](https://github.com/oguztasdemir)
