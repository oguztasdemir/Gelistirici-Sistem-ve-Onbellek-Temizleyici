import os
import shutil
import time
from dataclasses import dataclass
from typing import Callable, Optional
from src.core.settings import settings
from src.core.scanner import ScannerEngine
from src.utils.formatters import format_bytes

PROJECT_JUNK_NAMES = {
    "node_modules": ("📦 Node.js Bağımlılıkları", "JavaScript / TypeScript paketleri"),
    ".venv": ("🐍 Python Sanal Ortamı (.venv)", "Python paketleri ve ikili dosyaları"),
    "venv": ("🐍 Python Sanal Ortamı (venv)", "Python paketleri ve ikili dosyaları"),
    "env": ("🐍 Python Sanal Ortamı (env)", "Python paketleri ve ortam dosyaları"),
    "target": ("🦀 Rust Derleme Artığı (target)", "Cargo derleme çıktıları ve ikilileri"),
    "build": ("🏗️ Derleme Çıktısı (build)", "Geçici derleme ve paketleme dosyaları"),
    "dist": ("📦 Dağıtım Klasörü (dist)", "Üretilen dağıtım paketleri"),
    ".next": ("▲ Next.js Derleme Önbelleği", "Next.js önbellek ve sayfaları"),
    ".nuxt": ("💚 Nuxt.js Derleme Önbelleği", "Nuxt.js çalışma önbellekleri"),
    "__pycache__": ("⚡ Python Bytecode Önbelleği", ".pyc derlenmiş bytecode dosyaları"),
    ".pytest_cache": ("🧪 Pytest Test Önbelleği", "Birim test çalışma önbelleği"),
    ".dart_tool": ("🎯 Dart & Flutter Araçları", "Flutter paket ve derleme önbellekleri")
}

IGNORED_SCAN_FOLDERS = {".git", ".svn", ".hg", "System Volume Information", "$RECYCLE.BIN"}

@dataclass
class ProjectJunkItem:
    path: str
    folder_name: str
    project_name: str
    junk_type_title: str
    size_bytes: int
    modified_time: float
    is_selected: bool = True

    @property
    def formatted_size(self) -> str:
        return format_bytes(self.size_bytes)

    @property
    def formatted_date(self) -> str:
        if not self.modified_time:
            return "-"
        return time.strftime("%d.%m.%Y", time.localtime(self.modified_time))


class ProjectCleanerEngine:
    """Yazılım projelerindeki bağımlılık ve önbellek klasörlerini derinlemesine tarayan motor."""

    def __init__(self):
        self.found_items: list[ProjectJunkItem] = []
        self._scanner = ScannerEngine()

    def scan_directory(
        self,
        root_dir: str,
        progress_callback: Optional[Callable[[str], None]] = None,
        max_depth: int = 4
    ) -> list[ProjectJunkItem]:
        self.found_items = []
        if not os.path.exists(root_dir):
            return []

        root_norm = os.path.normpath(root_dir)
        root_depth = root_norm.count(os.sep)

        try:
            for current_root, dirs, files in os.walk(root_dir, topdown=True):
                # Ignore system & git internal folders
                dirs[:] = [d for d in dirs if d not in IGNORED_SCAN_FOLDERS]

                cur_depth = os.path.normpath(current_root).count(os.sep) - root_depth
                if cur_depth > max_depth:
                    dirs.clear()
                    continue

                for d in list(dirs):
                    if d in PROJECT_JUNK_NAMES:
                        full_junk_path = os.path.join(current_root, d)
                        
                        # Whitelist check
                        if settings.is_whitelisted(full_junk_path):
                            continue

                        if progress_callback:
                            progress_callback(full_junk_path)

                        sz, _ = self._scanner.get_path_size_and_count(full_junk_path, max_depth=4)
                        mtime = 0
                        try:
                            mtime = os.path.getmtime(full_junk_path)
                        except Exception:
                            pass

                        title, desc = PROJECT_JUNK_NAMES[d]
                        project_name = os.path.basename(current_root)

                        self.found_items.append(
                            ProjectJunkItem(
                                path=full_junk_path,
                                folder_name=d,
                                project_name=project_name,
                                junk_type_title=title,
                                size_bytes=sz,
                                modified_time=mtime,
                                is_selected=True
                            )
                        )
                        # Don't descend into node_modules or venv
                        dirs.remove(d)
        except Exception:
            pass

        self.found_items.sort(key=lambda x: x.size_bytes, reverse=True)
        return self.found_items

    def clean_selected(
        self,
        items: list[ProjectJunkItem],
        log_callback: Optional[Callable[[str], None]] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> tuple[int, int]:
        """Seçilen proje klasörlerini siler. (freed_bytes, deleted_count) döndürür."""
        freed = 0
        deleted_count = 0
        total = len(items)

        for idx, item in enumerate(items):
            if not item.is_selected:
                continue

            if progress_callback:
                progress_callback(idx + 1, total)

            if log_callback:
                log_callback(f"🧹 Proje artığı siliniyor: {item.project_name} -> {item.folder_name}")

            try:
                if os.path.exists(item.path):
                    shutil.rmtree(item.path, ignore_errors=True)
                    freed += item.size_bytes
                    deleted_count += 1
            except Exception as e:
                if log_callback:
                    log_callback(f"  ❌ Hata: {str(e)}")

        return freed, deleted_count
