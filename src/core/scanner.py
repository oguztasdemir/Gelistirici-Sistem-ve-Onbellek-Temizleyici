import os
import shutil
import subprocess
from dataclasses import dataclass, field
from typing import Callable, Optional
from src.config import TARGETS
from src.utils.formatters import format_bytes


@dataclass
class TargetDetailItem:
    """Detay penceresinde gösterilecek tekil alt dosya/klasör öğesi."""
    key: str                    # Benzersiz id
    name: str                   # Dosya/Klasör adı
    path: str                   # Tam dosya yolu
    size_bytes: int             # Boyut
    is_dir: bool                # Dizin mi?
    is_selected: bool = True    # Temizlenecek mi? (Varsayılan: Evet)

    @property
    def formatted_size(self) -> str:
        return format_bytes(self.size_bytes)


@dataclass
class ScanResult:
    """Bir hedefe ait tarama sonucu."""
    key: str
    name: str
    category: str
    total_bytes: int = 0
    item_count: int = 0
    detail_items: list[TargetDetailItem] = field(default_factory=list)
    status_text: str = "Taranmadı"
    is_available: bool = False
    valid_paths: list[str] = field(default_factory=list)

    @property
    def size_bytes(self) -> int:
        return self.total_bytes

    @property
    def formatted_size(self) -> str:
        if not self.is_available:
            return "Bulunamadı"
        if self.key in ("dns",):
            return "Sistem Önbelleği"
        if self.key in ("conda",) and self.total_bytes == 0:
            return "Yüklü (Önbellek)"
        return format_bytes(self.total_bytes)


class ScannerEngine:
    """Önbellek ve geçici dosyaları tarayan yüksek performanslı motor."""

    def __init__(self):
        self.results: dict[str, ScanResult] = {}

    def get_path_size_and_count(self, path: str, max_depth: int = 5) -> tuple[int, int]:
        """Bir dizinin veya dosyanın toplam boyutunu ve dosya sayısını hesaplar."""
        if not os.path.exists(path):
            return 0, 0

        try:
            if os.path.isfile(path) or os.path.islink(path):
                try:
                    return os.path.getsize(path), 1
                except Exception:
                    return 0, 1
        except Exception:
            return 0, 0

        total_size = 0
        total_files = 0
        try:
            with os.scandir(path) as it:
                for entry in it:
                    try:
                        if entry.is_file(follow_symlinks=False):
                            total_size += entry.stat(follow_symlinks=False).st_size
                            total_files += 1
                        elif entry.is_dir(follow_symlinks=False):
                            if max_depth > 0:
                                sub_size, sub_files = self.get_path_size_and_count(entry.path, max_depth - 1)
                                total_size += sub_size
                                total_files += sub_files
                    except (PermissionError, FileNotFoundError, OSError):
                        continue
        except (PermissionError, FileNotFoundError, OSError):
            pass
        return total_size, total_files

    def scan_target(self, key: str, info: dict) -> ScanResult:
        """Tek bir hedefi tek geçişte hızlıca tarar."""
        name = info["name"]
        category = info.get("category", "dev")
        target_type = info["type"]
        paths = info.get("paths", [])
        
        result = ScanResult(key=key, name=name, category=category)
        valid_paths = [p for p in paths if os.path.exists(p)]
        result.valid_paths = valid_paths

        if target_type in ("folders", "folder", "temp_files"):
            if valid_paths:
                result.is_available = True
                total_bytes = 0
                total_files = 0
                detail_items: list[TargetDetailItem] = []
                item_idx = 0

                for root_path in valid_paths:
                    try:
                        with os.scandir(root_path) as it:
                            for entry in it:
                                try:
                                    item_idx += 1
                                    item_key = f"{key}_{item_idx}"
                                    entry_name = entry.name
                                    entry_path = entry.path

                                    if entry.is_file(follow_symlinks=False):
                                        f_size = entry.stat(follow_symlinks=False).st_size
                                        total_bytes += f_size
                                        total_files += 1
                                        detail_items.append(
                                            TargetDetailItem(
                                                key=item_key,
                                                name=entry_name,
                                                path=entry_path,
                                                size_bytes=f_size,
                                                is_dir=False,
                                                is_selected=True
                                            )
                                        )
                                    elif entry.is_dir(follow_symlinks=False):
                                        dir_size, dir_count = self.get_path_size_and_count(entry_path)
                                        total_bytes += dir_size
                                        total_files += dir_count
                                        detail_items.append(
                                            TargetDetailItem(
                                                key=item_key,
                                                name=entry_name,
                                                path=entry_path,
                                                size_bytes=dir_size,
                                                is_dir=True,
                                                is_selected=True
                                            )
                                        )
                                except (PermissionError, FileNotFoundError, OSError):
                                    continue
                    except (PermissionError, FileNotFoundError, OSError):
                        continue

                # Boyuta göre büyükten küçüğe sırala
                detail_items.sort(key=lambda x: x.size_bytes, reverse=True)
                result.total_bytes = total_bytes
                result.item_count = total_files
                result.detail_items = detail_items
                result.status_text = f"{format_bytes(total_bytes)} ({total_files} öğe)"
            else:
                result.is_available = False
                result.status_text = "Bulunamadı"

        elif target_type in ("dns_cmd", "recycle_bin_cmd"):
            result.is_available = True
            result.total_bytes = 0
            result.status_text = "Sistem Aracı" if target_type == "recycle_bin_cmd" else "Sistem Önbelleği"

        elif target_type == "docker_cmd":
            if shutil.which("docker"):
                try:
                    res = subprocess.run("docker info", shell=True, capture_output=True, timeout=1.5)
                    if res.returncode == 0:
                        result.is_available = True
                        result.status_text = "Docker Açık (Prune Hazır)"
                    else:
                        result.is_available = False
                        result.status_text = "Docker Kapalı"
                except Exception:
                    result.is_available = False
                    result.status_text = "Docker Kapalı"
            else:
                result.is_available = False
                result.status_text = "Bulunamadı"

        elif target_type == "conda_cmd":
            conda_cli = shutil.which("conda") is not None
            if conda_cli:
                result.is_available = True
                result.status_text = "Conda Yüklü"
            else:
                result.is_available = False
                result.status_text = "Bulunamadı"

        self.results[key] = result
        return result

    def scan_all(
        self, 
        progress_callback: Optional[Callable[[str, int, int], None]] = None,
        item_callback: Optional[Callable[[str, ScanResult], None]] = None
    ) -> dict[str, ScanResult]:
        """Tüm hedefleri sırayla tarar."""
        total = len(TARGETS)
        for idx, (key, info) in enumerate(TARGETS.items()):
            if progress_callback:
                progress_callback(info["name"], idx + 1, total)
            
            res = self.scan_target(key, info)
            
            if item_callback:
                item_callback(key, res)
                
        return self.results
