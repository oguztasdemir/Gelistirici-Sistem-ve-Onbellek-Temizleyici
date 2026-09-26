"""
Cache Cleaner - Çoklu Dil / Uluslararasılaşma (i18n) Modülü
"""

DEFAULT_LANGUAGE = "tr"

CATEGORIES_I18N = {
    "tr": {
        "all": "🌐 Tüm Kaynaklar",
        "dev": "💻 Geliştirici",
        "system": "⚙️ Sistem & Temp",
        "browser": "🌐 Tarayıcı & Medya"
    },
    "en": {
        "all": "🌐 All Sources",
        "dev": "💻 Developer",
        "system": "⚙️ System & Temp",
        "browser": "🌐 Browser & Media"
    }
}

TARGETS_I18N = {
    "tr": {
        "pip": ("Python pip Paket Önbelleği", "Python kütüphaneleri kurulurken indirilen tekerlek (wheel) ve paket önbellekleri."),
        "uv": ("Astral uv Python Paket Önbelleği", "uv hızlı Python paket yöneticisinin diskte tuttuğu tekerlek ve derleme önbellekleri."),
        "npm": ("Node.js npm Paket Önbelleği", "NPM paket kurulumlarında yerel diskte saklanan paket arşivleri."),
        "yarn_pnpm": ("Yarn & pnpm Paket Önbellekleri", "Yarn ve pnpm paket yöneticilerinin indirdiği küresel önbellek verileri."),
        "ai_models": ("PyTorch & HuggingFace Model Önbelleği", "Yapay zeka modellerinin indirildiği yerel ağırlık ve kontrol noktaları."),
        "ollama": ("Ollama Yerel Model Önbelleği", "Ollama tarafından yerel LLM modellerinin indirildiği blob ve model dosyaları."),
        "vscode": ("VS Code & Cursor Editör Önbelleği", "VS Code ve Cursor editörlerinin arayüz ve eklenti çalışma önbellekleri."),
        "gradle_maven": ("Gradle & Maven Derleme Önbellekleri", "Java/Kotlin ve Android derleme paketlerinin yerel önbellekleri."),
        "docker_wsl": ("Docker WSL Sanal Diski (docker_data.vhdx)", "Docker Desktop'ın diskte tuttuğu dinamik sanal disk dosyası."),
        "docker_daemon": ("Docker Atıl İmaj ve Konteyner Temizliği (Daemon)", "Arka planda çalışan Docker Desktop üzerinden atıl imaj ve birimleri temizler."),
        "conda": ("Anaconda / Miniconda Paket Önbelleği", "Conda paket yöneticisinin indirdiği sıkıştırılmış tarball ve önbellekler."),
        "gpu_shaders": ("NVIDIA / DirectX GPU Gölgelendirici (Shader) Önbelleği", "Oyun ve 3D uygulamaların derlediği grafik kartı gölgelendirici önbellekleri."),
        "user_temp": ("Windows Kullanıcı Geçici Dosyaları (Temp)", "Uygulamaların çalışırken oluşturduğu ve arkada unuttuğu geçici dosyalar."),
        "windows_update": ("Windows Update İndirme Artıkları (SoftwareDistribution)", "Tamamlanan Windows güncellemelerinden arta kalan kurulum paketleri."),
        "thumbnails": ("Windows Gezgini Küçük Resim (Thumbnail) Önbelleği", "Dosya Gezgini'nin resim ve videolar için oluşturduğu önizleme veritabanı."),
        "crash_dumps": ("Windows Çökme Dökümleri & Hata Raporları", "Çöken uygulamaların oluşturduğu büyük bellek döküm (.dmp) dosyaları."),
        "dns": ("Windows DNS Çözümleyici Önbelleği", "Windows'un web sitelerini daha hızlı açmak için tuttuğu yerel IP önbelleği."),
        "chrome": ("Google Chrome Tarayıcı Önbelleği", "Google Chrome tarafından saklanan web resimleri, betikleri ve önbellekleri."),
        "edge": ("Microsoft Edge Tarayıcı Önbelleği", "Microsoft Edge tarafından saklanan web sitelerinin önbellek verileri."),
        "brave": ("Brave Browser Önbelleği", "Brave tarayıcısının depoladığı web önbellekleri."),
        "telegram": ("Telegram Medya & Sohbet Önbelleği", "Telegram Masaüstü uygulamasının indirdiği geçici video, ses ve görsel önbellekleri."),
        "discord": ("Discord Medya & İletişim Önbelleği", "Discord uygulamasının tuttuğu sohbet avatarları, sunucu emojileri ve medyalar."),
        "jetbrains": ("JetBrains IDE Önbellekleri (PyCharm, IntelliJ vb.)", "PyCharm, IntelliJ IDEA ve diğer JetBrains IDE'lerinin indeks önbellekleri."),
        "electron_build": ("Electron & Masaüstü Çerçeve Önbelleği", "Electron tabanlı masaüstü uygulamalarının indirdiği ikili çalışma dosyaları."),
        "node_gyp": ("Node-gyp C++ Derleme Başlıkları", "Yerel Node.js C++ eklentilerini derlemek için indirilen başlık arşivleri."),
        "wer_reports": ("Windows Hata Raporlama (WER) Arşivleri", "Windows Hata Raporlama servisinin tuttuğu kilitlenme ve sorun günlükleri."),
        "recycle_bin": ("Windows Geri Dönüşüm Kutusu", "Tüm sürücülerdeki Geri Dönüşüm Kutusu içeriğini kalıcı olarak boşaltır."),
        "steam": ("Steam İstemci & Web Önbelleği", "Steam mağaza tarayıcısı, yerel HTML önbelleği ve oyun shader kalıntıları."),
        "playwright_cypress": ("Playwright & Cypress Test Tarayıcı Önbellekleri", "E2E test araçlarının indirdiği taşınabilir tarayıcı ikilileri ve önbellekleri."),
        "matplotlib": ("Matplotlib & Grafik Font Önbelleği", "Python veri bilimi görselleştirme kütüphanelerinin derlediği yazı tipi önbellekleri."),
        "system_temp": ("Windows Sistem Düzeyi Temp Dosyaları", "Windows arka plan sistem hizmetlerinin oluşturduğu genel geçici dosyalar."),
        "recent_files": ("Windows Son Kullanılan Dosya & Erişim Geçmişi", "Başlat menüsü ve Gezgin'de listelenen son açılan dosya geçmişi."),
        "cryptnet_cache": ("Windows Sertifika & URL Çözümleme Önbelleği", "SSL/TLS sertifika doğrulama ve iptal listelerinin yerel önbelleği."),
        "teams_slack": ("MS Teams, Slack & Zoom İletişim Önbellekleri", "Toplantı ve kurumsal mesajlaşma uygulamalarının medya ve arayüz önbellekleri."),
        "nvidia_installer": ("NVIDIA Sürücü Kurulum Yedekleri", "NVIDIA GeForce Experience ve sürücü güncellemelerinden kalan eski paketler."),
        "windows_cbs_logs": ("Windows CBS & DISM Kurulum Günlükleri", "Windows Update ve bileşen onarım işlemlerinden arta kalan büyük günlükler."),
        "jedi_cache": ("Python Jedi Kod Tamamlama Önbelleği", "VS Code ve Python editörlerinin kod tamamlama indeks önbellekleri."),
        "downloaded_installations": ("İndirilen Kurulum ve Setup Kalıntıları", "Program kurucularının arşivden çıkarıp arkada bıraktığı setup dosyaları."),
        "ea_app_cache": ("EA App & Oyun Başlatıcı Önbelleği", "Electronic Arts istemcisinin yerel web önbelleği ve çökme günlükleri."),
        "epic_games_cache": ("Epic Games Launcher Web & Kayıt Önbelleği", "Epic Games istemcisinin web görselleri, mağaza önbelleği ve kayıt kalıntıları."),
        "games_crash_logs": ("PUBG & FC 26 Oyun Çökme & Shader Günlükleri", "PUBG ve EA FC 26 oyunlarının biriktirdiği kilitlenme dökümleri ve günlükler."),
        "spotify": ("Spotify Şarkı & Medya Önbelleği", "Spotify uygulamasının dinlenen şarkıları ve albüm kapaklarını sakladığı alan.")
    },
    "en": {
        "pip": ("Python pip Package Cache", "Wheels, build caches and tarballs downloaded during Python package installations."),
        "uv": ("Astral uv Package Cache", "Fast Python package manager wheel and build artifact cache."),
        "npm": ("Node.js npm Package Cache", "Local cached tarballs and metadata created during npm installs."),
        "yarn_pnpm": ("Yarn & pnpm Global Cache", "Global download packages and content-addressable store caches."),
        "ai_models": ("PyTorch & HuggingFace Models", "Locally downloaded neural network weights, checkpoints and tokenizers."),
        "ollama": ("Ollama Local LLM Cache", "Locally pulled LLM model blobs and manifests managed by Ollama."),
        "vscode": ("VS Code & Cursor Editor Cache", "Workspace index, extension cache and UI state data."),
        "gradle_maven": ("Gradle & Maven Build Cache", "Java/Kotlin and Android dependency artifacts and local repositories."),
        "docker_wsl": ("Docker WSL Virtual Disk (docker_data.vhdx)", "Dynamic virtual disk file holding Docker containers and images."),
        "docker_daemon": ("Docker Prune Containers & Images", "Removes dangling images, stopped containers and build cache via Docker engine."),
        "conda": ("Anaconda / Miniconda Package Cache", "Downloaded package archives and tarballs stored by conda."),
        "gpu_shaders": ("GPU Shader Cache (DirectX & NVIDIA & AMD)", "Precompiled graphics pipeline shaders generated by games and 3D software."),
        "user_temp": ("Windows User Temporary Files (Temp)", "Temporary runtime scratch files abandoned by applications."),
        "windows_update": ("Windows Update Download Cache", "Leftover installation files from completed Windows update cycles."),
        "thumbnails": ("Windows Thumbnail Cache", "Explorer image and video thumbnail preview cache databases."),
        "crash_dumps": ("Crash Dumps & Error Reports", "Full and mini memory dumps (.dmp) generated by crashing programs."),
        "dns": ("Windows DNS Resolver Cache", "Local DNS cache resolving domain names to IP addresses."),
        "chrome": ("Google Chrome Browser Cache", "Web page images, scripts, network cache and code cache."),
        "edge": ("Microsoft Edge Browser Cache", "Browsing data, cached web assets and script caches."),
        "brave": ("Brave Browser Cache", "Offline web cache and media data saved by Brave."),
        "telegram": ("Telegram Desktop Media Cache", "Cached voice notes, stickers, videos and images."),
        "discord": ("Discord Media & Cache", "Cached guild avatars, custom emojis and shared media files."),
        "jetbrains": ("JetBrains IDE Caches (PyCharm, IDEA)", "Local index databases, logs and compiler caches."),
        "electron_build": ("Electron Runtime Cache", "Cached binaries and frameworks downloaded by Electron applications."),
        "node_gyp": ("Node-gyp C++ Headers", "C++ headers downloaded for compiling native Node.js modules."),
        "wer_reports": ("Windows Error Reporting (WER) Logs", "Diagnostic archives and telemetry logs from software faults."),
        "recycle_bin": ("Windows Recycle Bin", "Permanently empties deleted files across all connected drives."),
        "steam": ("Steam Client & Shader Cache", "Steam web browser cache, download chunks and graphics shaders."),
        "playwright_cypress": ("Playwright & Cypress Browser Binaries", "Test automation browser binaries and download caches."),
        "matplotlib": ("Matplotlib Font Cache", "Prebuilt font list caches compiled by Python visualization packages."),
        "system_temp": ("Windows System Temp Files", "General temp files created by Windows background system services."),
        "recent_files": ("Recent Files & Jump Lists", "Explorer and Start menu recent file shortcuts history."),
        "cryptnet_cache": ("Cryptnet SSL Certificate Cache", "Local cache of SSL certificate revocation lists and certificates."),
        "teams_slack": ("MS Teams, Slack & Zoom Cache", "Communication and meeting cache data and avatars."),
        "nvidia_installer": ("NVIDIA Driver Installer Packages", "Old driver installer packages left in ProgramData/NVIDIA."),
        "windows_cbs_logs": ("Windows CBS & DISM Logs", "Diagnostic and component store logs from Windows update/repair."),
        "jedi_cache": ("Python Jedi Auto-complete Cache", "Autocompletion index databases created by Python IDEs."),
        "downloaded_installations": ("Downloaded Setup Residuals", "Temporary extracted setup files left by program installers."),
        "ea_app_cache": ("EA App Client Cache", "Electronic Arts app cache, crash dumps and store assets."),
        "epic_games_cache": ("Epic Games Launcher Cache", "Epic Games web cache, launcher manifest and saved assets."),
        "games_crash_logs": ("PUBG & FC 26 Game Crash Logs", "Crash dumps and telemetry logs generated by games."),
        "spotify": ("Spotify Music & Media Cache", "Locally cached streaming audio tracks and album art.")
    }
}

TRANSLATIONS = {
    "tr": {
        # Header & Navigation
        "app_title": "Cache Cleaner",
        "app_subtitle": "Geliştirici Sistem & Disk Alanı Kurtarma Aracı",
        "tab_cache": "🧹  Sistem & Önbellek",
        "tab_projects": "💻  Proje Temizleyici",
        "tab_large_files": "🔍  Büyük Dosyalar",
        "tab_duplicates": "👯‍♂️  Kopya Dosya Bulucu",
        "tab_startup": "🚀  Başlangıç Yöneticisi",
        "tab_stats": "⚙️  İstatistik & Ayarlar",

        # Top Bar Titles & Descriptions
        "cache_view_title": "🧹 Sistem & Önbellek Temizleyici",
        "cache_view_desc": "Geliştirici paketleri, GPU shaderları ve sistem artıklarını tespit edin.",
        "project_view_title": "💻 Proje Bağımlılık & Önbellek Temizleyicisi",
        "project_view_desc": "Projelerinizdeki node_modules, venv, target ve derleme artıklarını silin.",
        "large_files_view_title": "🔍 Büyük Dosya ve Disk Alanı Analizcisi",
        "large_files_view_desc": "Diskteki en büyük video, arşiv, sanal disk ve kurulum dosyalarını bulun.",
        "duplicate_view_title": "👯‍♂️ Kopya Dosya Bulucu (Duplicate Finder)",
        "duplicate_view_desc": "Diskteki birebir aynı kopya dosyaları hash karşılaştırmasıyla bulun.",
        "startup_view_title": "🚀 Windows Başlangıç Programları Yöneticisi",
        "startup_view_desc": "Açılışta otomatik başlayan uygulamaları denetleyin ve açılışı hızlandırın.",
        "settings_view_title": "⚙️ Yaşam Boyu İstatistikler & Ayarlar",
        "settings_view_desc": "Kurtarılan toplam alan istatistikleri ve kalıcı beyaz liste koruması.",

        # Stat Cards
        "stat_card_total_detected": "Bulunan Alan",
        "stat_card_selected_clean": "Seçilen Temizlenecek",
        "stat_card_safety_title": "Güvenlik Seviyesi",
        "stat_card_safety_val": "%100 Güvenli",
        "search_placeholder": "🔍 Ara / Filtrele...",

        # Buttons
        "btn_rescan": "🔄 Yeniden Tara",
        "btn_clean_selected": "✨ Seçilenleri Güvenle Temizle",
        "btn_clean_with_size": "✨ Seçilenleri Güvenle Temizle ({size})",
        "btn_detail": "🔍 İncele",
        "btn_detail_count": "🔍 Detay ({count})",
        "btn_explorer": "📂",
        "btn_select_all": "✓ Tümünü Seç",
        "btn_deselect_all": "✕ Seçimi Kaldır",
        "btn_toggle_logs": "📜 İşlem Günlüğünü Aç / Kapat",
        "btn_copy": "📋 Kopyala",
        "btn_clear": "🗑️ Temizle",
        "btn_browse": "📁 Klasör Seç",
        "btn_scan_projects": "🔍 Projeleri Tara",
        "btn_clean_projects": "🧹 Seçili Proje Artıklarını Sil",
        "btn_scan_large_files": "🔍 Büyük Dosyaları Tara",
        "btn_delete_large_files": "🗑️ Seçilen Dosyaları Sil",
        "btn_scan_duplicates": "🔍 Kopyaları Tara",
        "btn_auto_select_dupes": "✨ Fazla Kopyaları Otomatik Seç",
        "btn_delete_duplicates": "🗑️ Seçili Kopyaları Sil",
        "btn_refresh_startup": "🔄 Listeyi Yenile",
        "btn_save": "💾 Kaydet",
        "btn_reset_stats": "🔄 İstatistikleri Sıfırla",
        "btn_add_whitelist": "➕ Listeye Ekle",
        "btn_remove_whitelist": "🗑️ Seçileni Kaldır",

        # Badges
        "badge_safe": "🛡️ Güvenli",
        "badge_warning": "⚠️ İncele",
        "badge_not_found": "Bulunamadı",
        "badge_empty": "0 B",

        # Logs & Status
        "status_ready": "Hazır",
        "status_scanning": "Önbellek ve geçici dosyalar taranıyor...",
        "status_scanning_item": "Taranıyor ({current}/{total}): {name}...",
        "status_scan_done": "Tarama tamamlandı",
        "status_cleaning": "Temizleme işlemi başlatıldı...",
        "status_cleaning_item": "Temizleniyor ({current}/{total}): {name}...",
        "status_clean_done": "Temizlik başarıyla tamamlandı.",
        "log_scan_started": "🔍 Sistem ve önbellek taraması başlatıldı...",
        "log_scan_completed": "✅ Tarama başarıyla tamamlandı. Toplam {size} önbellek tespit edildi.",
        "log_clean_completed": "🎉 Temizlik tamamlandı! {size} net alan geri kazanıldı.",

        # Project Cleaner View
        "project_cleaner_title": "💻 Proje Önbellek ve Bağımlılık Temizleyicisi",
        "project_cleaner_desc": "Projelerinizdeki unutulmuş 'node_modules', 'venv', 'target' ve derleme artıklarını bularak onlarca GB yer açın.",
        "select_project_dir": "Taranacak Ana Proje Dizini:",
        "project_item_count": "Toplam {count} proje kalıntısı bulundu ({size})",
        "confirm_project_clean": "Seçilen {count} adet proje bağımlılık klasörü (node_modules, venv vb.) silinecektir.\n\nToplam Kurtarılacak Alan: {size}\n\nDevam etmek istiyor musunuz?",

        # Large Files View
        "large_files_title": "🔍 Büyük Dosya ve Disk Alanı Analizcisi",
        "large_files_desc": "Diskinizde gizlenen devasa video, arşiv (.zip, .iso), sanal disk ve yedek dosyalarını tespit edin.",
        "min_file_size": "Minimum Dosya Boyutu:",
        "large_files_found": "Toplam {count} büyük dosya tespit edildi ({size})",
        "col_filename": "Dosya Adı",
        "col_path": "Dosya Yolu",
        "col_size": "Boyut",
        "confirm_large_file_delete": "DİKKAT: Seçilen {count} adet büyük dosya kalıcı olarak silinecektir.\n\nToplam Silinecek: {size}\n\nBu işlem geri alınamaz. Onaylıyor musunuz?",

        # Duplicate Finder View
        "duplicate_title": "👯‍♂️ Kopya Dosya Bulucu",
        "duplicate_desc": "MD5 hash karşılaştırmasıyla diskteki birebir aynı kopya dosyaları bulun.",
        "duplicate_summary": "{groups} grupta {files} dosya tespit edildi. İsraf Edilen: {size}",

        # Startup View
        "startup_title": "🚀 Windows Başlangıç Programları",
        "startup_desc": "Windows açılışında otomatik çalışan uygulamaları devre dışı bırakın.",
        "startup_app_count": "Toplam {count} başlangıç uygulaması listelendi",

        # Stats & Settings View
        "stats_title": "📈 Yaşam Boyu Temizlik İstatistikleri",
        "stat_lifetime_freed": "Şu Ana Kadar Kurtarılan Toplam Alan:",
        "stat_sessions_count": "Toplam Temizlik Seansı:",
        "stat_last_cleaned": "Son Temizlik Tarihi:",
        "whitelist_title": "🛡️ Kalıcı Koruma / Beyaz Liste (Whitelist)",
        "whitelist_desc": "Buraya eklediğiniz dosya ve klasör yolları tarama veya temizliklerde asla silinmez.",
        "whitelist_placeholder": "Korunacak tam dosya veya klasör yolu girin...",
        "language_setting": "🌍 Uygulama Dili / Language:",

        # Dialogs
        "dialog_confirm_title": "Temizleme Onayı",
        "dialog_success_title": "Temizlik Başarılı",
        "dialog_warning_title": "Uyarı"
    },
    "en": {
        # Header & Navigation
        "app_title": "Cache Cleaner",
        "app_subtitle": "Developer System & Disk Space Recovery Tool",
        "tab_cache": "🧹  System & Cache",
        "tab_projects": "💻  Project Cleaner",
        "tab_large_files": "🔍  Large Files",
        "tab_duplicates": "👯‍♂️  Duplicate Finder",
        "tab_startup": "🚀  Startup Manager",
        "tab_stats": "⚙️  Stats & Settings",

        # Top Bar Titles & Descriptions
        "cache_view_title": "🧹 System & Cache Cleaner",
        "cache_view_desc": "Clean developer build caches, GPU shaders, and system junk safely.",
        "project_view_title": "💻 Project Dependency & Cache Cleaner",
        "project_view_desc": "Scan and remove abandoned node_modules, venv, target and build leftovers.",
        "large_files_view_title": "🔍 Large File & Disk Visualizer",
        "large_files_view_desc": "Discover large videos, disk images (.vhdx), archives, and installers.",
        "duplicate_view_title": "👯‍♂️ Duplicate File Finder",
        "duplicate_view_desc": "Find exact duplicate files across your storage using fast MD5 hashing.",
        "startup_view_title": "🚀 Windows Startup Application Manager",
        "startup_view_desc": "Inspect and manage apps starting automatically on Windows boot.",
        "settings_view_title": "⚙️ Lifetime Statistics & Preferences",
        "settings_view_desc": "Lifetime recovered disk space statistics and permanent whitelist protection.",

        # Stat Cards
        "stat_card_total_detected": "Total Found",
        "stat_card_selected_clean": "Selected to Clean",
        "stat_card_safety_title": "Protection Level",
        "stat_card_safety_val": "100% Safe",
        "search_placeholder": "🔍 Search / Filter...",

        # Buttons
        "btn_rescan": "🔄 Rescan",
        "btn_clean_selected": "✨ Clean Selected Safely",
        "btn_clean_with_size": "✨ Clean Selected Safely ({size})",
        "btn_detail": "🔍 Inspect",
        "btn_detail_count": "🔍 Detail ({count})",
        "btn_explorer": "📂",
        "btn_select_all": "✓ Select All",
        "btn_deselect_all": "✕ Deselect All",
        "btn_toggle_logs": "📜 Show / Hide Live Terminal Log",
        "btn_copy": "📋 Copy",
        "btn_clear": "🗑️ Clear",
        "btn_browse": "📁 Browse Folder",
        "btn_scan_projects": "🔍 Scan Projects",
        "btn_clean_projects": "🧹 Delete Selected Project Junk",
        "btn_scan_large_files": "🔍 Scan Large Files",
        "btn_delete_large_files": "🗑️ Delete Selected Files",
        "btn_scan_duplicates": "🔍 Scan Duplicates",
        "btn_auto_select_dupes": "✨ Auto-select Extra Copies",
        "btn_delete_duplicates": "🗑️ Delete Selected Duplicates",
        "btn_refresh_startup": "🔄 Refresh List",
        "btn_save": "💾 Save",
        "btn_reset_stats": "🔄 Reset Stats",
        "btn_add_whitelist": "➕ Add to Whitelist",
        "btn_remove_whitelist": "🗑️ Remove Selected",

        # Badges
        "badge_safe": "🛡️ Safe",
        "badge_warning": "⚠️ Review",
        "badge_not_found": "Not Found",
        "badge_empty": "0 B",

        # Logs & Status
        "status_ready": "Ready",
        "status_scanning": "Scanning cache and temporary files...",
        "status_scanning_item": "Scanning ({current}/{total}): {name}...",
        "status_scan_done": "Scan completed",
        "status_cleaning": "Cleaning process started...",
        "status_cleaning_item": "Cleaning ({current}/{total}): {name}...",
        "status_clean_done": "Cleaning completed successfully.",
        "log_scan_started": "🔍 System and cache scan started...",
        "log_scan_completed": "✅ Scan completed successfully. Total {size} cache detected.",
        "log_clean_completed": "🎉 Cleaning completed! {size} space recovered.",

        # Project Cleaner View
        "project_cleaner_title": "💻 Project Cache & Dependency Cleaner",
        "project_cleaner_desc": "Scan and remove abandoned 'node_modules', 'venv', 'target' and build leftovers across all your projects.",
        "select_project_dir": "Root Projects Directory:",
        "project_item_count": "Found {count} project junk items ({size})",
        "confirm_project_clean": "Selected {count} project dependency folders will be deleted.\n\nTotal Recovered Space: {size}\n\nDo you want to proceed?",

        # Large Files View
        "large_files_title": "🔍 Large File & Disk Visualizer",
        "large_files_desc": "Discover huge video, archive (.zip, .iso), virtual disk and backup files hiding on your drive.",
        "min_file_size": "Minimum File Size:",
        "large_files_found": "Total {count} large files found ({size})",
        "col_filename": "File Name",
        "col_path": "Path",
        "col_size": "Size",
        "confirm_large_file_delete": "CAUTION: Selected {count} large files will be permanently deleted.\n\nTotal Size: {size}\n\nThis cannot be undone. Are you sure?",

        # Duplicate Finder View
        "duplicate_title": "👯‍♂️ Duplicate File Finder",
        "duplicate_desc": "Find exact duplicate files on your disk using fast MD5 hashing.",
        "duplicate_summary": "Found {files} files in {groups} groups. Wasted Space: {size}",

        # Startup View
        "startup_title": "🚀 Windows Startup Applications",
        "startup_desc": "Disable unnecessary startup applications to speed up Windows boot time.",
        "startup_app_count": "Total {count} startup applications listed",

        # Stats & Settings View
        "stats_title": "📈 Lifetime Clean Stats & Settings",
        "stat_lifetime_freed": "Total Space Recovered to Date:",
        "stat_sessions_count": "Total Cleaning Sessions:",
        "stat_last_cleaned": "Last Cleaned Date:",
        "whitelist_title": "🛡️ Permanent Whitelist & Protection",
        "whitelist_desc": "Paths added here will never be touched or deleted during scans/cleaning.",
        "whitelist_placeholder": "Enter full file or directory path to protect...",
        "language_setting": "🌍 Application Language:",

        # Dialogs
        "dialog_confirm_title": "Cleaning Confirmation",
        "dialog_success_title": "Cleaning Successful",
        "dialog_warning_title": "Warning"
    }
}

class I18nManager:
    """Uygulama genelinde çoklu dil yöneticisi."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(I18nManager, cls).__new__(cls)
            cls._instance.current_lang = DEFAULT_LANGUAGE
        return cls._instance

    def set_language(self, lang_code: str):
        if lang_code in ("tr", "en"):
            self.current_lang = lang_code

    def get_language(self) -> str:
        return self.current_lang

    def t(self, key: str, **kwargs) -> str:
        lang_dict = TRANSLATIONS.get(self.current_lang, TRANSLATIONS["tr"])
        text = lang_dict.get(key, TRANSLATIONS["tr"].get(key, key))
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

    def get_category_name(self, cat_key: str) -> str:
        cat_dict = CATEGORIES_I18N.get(self.current_lang, CATEGORIES_I18N["tr"])
        return cat_dict.get(cat_key, cat_key)

    def get_target_name_and_desc(self, key: str) -> tuple[str, str]:
        t_dict = TARGETS_I18N.get(self.current_lang, TARGETS_I18N["tr"])
        return t_dict.get(key, (key, ""))

# Global singleton helper
_i18n = I18nManager()

def t(key: str, **kwargs) -> str:
    return _i18n.t(key, **kwargs)

def set_language(lang: str):
    _i18n.set_language(lang)

def get_language() -> str:
    return _i18n.get_language()

def get_category_name(cat_key: str) -> str:
    return _i18n.get_category_name(cat_key)

def get_target_info_i18n(key: str) -> tuple[str, str]:
    return _i18n.get_target_name_and_desc(key)
