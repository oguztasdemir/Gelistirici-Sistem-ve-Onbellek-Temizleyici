import os
import time
import shutil
import subprocess
from dataclasses import dataclass, field
from typing import Callable, Optional
from src.config import TARGETS
from src.core.scanner import ScanResult
from src.utils.formatters import format_bytes, format_duration


@dataclass
class CleanResult:
    """Temizleme işlemi sonucu özeti."""
    freed_bytes: int = 0
    deleted_items_count: int = 0
    skipped_items_count: int = 0
    success_targets: list[str] = field(default_factory=list)
    failed_targets: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0

    @property
    def formatted_freed(self) -> str:
        return format_bytes(self.freed_bytes)

    @property
    def formatted_duration(self) -> str:
        return format_duration(self.duration_seconds)


class CleanerEngine:
    """Önbellek ve geçici dosyaları güvenle temizleyen motor."""

    def __init__(self):
        pass

    def _delete_file_or_folder(self, path: str) -> tuple[int, bool]:
        """Tek bir dosya veya klasörü güvenle siler. (freed_bytes, success) döndürür."""
        freed = 0
        if not os.path.exists(path):
            return 0, True
        
        try:
            if os.path.isfile(path) or os.path.islink(path):
                try:
                    freed = os.path.getsize(path)
                except Exception:
                    freed = 0
                os.unlink(path)
                return freed, True
            elif os.path.isdir(path):
                # Klasör boyutunu yaklaşık hesapla
                for root, dirs, files in os.walk(path):
                    for f in files:
                        try:
                            fp = os.path.join(root, f)
                            freed += os.path.getsize(fp)
                        except Exception:
                            pass
                shutil.rmtree(path, ignore_errors=True)
                return freed, True
        except (PermissionError, OSError):
            return 0, False
        return freed, False

    def clean_target(
        self,
        key: str,
        scan_result: Optional[ScanResult],
        excluded_paths: set[str],
        log_callback: Optional[Callable[[str], None]] = None
    ) -> tuple[int, int, int, bool]:
        """
        Tek bir hedefi temizler.
        Döndürür: (freed_bytes, deleted_count, skipped_count, success)
        """
        info = TARGETS.get(key)
        if not info:
            return 0, 0, 0, False

        name = info["name"]
        target_type = info["type"]
        freed_bytes = 0
        deleted_count = 0
        skipped_count = 0
        
        if log_callback:
            log_callback(f"🧹 Temizleniyor: {name}...")

        try:
            if target_type in ("folders", "folder", "temp_files"):
                valid_paths = [p for p in info.get("paths", []) if os.path.exists(p)]
                
                for root_path in valid_paths:
                    if not os.path.exists(root_path):
                        continue
                    
                    # Eğer tüm klasör kökten silinebilir ve hariç tutulan yoksa
                    if not excluded_paths:
                        try:
                            with os.scandir(root_path) as it:
                                for entry in it:
                                    f_bytes, ok = self._delete_file_or_folder(entry.path)
                                    if ok:
                                        freed_bytes += f_bytes
                                        deleted_count += 1
                                    else:
                                        skipped_count += 1
                        except Exception as e:
                            if log_callback:
                                log_callback(f"  ⚠ Kısmi erişim hatası: {entry.name if 'entry' in locals() else str(e)}")
                    else:
                        # Hariç tutulanlar var; tek tek kontrol et
                        try:
                            with os.scandir(root_path) as it:
                                for entry in it:
                                    if entry.path in excluded_paths:
                                        if log_callback:
                                            log_callback(f"  🛡️ Hariç tutuldu: {entry.name}")
                                        continue
                                    
                                    f_bytes, ok = self._delete_file_or_folder(entry.path)
                                    if ok:
                                        freed_bytes += f_bytes
                                        deleted_count += 1
                                    else:
                                        skipped_count += 1
                        except Exception as e:
                            if log_callback:
                                log_callback(f"  ⚠ Dizin okuma hatası: {str(e)}")

            elif target_type == "dns_cmd":
                res = subprocess.run(
                    "ipconfig /flushdns", 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    errors="replace"
                )
                if res.returncode == 0:
                    deleted_count += 1
                    if log_callback:
                        log_callback("  ✓ DNS Çözümleyici önbelleği başarıyla temizlendi.")
                else:
                    skipped_count += 1
                    if log_callback:
                        log_callback("  ⚠ DNS önbelleği temizlenemedi.")

            elif target_type == "recycle_bin_cmd":
                res = subprocess.run(
                    'powershell -NoProfile -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"',
                    shell=True,
                    capture_output=True,
                    text=True,
                    errors="replace"
                )
                if res.returncode == 0:
                    deleted_count += 1
                    if log_callback:
                        log_callback("  ✓ Windows Geri Dönüşüm Kutusu başarıyla boşaltıldı.")
                else:
                    skipped_count += 1
                    if log_callback:
                        log_callback("  ⚠ Geri Dönüşüm Kutusu boşaltılamadı.")

            elif target_type == "docker_cmd":
                if shutil.which("docker"):
                    res = subprocess.run(
                        "docker system prune -a --volumes --force", 
                        shell=True, 
                        capture_output=True, 
                        text=True, 
                        errors="replace",
                        timeout=60
                    )
                    if res.returncode == 0:
                        deleted_count += 1
                        if log_callback:
                            log_callback("  ✓ Docker atıl imaj ve birimleri temizlendi.")
                    else:
                        skipped_count += 1
                        if log_callback:
                            log_callback("  ⚠ Docker arka plan hizmetine erişilemedi.")
                else:
                    if log_callback:
                        log_callback("  ℹ Docker komut satırı bulunamadı.")

            elif target_type == "conda_cmd":
                if shutil.which("conda"):
                    res = subprocess.run(
                        "conda clean --all -y",
                        shell=True, 
                        capture_output=True, 
                        text=True, 
                        errors="replace",
                        timeout=60
                    )
                    if res.returncode == 0:
                        deleted_count += 1
                        if log_callback:
                            log_callback("  ✓ Conda paket ve tarball önbelleği temizlendi.")
                    else:
                        skipped_count += 1
                        if log_callback:
                            log_callback("  ⚠ Conda temizleme komutu hata verdi.")
                else:
                    if log_callback:
                        log_callback("  ℹ Conda komut satırı bulunamadı.")

            if log_callback:
                if skipped_count > 0:
                    log_callback(f"  ✓ {name}: {deleted_count} öğe silindi, {skipped_count} aktif dosya korundu.")
                else:
                    log_callback(f"  ✓ {name} temizliği tamamlandı.")
            return freed_bytes, deleted_count, skipped_count, True

        except Exception as e:
            if log_callback:
                log_callback(f"  ❌ Hata oluştu ({name}): {str(e)}")
            return freed_bytes, deleted_count, skipped_count, False

    def clean_all(
        self,
        selected_keys: list[str],
        scan_results: dict[str, ScanResult],
        excluded_paths: set[str],
        progress_callback: Optional[Callable[[str, int, int], None]] = None,
        log_callback: Optional[Callable[[str], None]] = None
    ) -> CleanResult:
        """Seçilen tüm hedefleri temizler ve özet sonucu döner."""
        start_time = time.time()
        result = CleanResult()
        total_targets = len(selected_keys)

        for idx, key in enumerate(selected_keys):
            info = TARGETS.get(key, {})
            name = info.get("name", key)

            if progress_callback:
                progress_callback(name, idx + 1, total_targets)

            freed, deleted, skipped, success = self.clean_target(
                key=key,
                scan_result=scan_results.get(key),
                excluded_paths=excluded_paths,
                log_callback=log_callback
            )

            result.freed_bytes += freed
            result.deleted_items_count += deleted
            result.skipped_items_count += skipped

            if success:
                result.success_targets.append(key)
            else:
                result.failed_targets.append(key)

        result.duration_seconds = time.time() - start_time
        return result
