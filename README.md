# ⚡ Cache Cleaner - Professional Developer & System Disk Recovery Suite

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![UI: CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-10B981?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com/windows)
[![i18n: EN & TR](https://img.shields.io/badge/i18n-English%20%7C%20T%C3%BCrk%C3%A7e-38BDF8?style=for-the-badge)](https://github.com/oguztasdemir/cache-cleaner)

**A high-performance desktop suite designed for developers and power users to deeply scan, inspect, and safely reclaim gigabytes of disk space from package managers, AI model weights, build dependencies, dormant files, and system junk.**

[English](#-english-documentation) • [Türkçe](#-türkçe-dokümantasyon) • [Installation](#-installation--quick-start) • [Architecture](#-project-architecture)

</div>

---

## 🌟 Key Modules & Features

### 1. 🧹 Deep System & Cache Cleaner (42+ Targets)
- **Developer Package Caches:** Python `pip`, `uv`, Node.js `npm`, `yarn`, `pnpm`, `node-gyp`, Python `jedi`.
- **AI & ML Models:** PyTorch hub checkpoints, HuggingFace model cache, Ollama local LLMs.
- **IDE & Editors:** VS Code, Cursor, JetBrains IDEs (PyCharm, IntelliJ, CLion), Gradle, Maven, Electron runtime caches.
- **Hardware & GPU Shaders:** NVIDIA, DirectX, AMD shader caches, Windows CBS/DISM logs, Windows Update downloads (`SoftwareDistribution`), Windows crash dumps, DNS resolver flush.
- **Browsers & Media:** Google Chrome, Microsoft Edge, Brave, Telegram Desktop, Discord, Slack, Zoom, Steam, Epic Games, EA App, Spotify.

### 2. 💻 Project Dependency Cleaner
- Recursively cleans abandoned developer directories:
  - `node_modules` (JS/TS dependencies)
  - `venv`, `.venv`, `env` (Python virtual environments)
  - `target/` (Rust Cargo build outputs)
  - `build/`, `dist/`, `.next/`, `.nuxt/` (Web/App build caches)

### 3. 🔍 Large File & Disk Analyzer
- Discovers heavy files (> 50 MB, 100 MB, 500 MB, 1 GB, 2 GB+) consuming storage.
- Classifies files into categories: Videos, Disk Images (`.iso`, `.vhdx`), Archives (`.zip`, `.7z`), AI models (`.safetensors`, `.gguf`, `.pth`).

### 4. 👯‍♂️ Duplicate File Finder
- Fast MD5 hash-based duplicate finder with 1-click smart auto-selection of extra copies.

### 5. 🚀 Windows Startup Manager
- Inspects and manages background applications that start automatically on Windows boot.

### 6. 🛡️ Permanent Whitelist & Lifetime Stats
- Permanent file/folder protection against accidental deletion.
- Real-time tracker for lifetime recovered gigabytes and cleaning sessions.

### 7. 🌍 Modern Left Sidebar & Instant i18n
- Modern Obsidian/Emerald dark dashboard.
- Live C: drive storage gauge.
- Seamless, restart-free language toggle (`🇹🇷 TR` / `🇬🇧 EN`).
- Live search and filter bar across all 42+ targets.

---

## 🚀 Installation & Quick Start

### Prerequisites
- Windows 10 / 11
- Python 3.10 or higher

### Option A: Clone & Run (Recommended)
```powershell
# 1. Clone repository
git clone https://github.com/oguztasdemir/cache-cleaner.git
cd cache-cleaner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch application
python main.py
```
*(Or simply double-click `run.bat` on Windows)*

### Option B: Build Standalone Windows Executable (.exe)
```powershell
python build_exe.py
```
The compiled executable will be located in `dist/CacheCleaner.exe`.

---

## 📂 Project Architecture

```text
cache-cleaner/
├── main.py                        # Modern Application Entry Point
├── run.bat                        # 1-Click Windows Batch Launcher
├── build_exe.py                   # Automated PyInstaller Executable Builder
├── requirements.txt               # Dependencies (customtkinter, psutil)
├── LICENSE                        # MIT License
├── README.md                      # GitHub Showcase Documentation
├── PLANLAMA.md                    # Technical Architecture & Planning
└── src/
    ├── config.py                  # 42+ Cache Targets, Colors & Theme Tokens
    ├── i18n.py                    # Multi-language Engine (Turkish & English)
    ├── core/
    │   ├── scanner.py             # Multi-threaded high performance cache scanner
    │   ├── cleaner.py             # Error-resilient safe deletion engine
    │   ├── project_cleaner.py     # Recursive project dependency cleaner
    │   ├── large_files.py         # Large file detector & categorizer
    │   ├── duplicate_finder.py    # MD5 hash-based duplicate file finder
    │   ├── startup_manager.py     # Windows Registry startup manager
    │   └── settings.py            # Persistent settings, whitelist & lifetime stats
    ├── ui/
    │   ├── app.py                 # Main Application Layout & Controller
    │   ├── components/
    │   │   ├── sidebar.py         # Left Navigation Sidebar with C: Drive Meter
    │   │   ├── top_bar.py         # Header, Stat Cards, Live Search & Filters
    │   │   ├── target_card.py     # Interactive Cache Card Component
    │   │   ├── footer.py          # Bottom Action Bar & Progress Indicator
    │   │   ├── log_panel.py       # Live Collapsible Terminal Output
    │   │   ├── project_cleaner_view.py # Project Cleaner Module View
    │   │   ├── disk_analyzer_view.py   # Large Files Visualizer View
    │   │   ├── duplicate_finder_view.py # Duplicate Finder View
    │   │   ├── startup_view.py    # Windows Startup Manager View
    │   │   └── settings_view.py   # Whitelist & Lifetime Stats View
    │   └── dialogs/
    │       └── detail_dialog.py   # Granular Sub-item Inspection & Exclusion Modal
    └── utils/
        ├── formatters.py          # Byte and duration formatting helpers
        └── system_helper.py       # Windows Explorer & OS helper functions
```

---

## 🇹🇷 Türkçe Dokümantasyon

### 🎯 Proje Hakkında
**Cache Cleaner**, geliştiricilerin ve ileri düzey bilgisayar kullanıcılarının disklerinde biriken onlarca GB gereksiz önbellek, paket arşivi, GPU shader kalıntısı ve terk edilmiş proje bağımlılıklarını (`node_modules`, `venv`, `target`) güvenle temizlemek için geliştirilmiş modern ve profesyonel bir masaüstü uygulamasıdır.

### 🌟 Öne Çıkan Özellikler
1. **42+ Önbellek Kaynağı:** Python pip, NPM, Yarn, Docker WSL, PyTorch AI modelleri, Ollama, VS Code, GPU Shaderları, Tarayıcılar ve Sistem geçici dosyaları.
2. **Proje Temizleyici:** Proje dizinlerinizdeki unutulmuş derleme kalıntılarını tek tıkla silme.
3. **Büyük Dosya Analizi:** Diskteki devasa video, arşiv ve sanal diskleri listeleme.
4. **Kopya Dosya Bulucu:** Hash tabanlı mükerrer kopya tespiti.
5. **Açılış Yöneticisi:** Windows başlangıç uygulamalarını denetleme.
6. **Güvenli ve Korumalı:** Kalıcı beyaz liste ve kilitli dosyalarda otomatik atlama mekanizması.
7. **Çift Dil:** Tek tıkla Türkçe / İngilizce anında geçiş.

---

## 🛡️ Safety & Reliability

- **Non-Destructive Deletion:** Locked files or running processes are safely skipped without halting execution.
- **Whitelist Protection:** User-defined critical directories are never touched.
- **Granular Inspection:** Each target can be inspected with sub-item exclusion controls before executing any cleaning operation.

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).
