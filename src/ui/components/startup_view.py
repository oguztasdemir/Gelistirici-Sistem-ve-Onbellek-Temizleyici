import customtkinter as ctk
from src.core.startup_manager import StartupManagerEngine, StartupAppInfo
from src.utils.system_helper import open_folder_in_explorer
from src.config import (
    COLOR_BG_DARK, COLOR_CARD_BG, COLOR_CARD_BORDER,
    COLOR_PRIMARY, COLOR_ACCENT, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED
)

class StartupManagerView(ctk.CTkFrame):
    """Windows başlangıç programlarını listeleyen ve yöneten görünüm."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.engine = StartupManagerEngine()
        self.apps: list[StartupAppInfo] = []

        self.setup_ui()
        self.refresh_apps()

    def setup_ui(self):
        # Header Box
        header_box = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=8, border_width=1, border_color=COLOR_CARD_BORDER)
        header_box.pack(fill="x", pady=(0, 10), padx=2)

        top_info = ctk.CTkFrame(header_box, fg_color="transparent")
        top_info.pack(fill="x", padx=16, pady=12)

        title = ctk.CTkLabel(
            top_info,
            text="🚀 Windows Başlangıç Yöneticisi (Startup Manager)",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        title.pack(anchor="w")

        desc = ctk.CTkLabel(
            top_info,
            text="Bilgisayar açılışında otomatik başlayan uygulamaları denetleyin, açılış süresini hızlandırın.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXT_MUTED
        )
        desc.pack(anchor="w", pady=(2, 0))

        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 8))

        self.summary_lbl = ctk.CTkLabel(
            toolbar,
            text="0 başlangıç uygulaması",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        self.summary_lbl.pack(side="left")

        refresh_btn = ctk.CTkButton(
            toolbar,
            text="🔄 Yenile",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color="#334155",
            hover_color="#475569",
            width=90,
            height=28,
            command=self.refresh_apps
        )
        refresh_btn.pack(side="right")

        # Scrollable List
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLOR_BG_DARK,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            corner_radius=8
        )
        self.scroll_frame.pack(fill="both", expand=True)

    def refresh_apps(self):
        self.apps = self.engine.get_startup_apps()
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        self.summary_lbl.configure(text=f"Toplam {len(self.apps)} başlangıç uygulaması tespit edildi")

        if not self.apps:
            lbl = ctk.CTkLabel(
                self.scroll_frame,
                text="Kayıtlı başlangıç uygulaması bulunamadı.",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=COLOR_TEXT_MUTED
            )
            lbl.pack(pady=40)
            return

        for app in self.apps:
            card = ctk.CTkFrame(
                self.scroll_frame,
                fg_color=COLOR_CARD_BG,
                corner_radius=6,
                border_width=1,
                border_color=COLOR_CARD_BORDER,
                height=52
            )
            card.pack(fill="x", pady=3, padx=2)
            card.pack_propagate(False)

            left_box = ctk.CTkFrame(card, fg_color="transparent")
            left_box.pack(side="left", fill="both", expand=True, padx=12, pady=6)

            title = ctk.CTkLabel(
                left_box,
                text=f"🚀  {app.name}",
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=COLOR_TEXT_MAIN
            )
            title.pack(anchor="w")

            cmd_lbl = ctk.CTkLabel(
                left_box,
                text=app.command,
                font=ctk.CTkFont(family="Segoe UI", size=9),
                text_color=COLOR_TEXT_MUTED
            )
            cmd_lbl.pack(anchor="w")

            right_box = ctk.CTkFrame(card, fg_color="transparent")
            right_box.pack(side="right", padx=10)

            loc_badge = ctk.CTkLabel(
                right_box,
                text=app.location,
                font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                text_color=COLOR_ACCENT,
                fg_color="#0f172a",
                corner_radius=4,
                padx=8,
                height=24
            )
            loc_badge.pack(side="right")
