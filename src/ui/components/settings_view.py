import os
from tkinter import filedialog, messagebox
import customtkinter as ctk

from src.i18n import t, set_language, get_language
from src.core.settings import settings
from src.config import (
    COLOR_BG_DARK, COLOR_CARD_BG, COLOR_CARD_BORDER,
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_ACCENT,
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_DANGER
)

class SettingsView(ctk.CTkFrame):
    """Yaşam boyu istatistikler, dil seçimi ve kalıcı beyaz liste yönetim görünümü."""

    def __init__(self, parent, on_language_changed_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.on_language_changed = on_language_changed_callback
        self.setup_ui()

    def setup_ui(self):
        # 1. Lifetime Statistics Card
        stats_card = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=8, border_width=1, border_color=COLOR_CARD_BORDER)
        stats_card.pack(fill="x", pady=(0, 12), padx=2)

        stats_header = ctk.CTkFrame(stats_card, fg_color="transparent")
        stats_header.pack(fill="x", padx=16, pady=(12, 10))

        title = ctk.CTkLabel(
            stats_header,
            text=t("stats_title"),
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        title.pack(side="left")

        # Stats items grid
        grid_frame = ctk.CTkFrame(stats_card, fg_color="transparent")
        grid_frame.pack(fill="x", padx=16, pady=(0, 14))

        # Item 1: Total Space Freed
        self.stat_freed_lbl = ctk.CTkLabel(
            grid_frame,
            text=f"{t('stat_lifetime_freed')}  {settings.get_formatted_lifetime_freed()}",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=COLOR_ACCENT
        )
        self.stat_freed_lbl.pack(anchor="w", pady=2)

        # Item 2: Sessions Count
        self.stat_sessions_lbl = ctk.CTkLabel(
            grid_frame,
            text=f"{t('stat_sessions_count')}  {settings.get_cleaning_sessions_count()} seans",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXT_MAIN
        )
        self.stat_sessions_lbl.pack(anchor="w", pady=2)

        # Item 3: Last cleaned date
        self.stat_last_lbl = ctk.CTkLabel(
            grid_frame,
            text=f"{t('stat_last_cleaned')}  {settings.get_formatted_last_cleaned()}",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXT_MUTED
        )
        self.stat_last_lbl.pack(anchor="w", pady=2)

        # 2. General Preferences Card (Language & UI)
        pref_card = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=8, border_width=1, border_color=COLOR_CARD_BORDER)
        pref_card.pack(fill="x", pady=(0, 12), padx=2)

        pref_inner = ctk.CTkFrame(pref_card, fg_color="transparent")
        pref_inner.pack(fill="x", padx=16, pady=12)

        lang_lbl = ctk.CTkLabel(
            pref_inner,
            text=t("language_setting"),
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        lang_lbl.pack(side="left")

        current_lang = get_language()
        self.lang_segmented = ctk.CTkSegmentedButton(
            pref_inner,
            values=["Türkçe", "English"],
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            selected_color=COLOR_PRIMARY,
            command=self._handle_language_change
        )
        self.lang_segmented.set("Türkçe" if current_lang == "tr" else "English")
        self.lang_segmented.pack(side="right")

        # 3. Whitelist Manager Card
        white_card = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=8, border_width=1, border_color=COLOR_CARD_BORDER)
        white_card.pack(fill="both", expand=True, padx=2)

        white_header = ctk.CTkFrame(white_card, fg_color="transparent")
        white_header.pack(fill="x", padx=16, pady=(12, 6))

        w_title = ctk.CTkLabel(
            white_header,
            text=t("whitelist_title"),
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        w_title.pack(anchor="w")

        w_desc = ctk.CTkLabel(
            white_header,
            text=t("whitelist_desc"),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXT_MUTED
        )
        w_desc.pack(anchor="w", pady=(2, 0))

        # Input row
        input_row = ctk.CTkFrame(white_card, fg_color="transparent")
        input_row.pack(fill="x", padx=16, pady=(8, 10))

        self.whitelist_entry = ctk.CTkEntry(
            input_row,
            placeholder_text=t("whitelist_placeholder"),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            height=34,
            fg_color=COLOR_BG_DARK,
            border_color=COLOR_CARD_BORDER
        )
        self.whitelist_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        browse_btn = ctk.CTkButton(
            input_row,
            text=t("btn_browse"),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color="#334155",
            hover_color="#475569",
            width=90,
            height=34,
            command=self.browse_whitelist_path
        )
        browse_btn.pack(side="left", padx=(0, 8))

        add_btn = ctk.CTkButton(
            input_row,
            text=t("btn_add_whitelist"),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            width=120,
            height=34,
            command=self.add_whitelist_entry
        )
        add_btn.pack(side="left")

        # Scroll list of whitelisted paths
        self.whitelist_scroll = ctk.CTkScrollableFrame(
            white_card,
            fg_color=COLOR_BG_DARK,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            corner_radius=6
        )
        self.whitelist_scroll.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        self.refresh_whitelist_ui()

    def refresh_stats(self):
        self.stat_freed_lbl.configure(text=f"{t('stat_lifetime_freed')}  {settings.get_formatted_lifetime_freed()}")
        self.stat_sessions_lbl.configure(text=f"{t('stat_sessions_count')}  {settings.get_cleaning_sessions_count()} seans")
        self.stat_last_lbl.configure(text=f"{t('stat_last_cleaned')}  {settings.get_formatted_last_cleaned()}")

    def _handle_language_change(self, value: str):
        code = "tr" if value == "Türkçe" else "en"
        set_language(code)
        settings.set_language(code)
        if self.on_language_changed:
            self.on_language_changed(code)

    def browse_whitelist_path(self):
        chosen = filedialog.askdirectory()
        if chosen:
            self.whitelist_entry.delete(0, "end")
            self.whitelist_entry.insert(0, chosen)

    def add_whitelist_entry(self):
        val = self.whitelist_entry.get().strip()
        if val:
            settings.add_to_whitelist(val)
            self.whitelist_entry.delete(0, "end")
            self.refresh_whitelist_ui()

    def remove_whitelist_entry(self, path: str):
        settings.remove_from_whitelist(path)
        self.refresh_whitelist_ui()

    def refresh_whitelist_ui(self):
        for w in self.whitelist_scroll.winfo_children():
            w.destroy()

        paths = settings.get_whitelist()
        if not paths:
            lbl = ctk.CTkLabel(
                self.whitelist_scroll,
                text="Beyaz listede henüz kayıtlı bir koruma yolu yok.",
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=COLOR_TEXT_MUTED
            )
            lbl.pack(pady=20)
            return

        for p in paths:
            row = ctk.CTkFrame(self.whitelist_scroll, fg_color=COLOR_CARD_BG, corner_radius=4, height=36)
            row.pack(fill="x", pady=2, padx=2)
            row.pack_propagate(False)

            icon_lbl = ctk.CTkLabel(row, text="🛡️", font=ctk.CTkFont(size=12))
            icon_lbl.pack(side="left", padx=(10, 6))

            path_lbl = ctk.CTkLabel(
                row,
                text=p,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=COLOR_TEXT_MAIN
            )
            path_lbl.pack(side="left", fill="x", expand=True)

            del_btn = ctk.CTkButton(
                row,
                text="🗑️",
                width=28,
                height=26,
                fg_color="transparent",
                hover_color=COLOR_DANGER,
                command=lambda target=p: self.remove_whitelist_entry(target)
            )
            del_btn.pack(side="right", padx=6)
