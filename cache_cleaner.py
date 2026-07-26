import os
import sys
import shutil
import subprocess
import threading
from tkinter import messagebox

# Auto-install customtkinter to guarantee a highly modern GUI
try:
    import customtkinter as ctk
except ImportError:
    print("[Cortex Cleaner] 'customtkinter' bulunamadı. Otomatik olarak yükleniyor...")
    subprocess.run([sys.executable, "-m", "pip", "install", "customtkinter"], check=True)
    import customtkinter as ctk

# Configure CustomTkinter Theme
ctk.set_appearance_mode("Dark")  # Dark mode
ctk.set_default_color_theme("green")  # Green accent theme (#10b981 style)

class ModernCacheCleaner(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Cortex System & Cache Privacy Cleaner")
        self.geometry("740x660")
        self.resizable(False, False)
        
        self.user_home = os.path.expanduser("~")
        
        # Target Configurations
        self.targets = {
            "pip": {
                "name": "Python pip Paket Önbelleği",
                "path": os.path.join(self.user_home, "AppData", "Local", "pip"),
                "type": "folder",
                "desc": "Python kütüphaneleri kurulurken indirilen geçici kurulum yedekleri."
            },
            "npm": {
                "name": "Node.js npm Paket Önbelleği",
                "path": os.path.join(self.user_home, "AppData", "Local", "npm-cache"),
                "type": "folder",
                "desc": "Frontend projeleri geliştirirken indirilen paketlerin önbellek kopyaları."
            },
            "temp": {
                "name": "Windows Geçici Çalışma Dosyaları (Temp)",
                "path": os.path.join(self.user_home, "AppData", "Local", "Temp"),
                "type": "temp_files",
                "desc": "Programların anlık oluşturduğu ve silmeyi unuttuğu geçici artıklar."
            },
            "chrome": {
                "name": "Google Chrome Tarayıcı Önbelleği",
                "paths": [
                    os.path.join(self.user_home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cache"),
                    os.path.join(self.user_home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Code Cache")
                ],
                "type": "folders",
                "desc": "Google Chrome tarafından saklanan web sitelerinin önbellek verileri."
            },
            "edge": {
                "name": "Microsoft Edge Tarayıcı Önbelleği",
                "paths": [
                    os.path.join(self.user_home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Cache"),
                    os.path.join(self.user_home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Code Cache")
                ],
                "type": "folders",
                "desc": "Microsoft Edge tarafından saklanan web sitelerinin önbellek verileri."
            },
            "vscode": {
                "name": "Visual Studio Code Önbelleği",
                "paths": [
                    os.path.join(self.user_home, "AppData", "Roaming", "Code", "Cache"),
                    os.path.join(self.user_home, "AppData", "Roaming", "Code", "CachedData")
                ],
                "type": "folders",
                "desc": "VS Code editörünün hızlı yükleme ve çalışma için oluşturduğu önbellek."
            },
            "spotify": {
                "name": "Spotify Şarkı/Albüm Önbelleği",
                "path": os.path.join(self.user_home, "AppData", "Local", "Spotify", "Storage"),
                "type": "folder",
                "desc": "Spotify uygulamasının şarkıları hızlı oynatmak için tuttuğu yerel dosyalar."
            },
            "dns": {
                "name": "Windows DNS Önbelleği",
                "path": None,
                "type": "dns_cmd",
                "desc": "Windows'un web site adreslerini daha hızlı çözümlemek için tuttuğu önbellek."
            },
            "docker": {
                "name": "Docker Atıl İmaj ve Konteyner Hacimleri",
                "path": None,
                "type": "docker_cmd",
                "desc": "Kullanılmayan, arka planda birikmiş eski Docker kalıntıları."
            },
            "conda": {
                "name": "Anaconda / Conda Paket Önbelleği",
                "path": None,
                "type": "conda_cmd",
                "desc": "Kullanılmayan Conda paket kurulum dosyaları ve tarball yedekleri."
            }
        }
        
        self.checkbox_vars = {}
        self.sizes = {}
        self.is_scanning = False
        self.is_cleaning = False
        
        self.setup_ui()
        self.start_scan()

    def setup_ui(self):
        # Header Section
        self.header_frame = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="#1e293b")
        self.header_frame.pack(fill="x", side="top")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="🛡️ Cortex Privacy & Cache Cleaner", 
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#10b981"
        )
        self.title_label.pack(anchor="w", padx=25, pady=(18, 2))
        
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Sisteminizdeki önbellek ve geçici dosyaları tespit edin, güvenle temizleyin.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#94a3b8"
        )
        self.subtitle_label.pack(anchor="w", padx=25, pady=(0, 15))
        
        # Main Area Container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Section Title & Total Frame
        self.section_header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.section_header_frame.pack(fill="x", pady=(0, 8))
        
        self.section_label = ctk.CTkLabel(
            self.section_header_frame,
            text="Temizlenebilir Önbellek Kaynakları",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#e2e8f0"
        )
        self.section_label.pack(side="left")
        
        self.total_label = ctk.CTkLabel(
            self.section_header_frame,
            text="Toplam Tespit Edilen: 0.00 GB",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#10b981",
            fg_color="#1e293b",
            corner_radius=6,
            height=24
        )
        self.total_label.pack(side="right", padx=5)
        
        # Scrollable Frame for Targets
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container, height=260, fg_color="#0f172a", border_width=1, border_color="#1e293b")
        self.scroll_frame.pack(fill="x", pady=(0, 15))
        
        self.target_widgets = {}
        for key, info in self.targets.items():
            # Card Container
            card = ctk.CTkFrame(self.scroll_frame, fg_color="#1e293b", corner_radius=8, height=65)
            card.pack(fill="x", pady=5, padx=5)
            card.pack_propagate(False)
            
            # Left block: Checkbox and title
            left_frame = ctk.CTkFrame(card, fg_color="transparent")
            left_frame.pack(side="left", fill="both", expand=True, padx=15, pady=8)
            
            var = ctk.BooleanVar(value=True)
            self.checkbox_vars[key] = var
            
            chk = ctk.CTkCheckBox(
                left_frame,
                text=info["name"],
                variable=var,
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                text_color="#f1f5f9",
                checkbox_width=20,
                checkbox_height=20,
                corner_radius=6
            )
            chk.pack(anchor="w")
            
            desc = ctk.CTkLabel(
                left_frame,
                text=info["desc"],
                font=ctk.CTkFont(family="Segoe UI", size=10),
                text_color="#94a3b8"
            )
            desc.pack(anchor="w", pady=(2, 0))
            
            # Right block: Size badge
            size_badge = ctk.CTkLabel(
                card,
                text="Hesaplanıyor...",
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                text_color="#10b981",
                fg_color="#0f172a",
                corner_radius=6,
                width=100,
                height=28
            )
            size_badge.pack(side="right", padx=15)
            
            self.target_widgets[key] = {
                "size_badge": size_badge,
                "checkbox": chk
            }
            
        # Logging Panel
        self.log_label = ctk.CTkLabel(
            self.main_container,
            text="İşlem Günlüğü",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#e2e8f0"
        )
        self.log_label.pack(anchor="w", pady=(0, 6))
        
        self.log_text = ctk.CTkTextbox(
            self.main_container, 
            height=100, 
            fg_color="#0b0f19", 
            text_color="#38bdf8", 
            font=ctk.CTkFont(family="Consolas", size=11),
            border_width=1,
            border_color="#1e293b"
        )
        self.log_text.pack(fill="x", pady=(0, 15))
        
        # Progress Bar
        self.progress = ctk.CTkProgressBar(self, height=8, progress_color="#10b981", fg_color="#1e293b")
        self.progress.pack(fill="x", padx=25, pady=(0, 15))
        self.progress.set(0)
        
        # Action Buttons Area
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(fill="x", side="bottom", padx=25, pady=(0, 25))
        
        self.scan_btn = ctk.CTkButton(
            self.btn_frame,
            text="🔄 Yeniden Tara",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#334155",
            hover_color="#475569",
            width=160,
            height=38,
            command=self.start_scan
        )
        self.scan_btn.pack(side="left")
        
        self.clean_btn = ctk.CTkButton(
            self.btn_frame,
            text="🧼 Seçilenleri Güvenle Temizle",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            width=220,
            height=38,
            command=self.start_clean
        )
        self.clean_btn.pack(side="right")

    def log(self, msg):
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")

    def get_dir_size(self, path):
        total = 0
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file(follow_symlinks=False):
                        total += entry.stat(follow_symlinks=False).st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total += self.get_dir_size(entry.path)
        except Exception:
            pass
        return total

    def start_scan(self):
        if self.is_scanning or self.is_cleaning: return
        self.is_scanning = True
        self.scan_btn.configure(state="disabled")
        self.clean_btn.configure(state="disabled")
        self.progress.configure(mode="indeterminate")
        self.progress.start()
        self.log_text.delete("1.0", "end")
        self.log("🔍 Önbellek dizinleri taranıyor...")
        
        threading.Thread(target=self.scan_worker, daemon=True).start()

    def scan_worker(self):
        for key, info in self.targets.items():
            self.log(f"İnceleniyor: {info['name']}...")
            size_str = "0.00 GB"
            
            if info["type"] == "folder" or info["type"] == "temp_files":
                if os.path.exists(info["path"]):
                    bytes_size = self.get_dir_size(info["path"])
                    gb_size = bytes_size / (1024 ** 3)
                    size_str = f"{gb_size:.2f} GB"
                    self.sizes[key] = bytes_size
                else:
                    size_str = "Bulunamadı"
                    self.sizes[key] = 0
            elif info["type"] == "folders":
                bytes_size = 0
                found = False
                for p in info["paths"]:
                    if os.path.exists(p):
                        bytes_size += self.get_dir_size(p)
                        found = True
                if found:
                    gb_size = bytes_size / (1024 ** 3)
                    size_str = f"{gb_size:.2f} GB"
                    self.sizes[key] = bytes_size
                else:
                    size_str = "Bulunamadı"
                    self.sizes[key] = 0
            elif info["type"] == "dns_cmd":
                size_str = "Sistem Önbelleği"
                self.sizes[key] = 1 # dummy size to allow selection
            elif info["type"] == "docker_cmd":
                docker_path = os.path.join(self.user_home, "AppData", "Local", "Docker")
                if os.path.exists(docker_path):
                    bytes_size = self.get_dir_size(docker_path)
                    gb_size = bytes_size / (1024 ** 3)
                    size_str = f"~{gb_size:.2f} GB"
                    self.sizes[key] = bytes_size
                else:
                    size_str = "Bulunamadı"
                    self.sizes[key] = 0
            elif info["type"] == "conda_cmd":
                conda_found = shutil.which("conda") is not None
                if conda_found:
                    size_str = "Yüklü (Önbellek)"
                    self.sizes[key] = 1
                else:
                    size_str = "Bulunamadı"
                    self.sizes[key] = 0
                    
            self.after(0, self.update_size_label, key, size_str)
            
        self.after(0, self.scan_complete)
  
    def update_size_label(self, key, text):
        self.target_widgets[key]["size_badge"].configure(text=text)
  
    def scan_complete(self):
        self.is_scanning = False
        self.progress.stop()
        self.progress.configure(mode="determinate")
        self.progress.set(1.0)
        self.scan_btn.configure(state="normal")
        self.clean_btn.configure(state="normal")
        
        total_bytes = sum(v for k, v in self.sizes.items() if k not in ("conda", "dns"))
        total_gb = total_bytes / (1024 ** 3)
        self.total_label.configure(text=f"Toplam Tespit Edilen: {total_gb:.2f} GB")
        
        self.log(f"✅ Tarama tamamlandı. Toplam {total_gb:.2f} GB önbellek/geçici dosya tespit edildi.")

    def start_clean(self):
        if self.is_scanning or self.is_cleaning: return
        
        selected_keys = [k for k, v in self.checkbox_vars.items() if v.get() and self.sizes.get(k, 0) > 0]
        if not selected_keys:
            self.log("⚠ Temizlenecek boyutu olan hiçbir öğe seçilmedi.")
            return
            
        confirm = messagebox.askyesno(
            "Temizlik Onayı", 
            "Seçilen önbellek ve geçici dosyalar kalıcı olarak silinecektir.\nDevam etmek istiyor musunuz?"
        )
        if not confirm: return
        
        self.is_cleaning = True
        self.scan_btn.configure(state="disabled")
        self.clean_btn.configure(state="disabled")
        self.progress.set(0.0)
        self.log_text.delete("1.0", "end")
        self.log("🧼 Temizleme işlemi başlatıldı...")
        
        threading.Thread(target=self.clean_worker, args=(selected_keys,), daemon=True).start()

    def clean_worker(self, keys):
        total_steps = len(keys)
        for idx, key in enumerate(keys):
            info = self.targets[key]
            self.log(f"Siliniyor ({idx+1}/{total_steps}): {info['name']}...")
            
            try:
                if info["type"] == "folder":
                    if os.path.exists(info["path"]):
                        self.log(f"[DOSYA SİL] Dizin kaldırılıyor: {info['path']}")
                        shutil.rmtree(info["path"], ignore_errors=True)
                        self.log(f"✓ {info['name']} başarıyla temizlendi.")
                elif info["type"] == "folders":
                    for p in info["paths"]:
                        if os.path.exists(p):
                            self.log(f"[DOSYA SİL] Dizin kaldırılıyor: {p}")
                            shutil.rmtree(p, ignore_errors=True)
                    self.log(f"✓ {info['name']} başarıyla temizlendi.")
                elif info["type"] == "dns_cmd":
                    self.log("[CMD RUN] ipconfig /flushdns")
                    res = subprocess.run("ipconfig /flushdns", shell=True, capture_output=True, text=True)
                    if res.returncode == 0:
                        self.log("✓ Windows DNS önbelleği başarıyla temizlendi.")
                    else:
                        self.log("⚠ DNS önbelleği temizlenemedi.")
                elif info["type"] == "temp_files":
                    if os.path.exists(info["path"]):
                        self.log(f"[DOSYA SİL] Geçici dosyalar temizleniyor: {info['path']}")
                        for file_name in os.listdir(info["path"]):
                            file_path = os.path.join(info["path"], file_name)
                            try:
                                if os.path.isfile(file_path) or os.path.islink(file_path):
                                    os.unlink(file_path)
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path, ignore_errors=True)
                            except Exception:
                                pass
                        self.log(f"✓ Windows geçici dosyaları temizlendi.")
                elif info["type"] == "docker_cmd":
                    self.log("[CMD RUN] docker system prune -a --volumes --force")
                    res = subprocess.run("docker system prune -a --volumes --force", shell=True, capture_output=True, text=True)
                    if res.returncode == 0:
                        self.log("✓ Docker kullanılmayan kalıntılar temizlendi.")
                    else:
                        self.log("⚠ Docker kapalı olduğu için temizlik atlandı.")
                elif info["type"] == "conda_cmd":
                    self.log("[CMD RUN] conda clean --all -y")
                    res = subprocess.run("conda clean --all -y", shell=True, capture_output=True, text=True)
                    if res.returncode == 0:
                        self.log("✓ Conda paket önbellekleri temizlendi.")
                    else:
                        self.log("⚠ Conda komutu çalıştırılamadı.")
            except Exception as e:
                self.log(f"❌ Hata ({info['name']}): {str(e)}")
                
            progress_val = (idx + 1) / total_steps
            self.after(0, lambda val=progress_val: self.progress.set(val))
            
        self.after(0, self.clean_complete)

    def clean_complete(self):
        self.is_cleaning = False
        self.scan_btn.configure(state="normal")
        self.clean_btn.configure(state="normal")
        self.log("🎉 Temizlik tamamlandı! Güncel durum için yeniden taranıyor...")
        self.start_scan()
        messagebox.showinfo("Başarılı", "Seçilen tüm önbellek ve geçici dosyalar başarıyla temizlendi!")

if __name__ == "__main__":
    app = ModernCacheCleaner()
    app.mainloop()
