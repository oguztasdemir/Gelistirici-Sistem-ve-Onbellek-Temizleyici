import os
import json
import time
from src.utils.formatters import format_bytes, format_duration

SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".cache_cleaner_settings.json")

class SettingsManager:
    """Kalıcı ayarlar, beyaz liste ve yaşam boyu temizlik istatistikleri yöneticisi."""

    def __init__(self):
        self.data = {
            "language": "tr",
            "whitelist": [],
            "lifetime_freed_bytes": 0,
            "cleaning_sessions_count": 0,
            "last_cleaned_timestamp": None,
            "last_project_scan_dir": os.path.join(os.path.expanduser("~"), "Desktop")
        }
        self.load()

    def load(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.data.update(saved)
            except Exception:
                pass

    def save(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    # Language
    def get_language(self) -> str:
        return self.data.get("language", "tr")

    def set_language(self, lang: str):
        self.data["language"] = lang
        self.save()

    # Whitelist
    def get_whitelist(self) -> list[str]:
        return self.data.get("whitelist", [])

    def add_to_whitelist(self, path: str):
        norm = os.path.normpath(path)
        if norm and norm not in self.data["whitelist"]:
            self.data["whitelist"].append(norm)
            self.save()

    def remove_from_whitelist(self, path: str):
        norm = os.path.normpath(path)
        if norm in self.data["whitelist"]:
            self.data["whitelist"].remove(norm)
            self.save()

    def is_whitelisted(self, path: str) -> bool:
        norm = os.path.normpath(path).lower()
        for w in self.data.get("whitelist", []):
            if norm == os.path.normpath(w).lower() or norm.startswith(os.path.normpath(w).lower() + os.sep):
                return True
        return False

    # Stats
    def record_clean_session(self, freed_bytes: int):
        self.data["lifetime_freed_bytes"] = self.data.get("lifetime_freed_bytes", 0) + freed_bytes
        self.data["cleaning_sessions_count"] = self.data.get("cleaning_sessions_count", 0) + 1
        self.data["last_cleaned_timestamp"] = time.time()
        self.save()

    def reset_stats(self):
        self.data["lifetime_freed_bytes"] = 0
        self.data["cleaning_sessions_count"] = 0
        self.data["last_cleaned_timestamp"] = None
        self.save()

    def get_formatted_lifetime_freed(self) -> str:
        return format_bytes(self.data.get("lifetime_freed_bytes", 0))

    def get_cleaning_sessions_count(self) -> int:
        return self.data.get("cleaning_sessions_count", 0)

    def get_formatted_last_cleaned(self) -> str:
        ts = self.data.get("last_cleaned_timestamp")
        if not ts:
            return "-"
        return time.strftime("%d.%m.%Y %H:%M", time.localtime(ts))

    # Project Scan Dir
    def get_last_project_dir(self) -> str:
        return self.data.get("last_project_scan_dir", os.path.join(os.path.expanduser("~"), "Desktop"))

    def set_last_project_dir(self, path: str):
        self.data["last_project_scan_dir"] = path
        self.save()

# Singleton
settings = SettingsManager()
