import os
import subprocess
import platform

def open_folder_in_explorer(path: str) -> bool:
    """Belirtilen klasörü işletim sistemi dosya gezgininde açar."""
    if not path or not os.path.exists(path):
        return False
    
    try:
        if platform.system() == "Windows":
            os.startfile(os.path.abspath(path))
        elif platform.system() == "Darwin":
            subprocess.run(["open", os.path.abspath(path)], check=False)
        else:
            subprocess.run(["xdg-open", os.path.abspath(path)], check=False)
        return True
    except Exception:
        return False


def get_user_home() -> str:
    """Kullanıcı ev dizini yolunu döndürür."""
    return os.path.expanduser("~")
