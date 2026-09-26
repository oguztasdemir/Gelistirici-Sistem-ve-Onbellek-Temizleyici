import os
import hashlib
import time
from dataclasses import dataclass
from typing import Callable, Optional
from src.core.settings import settings
from src.utils.formatters import format_bytes

@dataclass
class DuplicateFileGroup:
    file_hash: str
    size_bytes: int
    files: list[str]

    @property
    def formatted_size(self) -> str:
        return format_bytes(self.size_bytes)

    @property
    def wasted_size(self) -> str:
        wasted = self.size_bytes * (len(self.files) - 1)
        return format_bytes(wasted)

class DuplicateFinderEngine:
    """Diskteki yinelenen (birebir kopya) dosyaları MD5/SHA-256 ile tespit eden motor."""

    def __init__(self):
        self.duplicate_groups: list[DuplicateFileGroup] = []

    def _get_file_hash(self, path: str, sample_size: int = 64 * 1024) -> str:
        """Hızlı kontrol için dosyanın başını ve sonunu hashler."""
        hasher = hashlib.md5()
        try:
            file_size = os.path.getsize(path)
            with open(path, "rb") as f:
                if file_size <= sample_size * 2:
                    hasher.update(f.read())
                else:
                    # Başından ve sonundan örnek al
                    hasher.update(f.read(sample_size))
                    f.seek(-sample_size, os.SEEK_END)
                    hasher.update(f.read(sample_size))
            return hasher.hexdigest()
        except Exception:
            return ""

    def scan_duplicates(
        self,
        target_dir: str,
        min_size_bytes: int = 10 * 1024 * 1024, # Varsayılan 10 MB+
        progress_callback: Optional[Callable[[str], None]] = None,
        max_depth: int = 5
    ) -> list[DuplicateFileGroup]:
        self.duplicate_groups = []
        if not os.path.exists(target_dir):
            return []

        # 1. Aşama: Dosyaları boyutlarına göre grupla
        size_dict: dict[int, list[str]] = {}
        root_norm = os.path.normpath(target_dir)
        root_depth = root_norm.count(os.sep)

        try:
            for current_root, dirs, files in os.walk(target_dir, topdown=True):
                cur_depth = os.path.normpath(current_root).count(os.sep) - root_depth
                if cur_depth > max_depth:
                    dirs.clear()
                    continue

                for f in files:
                    fp = os.path.join(current_root, f)
                    if settings.is_whitelisted(fp):
                        continue
                    try:
                        sz = os.path.getsize(fp)
                        if sz >= min_size_bytes:
                            size_dict.setdefault(sz, []).append(fp)
                    except (PermissionError, OSError):
                        continue
        except Exception:
            pass

        # 2. Aşama: Aynı boyuttaki dosyaların hashlerini karşılaştır
        candidate_sizes = [sz for sz, paths in size_dict.items() if len(paths) > 1]
        
        for sz in candidate_sizes:
            paths = size_dict[sz]
            hash_dict: dict[str, list[str]] = {}

            for p in paths:
                if progress_callback:
                    progress_callback(p)
                h = self._get_file_hash(p)
                if h:
                    hash_dict.setdefault(h, []).append(p)

            for h, dup_paths in hash_dict.items():
                if len(dup_paths) > 1:
                    self.duplicate_groups.append(
                        DuplicateFileGroup(
                            file_hash=h,
                            size_bytes=sz,
                            files=dup_paths
                        )
                    )

        # En çok yer kaplayan kopyaları başa al
        self.duplicate_groups.sort(key=lambda x: x.size_bytes * (len(x.files) - 1), reverse=True)
        return self.duplicate_groups
