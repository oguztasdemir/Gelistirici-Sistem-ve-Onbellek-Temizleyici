import os
import time
from dataclasses import dataclass
from typing import Callable, Optional
from src.core.settings import settings
from src.utils.formatters import format_bytes

FILE_CATEGORY_MAP = {
    # Video & Media
    ".mp4": "🎬 Video", ".mkv": "🎬 Video", ".avi": "🎬 Video", ".mov": "🎬 Video", ".wmv": "🎬 Video",
    # Disk & VM
    ".vhdx": "💽 Sanal Disk", ".vmdk": "💽 Sanal Disk", ".vdi": "💽 Sanal Disk", ".iso": "💿 Disk İmajı", ".img": "💿 Disk İmajı",
    # Arşiv
    ".zip": "📦 Arşiv", ".rar": "📦 Arşiv", ".7z": "📦 Arşiv", ".tar": "📦 Arşiv", ".gz": "📦 Arşiv",
    # Model & Yapay Zeka
    ".bin": "🤖 Model / İkili", ".safetensors": "🤖 AI Model", ".pth": "🤖 PyTorch Model", ".onnx": "🤖 ONNX Model", ".gguf": "🤖 LLM Modeli",
    # Kurulum
    ".exe": "💿 Kurulum / Exe", ".msi": "💿 Windows Installer"
}

@dataclass
class LargeFileInfo:
    path: str
    name: str
    size_bytes: int
    modified_time: float
    category_label: str
    is_selected: bool = False

    @property
    def formatted_size(self) -> str:
        return format_bytes(self.size_bytes)

    @property
    def formatted_date(self) -> str:
        if not self.modified_time:
            return "-"
        return time.strftime("%d.%m.%Y %H:%M", time.localtime(self.modified_time))


class LargeFileAnalyzerEngine:
    """Diskteki büyük ve yer kaplayan dosyaları tespit eden motor."""

    def __init__(self):
        self.found_files: list[LargeFileInfo] = []

    def scan_large_files(
        self,
        root_path: str,
        min_size_bytes: int = 100 * 1024 * 1024, # 100 MB default
        progress_callback: Optional[Callable[[str], None]] = None,
        max_depth: int = 6
    ) -> list[LargeFileInfo]:
        self.found_files = []
        if not os.path.exists(root_path):
            return []

        root_norm = os.path.normpath(root_path)
        root_depth = root_norm.count(os.sep)

        try:
            for current_root, dirs, files in os.walk(root_path, topdown=True):
                cur_depth = os.path.normpath(current_root).count(os.sep) - root_depth
                if cur_depth > max_depth:
                    dirs.clear()
                    continue

                for f in files:
                    full_path = os.path.join(current_root, f)
                    if settings.is_whitelisted(full_path):
                        continue

                    try:
                        sz = os.path.getsize(full_path)
                        if sz >= min_size_bytes:
                            if progress_callback:
                                progress_callback(full_path)

                            mtime = os.path.getmtime(full_path)
                            _, ext = os.path.splitext(f.lower())
                            cat = FILE_CATEGORY_MAP.get(ext, "📄 Dosya")

                            self.found_files.append(
                                LargeFileInfo(
                                    path=full_path,
                                    name=f,
                                    size_bytes=sz,
                                    modified_time=mtime,
                                    category_label=cat,
                                    is_selected=False
                                )
                            )
                    except (PermissionError, FileNotFoundError, OSError):
                        continue
        except Exception:
            pass

        self.found_files.sort(key=lambda x: x.size_bytes, reverse=True)
        return self.found_files

    def delete_selected(
        self,
        files: list[LargeFileInfo],
        log_callback: Optional[Callable[[str], None]] = None
    ) -> tuple[int, int]:
        """Seçilen büyük dosyaları siler. (freed_bytes, deleted_count) döndürür."""
        freed = 0
        deleted_count = 0

        for item in files:
            if not item.is_selected:
                continue

            if log_callback:
                log_callback(f"🗑️ Büyük dosya siliniyor: {item.name} ({item.formatted_size})")

            try:
                if os.path.exists(item.path):
                    os.remove(item.path)
                    freed += item.size_bytes
                    deleted_count += 1
            except Exception as e:
                if log_callback:
                    log_callback(f"  ❌ Hata: {str(e)}")

        return freed, deleted_count
