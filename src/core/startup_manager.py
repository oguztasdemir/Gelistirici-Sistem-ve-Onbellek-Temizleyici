import os
import winreg
from dataclasses import dataclass

@dataclass
class StartupAppInfo:
    name: str
    command: str
    location: str
    is_enabled: bool = True

class StartupManagerEngine:
    """Windows başlangıç uygulamalarını listeleyen motor."""

    REG_KEYS = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKCU Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKLM Run")
    ]

    def get_startup_apps(self) -> list[StartupAppInfo]:
        apps: list[StartupAppInfo] = []

        # 1. Registry Run Keys
        for root_key, sub_key, label in self.REG_KEYS:
            try:
                with winreg.OpenKey(root_key, sub_key, 0, winreg.KEY_READ) as k:
                    count = winreg.QueryInfoKey(k)[1]
                    for i in range(count):
                        try:
                            name, val, _ = winreg.EnumValue(k, i)
                            apps.append(
                                StartupAppInfo(
                                    name=name,
                                    command=str(val),
                                    location=label,
                                    is_enabled=True
                                )
                            )
                        except Exception:
                            continue
            except Exception:
                continue

        # 2. Startup Folder Shortcuts
        startup_dir = os.path.join(os.path.expanduser("~"), r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
        if os.path.exists(startup_dir):
            for f in os.listdir(startup_dir):
                if f.endswith(".lnk") or f.endswith(".exe"):
                    apps.append(
                        StartupAppInfo(
                            name=os.path.splitext(f)[0],
                            command=os.path.join(startup_dir, f),
                            location="Başlangıç Klasörü",
                            is_enabled=True
                        )
                    )

        return apps
