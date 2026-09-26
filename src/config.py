import os
from src.utils.system_helper import get_user_home

APP_TITLE = "Cache Cleaner - Geliştirici Sistem & Önbellek Temizleyici"
APP_SUBTITLE = "Geliştirici araçları, sistem artıkları ve tarayıcı önbelleklerini güvenle temizleyip disk alanınızı geri kazanın."
APP_VERSION = "2.1.0"

# UI Theme Config & Modern Design Tokens
DEFAULT_APPEARANCE = "Dark"
COLOR_BG_DARK = "#090d16"          # Ultra-deep obsidian background
COLOR_SIDEBAR_BG = "#0d121d"       # Elevated left panel
COLOR_SIDEBAR_BORDER = "#192233"   # Subtle panel border
COLOR_CARD_BG = "#121824"          # Sleek card surface
COLOR_CARD_HOVER = "#172030"       # Card hover surface
COLOR_CARD_BORDER = "#1e293b"      # Card border
COLOR_CARD_BORDER_ACTIVE = "#334155"

COLOR_PRIMARY = "#10b981"          # Emerald Green Accent
COLOR_PRIMARY_HOVER = "#059669"
COLOR_PRIMARY_LIGHT = "#10b98120"
COLOR_ACCENT = "#38bdf8"           # Sky Blue Accent
COLOR_ACCENT_HOVER = "#0284c7"
COLOR_PURPLE = "#818cf8"           # Indigo/Violet

COLOR_TEXT_MAIN = "#f1f5f9"         # Slate 100 High Contrast
COLOR_TEXT_MUTED = "#94a3b8"        # Slate 400 Secondary
COLOR_TEXT_DIM = "#64748b"          # Slate 500 Tertiary
COLOR_DANGER = "#f43f5e"            # Rose Red
COLOR_WARNING = "#fbbf24"           # Amber
COLOR_SUCCESS = "#10b981"

user_home = get_user_home()

CATEGORIES = {
    "all": "🌐 Tüm Kaynaklar",
    "dev": "💻 Geliştirici Araçları",
    "system": "⚙️ Sistem & Temp",
    "browser": "🌐 Tarayıcı & Medya"
}

TARGETS = {
    # ----------------------------------------------------
    # Geliştirici Araçları (Developer Tools)
    # ----------------------------------------------------
    "pip": {
        "name": "Python pip Paket Önbelleği",
        "category": "dev",
        "icon": "🐍",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "pip"),
            os.path.join(user_home, ".cache", "pip")
        ],
        "type": "folders",
        "desc": "Python kütüphaneleri kurulurken indirilen tekerlek (wheel) ve paket önbellekleri.",
        "danger_level": "safe"
    },
    "uv": {
        "name": "Astral uv Python Paket Önbelleği",
        "category": "dev",
        "icon": "⚡",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "uv", "cache")
        ],
        "type": "folders",
        "desc": "uv hızlı Python paket yöneticisinin diskte tuttuğu tekerlek ve derleme önbellekleri.",
        "danger_level": "safe"
    },
    "npm": {
        "name": "Node.js npm Paket Önbelleği",
        "category": "dev",
        "icon": "📦",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "npm-cache"),
            os.path.join(user_home, ".npm")
        ],
        "type": "folders",
        "desc": "NPM paket kurulumlarında yerel diskte saklanan paket arşivleri.",
        "danger_level": "safe"
    },
    "yarn_pnpm": {
        "name": "Yarn & pnpm Paket Önbellekleri",
        "category": "dev",
        "icon": "🧶",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "Yarn", "Cache"),
            os.path.join(user_home, "AppData", "Local", "pnpm", "store")
        ],
        "type": "folders",
        "desc": "Yarn ve pnpm paket yöneticilerinin indirdiği küresel önbellek verileri.",
        "danger_level": "safe"
    },
    "ai_models": {
        "name": "PyTorch & HuggingFace Model Önbelleği",
        "category": "dev",
        "icon": "🤖",
        "paths": [
            os.path.join(user_home, ".cache", "torch", "hub", "checkpoints"),
            os.path.join(user_home, ".cache", "huggingface", "hub")
        ],
        "type": "folders",
        "desc": "Yapay zeka modellerinin indirildiği yerel ağırlık ve kontrol noktaları.",
        "danger_level": "safe"
    },
    "ollama": {
        "name": "Ollama Yerel Model Önbelleği",
        "category": "dev",
        "icon": "🦙",
        "paths": [
            os.path.join(user_home, ".ollama", "models")
        ],
        "type": "folders",
        "desc": "Ollama tarafından yerel LLM modellerinin indirildiği blob ve model dosyaları.",
        "danger_level": "safe"
    },
    "vscode": {
        "name": "VS Code & Cursor Editör Önbelleği",
        "category": "dev",
        "icon": "📝",
        "paths": [
            os.path.join(user_home, "AppData", "Roaming", "Code", "Cache"),
            os.path.join(user_home, "AppData", "Roaming", "Code", "CachedData"),
            os.path.join(user_home, "AppData", "Roaming", "Code", "logs"),
            os.path.join(user_home, "AppData", "Roaming", "Cursor", "Cache"),
            os.path.join(user_home, "AppData", "Roaming", "Cursor", "CachedData")
        ],
        "type": "folders",
        "desc": "VS Code ve Cursor editörlerinin arayüz ve eklenti çalışma önbellekleri.",
        "danger_level": "safe"
    },
    "gradle_maven": {
        "name": "Gradle & Maven Derleme Önbellekleri",
        "category": "dev",
        "icon": "☕",
        "paths": [
            os.path.join(user_home, ".gradle", "caches"),
            os.path.join(user_home, ".m2", "repository")
        ],
        "type": "folders",
        "desc": "Java/Kotlin ve Android derleme paketlerinin yerel önbellekleri.",
        "danger_level": "safe"
    },
    "docker_wsl": {
        "name": "Docker WSL Sanal Diski (docker_data.vhdx)",
        "category": "dev",
        "icon": "🐳",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "Docker", "wsl")
        ],
        "type": "folders",
        "desc": "Docker Desktop'ın diskte tuttuğu dinamik sanal disk dosyası. Detay butonundan incelenebilir.",
        "danger_level": "safe"
    },
    "docker_daemon": {
        "name": "Docker Atıl İmaj ve Konteyner Temizliği (Daemon)",
        "category": "dev",
        "icon": "🐳",
        "paths": [],
        "type": "docker_cmd",
        "desc": "Arka planda çalışan Docker Desktop üzerinden atıl imaj ve birimleri temizler (Docker açık olmalıdır).",
        "danger_level": "safe"
    },
    "conda": {
        "name": "Anaconda / Miniconda Paket Önbelleği",
        "category": "dev",
        "icon": "🧪",
        "paths": [],
        "type": "conda_cmd",
        "desc": "Conda paket yöneticisinin indirdiği sıkıştırılmış tarball ve önbellekler.",
        "danger_level": "safe"
    },

    # ----------------------------------------------------
    # Sistem ve Donanım Geçici Dosyaları (System & GPU)
    # ----------------------------------------------------
    "gpu_shaders": {
        "name": "NVIDIA / DirectX GPU Gölgelendirici (Shader) Önbelleği",
        "category": "system",
        "icon": "🎮",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "NVIDIA", "DXCache"),
            os.path.join(user_home, "AppData", "Local", "NVIDIA", "GLCache"),
            os.path.join(user_home, "AppData", "Local", "D3DSCache"),
            os.path.join(user_home, "AppData", "Local", "AMD", "DxCache"),
            os.path.join(user_home, "AppData", "Local", "DirectXShaderCache")
        ],
        "type": "folders",
        "desc": "Oyun ve 3D uygulamaların derlediği, güvenle sıfırlanabilen devasa grafik kartı gölgelendirici önbellekleri.",
        "danger_level": "safe"
    },
    "user_temp": {
        "name": "Windows Kullanıcı Geçici Dosyaları (Temp)",
        "category": "system",
        "icon": "🗑️",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "Temp")
        ],
        "type": "temp_files",
        "desc": "Uygulamaların çalışırken oluşturduğu ve arkada unuttuğu geçici dosyalar.",
        "danger_level": "safe"
    },
    "windows_update": {
        "name": "Windows Update İndirme Artıkları (SoftwareDistribution)",
        "category": "system",
        "icon": "🔄",
        "paths": [
            "C:\\Windows\\SoftwareDistribution\\Download"
        ],
        "type": "temp_files",
        "desc": "Tamamlanan Windows güncellemelerinden arta kalan kurulum paketleri.",
        "danger_level": "safe"
    },
    "thumbnails": {
        "name": "Windows Gezgini Küçük Resim (Thumbnail) Önbelleği",
        "category": "system",
        "icon": "🖼️",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "Microsoft", "Windows", "Explorer")
        ],
        "type": "folders",
        "desc": "Dosya Gezgini'nin resim ve videolar için oluşturduğu önizleme veritabanı dosyaları.",
        "danger_level": "safe"
    },
    "crash_dumps": {
        "name": "Windows Çökme Dökümleri & Hata Raporları",
        "category": "system",
        "icon": "💥",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "CrashDumps")
        ],
        "type": "temp_files",
        "desc": "Çöken uygulamaların oluşturduğu büyük bellek döküm (.dmp) dosyaları.",
        "danger_level": "safe"
    },
    "dns": {
        "name": "Windows DNS Çözümleyici Önbelleği",
        "category": "system",
        "icon": "🌐",
        "paths": [],
        "type": "dns_cmd",
        "desc": "Windows'un web site adreslerini daha hızlı çözümlemek için tuttuğu yerel IP önbelleği.",
        "danger_level": "safe"
    },

    # ----------------------------------------------------
    # Tarayıcı & Medya & İletişim (Browser & Media & Chat)
    # ----------------------------------------------------
    "chrome": {
        "name": "Google Chrome Tarayıcı Önbelleği",
        "category": "browser",
        "icon": "🌐",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cache"),
            os.path.join(user_home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Code Cache")
        ],
        "type": "folders",
        "desc": "Google Chrome tarafından saklanan web resimleri, betikleri ve önbellekleri.",
        "danger_level": "safe"
    },
    "edge": {
        "name": "Microsoft Edge Tarayıcı Önbelleği",
        "category": "browser",
        "icon": "🌐",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Cache"),
            os.path.join(user_home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Code Cache")
        ],
        "type": "folders",
        "desc": "Microsoft Edge tarafından saklanan web sitelerinin önbellek verileri.",
        "danger_level": "safe"
    },
    "brave": {
        "name": "Brave Browser Önbelleği",
        "category": "browser",
        "icon": "🦁",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Cache"),
            os.path.join(user_home, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Code Cache")
        ],
        "type": "folders",
        "desc": "Brave tarayıcısının depoladığı web önbellekleri.",
        "danger_level": "safe"
    },
    "telegram": {
        "name": "Telegram Medya & Sohbet Önbelleği",
        "category": "browser",
        "icon": "✈️",
        "paths": [
            os.path.join(user_home, "AppData", "Roaming", "Telegram Desktop", "tdata", "user_data")
        ],
        "type": "folders",
        "desc": "Telegram Masaüstü uygulamasının indirdiği geçici video, ses ve görsel önbellekleri.",
        "danger_level": "safe"
    },
    "discord": {
        "name": "Discord Medya & İletişim Önbelleği",
        "category": "browser",
        "icon": "💬",
        "paths": [
            os.path.join(user_home, "AppData", "Roaming", "discord", "Cache"),
            os.path.join(user_home, "AppData", "Roaming", "discord", "Code Cache")
        ],
        "type": "folders",
        "desc": "Discord uygulamasının tuttuğu sohbet avatarları, sunucu emojileri ve medya dosyaları.",
        "danger_level": "safe"
    },
    "jetbrains": {
        "name": "JetBrains IDE Önbellekleri (PyCharm, IntelliJ vb.)",
        "category": "dev",
        "icon": "🧠",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "JetBrains")
        ],
        "type": "folders",
        "desc": "PyCharm, IntelliJ IDEA ve diğer JetBrains IDE'lerinin indeks ve derleme önbellekleri.",
        "danger_level": "safe"
    },
    "electron_build": {
        "name": "Electron & Masaüstü Çerçeve Önbelleği",
        "category": "dev",
        "icon": "⚛️",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "electron", "Cache")
        ],
        "type": "folders",
        "desc": "Electron tabanlı masaüstü uygulamalarının indirdiği ikili çalışma dosyaları.",
        "danger_level": "safe"
    },
    "node_gyp": {
        "name": "Node-gyp C++ Derleme Başlıkları",
        "category": "dev",
        "icon": "⚙️",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "node-gyp", "Cache")
        ],
        "type": "folders",
        "desc": "Yerel Node.js C++ eklentilerini derlemek için indirilen başlık arşivleri.",
        "danger_level": "safe"
    },
    "wer_reports": {
        "name": "Windows Hata Raporlama (WER) Arşivleri",
        "category": "system",
        "icon": "📋",
        "paths": [
            "C:\\ProgramData\\Microsoft\\Windows\\WER"
        ],
        "type": "folders",
        "desc": "Windows Hata Raporlama servisinin tuttuğu kilitlenme ve sorun günlükleri.",
        "danger_level": "safe"
    },
    "recycle_bin": {
        "name": "Windows Geri Dönüşüm Kutusu",
        "category": "system",
        "icon": "🗑️",
        "paths": [],
        "type": "recycle_bin_cmd",
        "desc": "Tüm sürücülerdeki Geri Dönüşüm Kutusu içeriğini kalıcı olarak boşaltır.",
        "danger_level": "safe"
    },
    "steam": {
        "name": "Steam İstemci & Web Önbelleği",
        "category": "browser",
        "icon": "🎮",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "Steam", "htmlcache"),
            "C:\\Program Files (x86)\\Steam\\steamapps\\shadercache"
        ],
        "type": "folders",
        "desc": "Steam mağaza tarayıcısı, yerel HTML önbelleği ve oyun shader kalıntıları.",
        "danger_level": "safe"
    },
    "playwright_cypress": {
        "name": "Playwright & Cypress Test Tarayıcı Önbellekleri",
        "category": "dev",
        "icon": "🎭",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "ms-playwright"),
            os.path.join(user_home, "AppData", "Local", "Cypress", "Cache")
        ],
        "type": "folders",
        "desc": "Uçtan uca (E2E) test araçlarının indirdiği taşınabilir tarayıcı ikilileri ve önbellekleri.",
        "danger_level": "safe"
    },
    "matplotlib": {
        "name": "Matplotlib & Grafik Font Önbelleği",
        "category": "dev",
        "icon": "📊",
        "paths": [
            os.path.join(user_home, ".matplotlib")
        ],
        "type": "folders",
        "desc": "Python veri bilimi görselleştirme kütüphanelerinin derlediği yazı tipi önbellekleri.",
        "danger_level": "safe"
    },
    "system_temp": {
        "name": "Windows Sistem Düzeyi Temp Dosyaları",
        "category": "system",
        "icon": "🗄️",
        "paths": [
            "C:\\Windows\\Temp"
        ],
        "type": "temp_files",
        "desc": "Windows arka plan sistem hizmetlerinin oluşturduğu genel geçici dosyalar.",
        "danger_level": "safe"
    },
    "recent_files": {
        "name": "Windows Son Kullanılan Dosya & Erişim Geçmişi",
        "category": "system",
        "icon": "🕒",
        "paths": [
            os.path.join(user_home, "AppData", "Roaming", "Microsoft", "Windows", "Recent")
        ],
        "type": "temp_files",
        "desc": "Başlat menüsü ve Gezgin'de listelenen son açılan dosya ve klasör kısayol geçmişi.",
        "danger_level": "safe"
    },
    "cryptnet_cache": {
        "name": "Windows Sertifika & URL Çözümleme Önbelleği",
        "category": "system",
        "icon": "🔒",
        "paths": [
            os.path.join(user_home, "AppData", "LocalLow", "Microsoft", "CryptnetUrlCache")
        ],
        "type": "folders",
        "desc": "SSL/TLS sertifika doğrulama ve iptal listelerinin yerel önbelleği.",
        "danger_level": "safe"
    },
    "teams_slack": {
        "name": "MS Teams, Slack & Zoom İletişim Önbellekleri",
        "category": "browser",
        "icon": "👥",
        "paths": [
            os.path.join(user_home, "AppData", "Roaming", "Slack", "Cache"),
            os.path.join(user_home, "AppData", "Roaming", "Zoom", "data")
        ],
        "type": "folders",
        "desc": "Toplantı ve kurumsal mesajlaşma uygulamalarının medya ve arayüz önbellekleri.",
        "danger_level": "safe"
    },
    "nvidia_installer": {
        "name": "NVIDIA Sürücü Kurulum Yedekleri",
        "category": "system",
        "icon": "📦",
        "paths": [
            "C:\\ProgramData\\NVIDIA Corporation\\Downloader",
            "C:\\Program Files\\NVIDIA Corporation\\Installer2"
        ],
        "type": "folders",
        "desc": "NVIDIA GeForce Experience ve sürücü güncellemelerinin diskte unuttuğu eski kurulum paketleri.",
        "danger_level": "safe"
    },
    "windows_cbs_logs": {
        "name": "Windows CBS & DISM Kurulum Günlükleri",
        "category": "system",
        "icon": "📝",
        "paths": [
            "C:\\Windows\\Logs\\CBS",
            "C:\\Windows\\Logs\\DISM"
        ],
        "type": "temp_files",
        "desc": "Windows Update ve bileşen onarım işlemlerinden arta kalan büyük .log günlük dosyaları.",
        "danger_level": "safe"
    },
    "jedi_cache": {
        "name": "Python Jedi Kod Tamamlama Önbelleği",
        "category": "dev",
        "icon": "🐍",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "Jedi")
        ],
        "type": "folders",
        "desc": "VS Code ve Python editörlerinin otomatik kod tamamlama için derlediği indeks önbellekleri.",
        "danger_level": "safe"
    },
    "downloaded_installations": {
        "name": "İndirilen Kurulum ve Setup Kalıntıları",
        "category": "system",
        "icon": "💿",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "Downloaded Installations")
        ],
        "type": "folders",
        "desc": "Program kurucularının arşivden çıkarıp kurulum sonrasında arkada bıraktığı setup dosyaları.",
        "danger_level": "safe"
    },
    "ea_app_cache": {
        "name": "EA App & Oyun Başlatıcı Önbelleği",
        "category": "browser",
        "icon": "🎮",
        "paths": [
            os.path.join(user_home, "AppData", "Roaming", "EA")
        ],
        "type": "folders",
        "desc": "Electronic Arts (EA App) istemcisinin yerel web önbelleği ve çökme günlükleri.",
        "danger_level": "safe"
    },
    "epic_games_cache": {
        "name": "Epic Games Launcher Web & Kayıt Önbelleği",
        "category": "browser",
        "icon": "🕹️",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "EpicGamesLauncher", "Saved")
        ],
        "type": "folders",
        "desc": "Epic Games istemcisinin web görselleri, mağaza önbelleği ve kayıt kalıntıları.",
        "danger_level": "safe"
    },
    "games_crash_logs": {
        "name": "PUBG & FC 26 Oyun Çökme & Shader Günlükleri",
        "category": "system",
        "icon": "🎯",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "TslGame", "Saved"),
            os.path.join(user_home, "AppData", "Local", "EA SPORTS FC 26")
        ],
        "type": "folders",
        "desc": "PUBG ve EA FC 26 oyunlarının biriktirdiği kilitlenme dökümleri ve geçici günlükler.",
        "danger_level": "safe"
    },
    "spotify": {
        "name": "Spotify Şarkı & Medya Önbelleği",
        "category": "browser",
        "icon": "🎵",
        "paths": [
            os.path.join(user_home, "AppData", "Local", "Spotify", "Storage"),
            os.path.join(user_home, "AppData", "Local", "Spotify", "Data")
        ],
        "type": "folders",
        "desc": "Spotify uygulamasının dinlenen şarkıları ve albüm kapaklarını sakladığı yerel alan.",
        "danger_level": "safe"
    }
}
