import customtkinter as ctk
from src.config import (
    COLOR_CARD_BG, COLOR_CARD_BORDER, COLOR_ACCENT, 
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_PRIMARY
)

class LogPanelComponent(ctk.CTkFrame):
    """İşlem kayıtlarını canlı gösteren, temizleme ve kopyalama destekli modern konsol paneli."""

    def __init__(self, parent, height: int = 100):
        super().__init__(parent, fg_color="transparent")
        self.preferred_height = height
        self.setup_ui()

    def setup_ui(self):
        # Header bar
        header_bar = ctk.CTkFrame(self, fg_color="transparent")
        header_bar.pack(fill="x", pady=(0, 4))

        title = ctk.CTkLabel(
            header_bar,
            text="📜 Canlı İşlem Günlüğü (Terminal)",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=COLOR_TEXT_MUTED
        )
        title.pack(side="left")

        # Action buttons on right
        actions_box = ctk.CTkFrame(header_bar, fg_color="transparent")
        actions_box.pack(side="right")

        copy_btn = ctk.CTkButton(
            actions_box,
            text="📋 Kopyala",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            fg_color="#182334",
            hover_color="#24344d",
            border_width=1,
            border_color="#2a3a52",
            width=65,
            height=22,
            corner_radius=4,
            command=self.copy_logs
        )
        copy_btn.pack(side="left", padx=(0, 6))

        clear_btn = ctk.CTkButton(
            actions_box,
            text="🗑️ Temizle",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            fg_color="#182334",
            hover_color="#24344d",
            border_width=1,
            border_color="#2a3a52",
            width=65,
            height=22,
            corner_radius=4,
            command=self.clear_logs
        )
        clear_btn.pack(side="left")

        # Textbox
        self.textbox = ctk.CTkTextbox(
            self,
            height=self.preferred_height,
            fg_color="#090d16",
            text_color="#38bdf8",
            font=ctk.CTkFont(family="Consolas", size=10),
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            corner_radius=6
        )
        self.textbox.pack(fill="both", expand=True)

    def log(self, message: str):
        self.textbox.insert("end", f"{message}\n")
        self.textbox.see("end")

    def clear_logs(self):
        self.textbox.delete("1.0", "end")

    def copy_logs(self):
        content = self.textbox.get("1.0", "end").strip()
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            self.log("ℹ [GÜNLÜK] Günlük metni panoya kopyalandı.")
