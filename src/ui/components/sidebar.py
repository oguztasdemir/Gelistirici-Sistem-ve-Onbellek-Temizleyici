import shutil
import customtkinter as ctk
from typing import Callable, Optional
from src.i18n import t, get_language, set_language
from src.core.settings import settings
from src.utils.formatters import format_bytes
from src.config import (
    COLOR_BG_DARK, COLOR_SIDEBAR_BG, COLOR_SIDEBAR_BORDER, COLOR_CARD_BG,
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_ACCENT,
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_TEXT_DIM, COLOR_CARD_BORDER
)

class SidebarComponent(ctk.CTkFrame):
    """Modern sol panel navigasyon ve sistem özet bileşeni."""

    def __init__(
        self,
        parent,
        active_tab: str = "cache",
        on_tab_select: Optional[Callable[[str], None]] = None,
        on_language_change: Optional[Callable[[str], None]] = None
    ):
        super().__init__(
            parent,
            width=240,
            corner_radius=0,
            fg_color=COLOR_SIDEBAR_BG,
            border_width=1,
            border_color=COLOR_SIDEBAR_BORDER
        )
        self.pack_propagate(False)

        self.active_tab = active_tab
        self.on_tab_select = on_tab_select
        self.on_language_change = on_language_change
        self.nav_buttons: dict[str, ctk.CTkButton] = {}

        self.setup_ui()

    def setup_ui(self):
        # 1. Branding Header
        brand_frame = ctk.CTkFrame(self, fg_color="transparent")
        brand_frame.pack(fill="x", padx=16, pady=(20, 16))

        # Brand row with logo icon + text
        brand_row = ctk.CTkFrame(brand_frame, fg_color="transparent")
        brand_row.pack(fill="x")

        logo_icon_box = ctk.CTkFrame(
            brand_row,
            width=36,
            height=36,
            corner_radius=8,
            fg_color="#064e3b"
        )
        logo_icon_box.pack_propagate(False)
        logo_icon_box.pack(side="left", padx=(0, 10))

        logo_lbl = ctk.CTkLabel(
            logo_icon_box,
            text="⚡",
            font=ctk.CTkFont(size=18)
        )
        logo_lbl.pack(expand=True)

        brand_text_box = ctk.CTkFrame(brand_row, fg_color="transparent")
        brand_text_box.pack(side="left", fill="both", expand=True)

        app_title = ctk.CTkLabel(
            brand_text_box,
            text="Cache Cleaner",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        app_title.pack(anchor="w")

        sub_label = ctk.CTkLabel(
            brand_text_box,
            text="Pro Suite v2.2",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=COLOR_PRIMARY
        )
        sub_label.pack(anchor="w")

        # Divider
        divider = ctk.CTkFrame(self, height=1, fg_color=COLOR_SIDEBAR_BORDER)
        divider.pack(fill="x", padx=14, pady=(0, 14))

        # Section Header
        self.sec_lbl = ctk.CTkLabel(
            self,
            text="MAIN MENU" if cur_lang == "en" else "ANA MENÜ",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=COLOR_TEXT_DIM
        )
        self.sec_lbl.pack(anchor="w", padx=20, pady=(0, 6))

        # 2. Navigation Menu
        nav_menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_menu_frame.pack(fill="both", expand=True, padx=12)

        self.nav_items = [
            ("cache", "🧹  Sistem & Önbellek", "🧹  System & Cache"),
            ("projects", "💻  Proje Temizleyici", "💻  Project Cleaner"),
            ("large_files", "🔍  Büyük Dosyalar", "🔍  Large Files"),
            ("duplicates", "👯‍♂️  Kopya Dosya Bulucu", "👯‍♂️  Duplicate Finder"),
            ("startup", "🚀  Başlangıç Yöneticisi", "🚀  Startup Manager"),
            ("settings", "⚙️  İstatistik & Ayarlar", "⚙️  Stats & Settings")
        ]

        cur_lang = get_language()
        for key, tr_label, en_label in self.nav_items:
            label = tr_label if cur_lang == "tr" else en_label
            is_active = (key == self.active_tab)

            btn = ctk.CTkButton(
                nav_menu_frame,
                text=label,
                anchor="w",
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold" if is_active else "normal"),
                fg_color=COLOR_PRIMARY if is_active else "transparent",
                hover_color="#059669" if is_active else "#182234",
                text_color=COLOR_TEXT_MAIN if is_active else COLOR_TEXT_MUTED,
                height=38,
                corner_radius=8,
                command=lambda k=key: self._handle_tab_click(k)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[key] = btn

        # 3. Bottom Sidebar Controls (Disk Info + Language)
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", side="bottom", padx=12, pady=(0, 14))

        # Disk Storage Card
        self.disk_card = ctk.CTkFrame(
            bottom_frame,
            fg_color="#121824",
            corner_radius=8,
            border_width=1,
            border_color=COLOR_SIDEBAR_BORDER
        )
        self.disk_card.pack(fill="x", pady=(0, 10))

        disk_header = ctk.CTkFrame(self.disk_card, fg_color="transparent")
        disk_header.pack(fill="x", padx=10, pady=(8, 4))

        d_title = ctk.CTkLabel(
            disk_header,
            text="💽 C: Sürücüsü",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        d_title.pack(side="left")

        try:
            total, used, free = shutil.disk_usage("C:\\")
            pct = used / total
            used_str = format_bytes(used)
            total_str = format_bytes(total)
            free_str = format_bytes(free)
        except Exception:
            pct = 0.5
            used_str = "-"
            total_str = "-"
            free_str = "-"

        self.disk_free_lbl = ctk.CTkLabel(
            disk_header,
            text=f"{free_str} boş",
            font=ctk.CTkFont(family="Segoe UI", size=9, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        self.disk_free_lbl.pack(side="right")

        self.disk_bar = ctk.CTkProgressBar(
            self.disk_card,
            height=6,
            progress_color=COLOR_PRIMARY if pct < 0.85 else "#f43f5e",
            fg_color="#090d16",
            corner_radius=3
        )
        self.disk_bar.pack(fill="x", padx=10, pady=(0, 8))
        self.disk_bar.set(pct)

        # Language Segmented Button at bottom
        lang_card = ctk.CTkFrame(
            bottom_frame,
            fg_color="transparent"
        )
        lang_card.pack(fill="x")

        lang_label = ctk.CTkLabel(
            lang_card,
            text="🌍 Dil / Lang:",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXT_MUTED
        )
        lang_label.pack(side="left", padx=(4, 0))

        self.lang_segmented = ctk.CTkSegmentedButton(
            lang_card,
            values=["🇹🇷 TR", "🇬🇧 EN"],
            width=100,
            height=28,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            selected_color=COLOR_PRIMARY,
            selected_hover_color=COLOR_PRIMARY_HOVER,
            unselected_color="#182234",
            unselected_hover_color="#1e2d44",
            command=self._handle_lang_switch
        )
        self.lang_segmented.set("🇹🇷 TR" if cur_lang == "tr" else "🇬🇧 EN")
        self.lang_segmented.pack(side="right")

    def _handle_tab_click(self, key: str):
        self.active_tab = key
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(
                    fg_color=COLOR_PRIMARY,
                    hover_color=COLOR_PRIMARY_HOVER,
                    text_color=COLOR_TEXT_MAIN,
                    font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    hover_color="#182234",
                    text_color=COLOR_TEXT_MUTED,
                    font=ctk.CTkFont(family="Segoe UI", size=12, weight="normal")
                )

        if self.on_tab_select:
            self.on_tab_select(key)

    def _handle_lang_switch(self, val: str):
        code = "tr" if "TR" in val else "en"
        set_language(code)
        settings.set_language(code)
        self.update_labels()
        if self.on_language_change:
            self.on_language_change(code)

    def update_labels(self):
        cur_lang = get_language()
        if hasattr(self, "sec_lbl"):
            self.sec_lbl.configure(text="MAIN MENU" if cur_lang == "en" else "ANA MENÜ")
        for key, tr_label, en_label in self.nav_items:
            if key in self.nav_buttons:
                label = tr_label if cur_lang == "tr" else en_label
                self.nav_buttons[key].configure(text=label)
        try:
            total, used, free = shutil.disk_usage("C:\\")
            free_str = format_bytes(free)
            self.disk_free_lbl.configure(text=f"{free_str} free" if cur_lang == "en" else f"{free_str} boş")
        except Exception:
            pass
