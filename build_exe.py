"""
Cache Cleaner - Tek Tıkla Standalone Windows .exe Derleme Betiği
"""

import os
import sys
import subprocess

def build():
    print("========================================================")
    print("  Cache Cleaner - Windows Standalone Executable Builder")
    print("========================================================")
    print()

    # 1. PyInstaller check
    try:
        import PyInstaller
        print("[+] PyInstaller mevcut.")
    except ImportError:
        print("[*] PyInstaller kuruluyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 2. Build command
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name=CacheCleaner",
        "--clean",
        "main.py"
    ]

    print(f"[*] Derleme komutu calistiriliyor: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        exe_path = os.path.abspath(os.path.join("dist", "CacheCleaner.exe"))
        print()
        print("========================================================")
        print("  [✓] DERLEME BASARIYLA TAMAMLANDI!")
        print(f"  Calistirilabilir dosya: {exe_path}")
        print("========================================================")
    else:
        print()
        print("[HATA] Derleme sirasinda bir sorun olustu.")

if __name__ == "__main__":
    build()
