import customtkinter as ctk
from typing import Callable, Optional
from src.i18n import t, set_language, get_language
from src.core.settings import settings
from src.config import (
    APP_TITLE, CATEGORIES,
    COLOR_CARD_BG, COLOR_PRIMARY, COLOR_ACCENT, 
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED
)

class HeaderComponent(ctk.CTkFrame):
    """Modern üst başlık, gezinme sekmeleri, dil seçici ve kategori filtre butonları."""

    def __init__(
        self,
        parent,
        on_tab_change: Optional[Callable[[str], None]] = None,
        on_category_change: Optional[Callable[[str], None]] = None,
        on_select_all: Optional[Callable[[], None]] = None,
        on_deselect_all: Optional[Callable[[], None]] = None,
        on_language_change: Optional[Callable[[str], None]] = None
    ):
        super().__init__(parent, fg_color=COLOR_CARD_BG, corner_radius=0)
        self.on_tab_change = on_tab_change
        self.on_category_change = on_category_change
        self.on_select_all = on_select_all
        self.on_deselect_all = on_deselect_all
        self.on_language_change = on_language_change

        self.active_tab = "cache"
        self.active_category = "all"
        self.category_buttons: dict[str, ctk.CTkButton] = {}

        self.setup_ui()

    def setup_ui(self):
        # 1. Top branding line
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=24, pady=(14, 8))

        # Title & Subtitle Left
        text_box = ctk.CTkFrame(top_bar, fg_color="transparent")
        text_box.pack(side="left", fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            text_box,
            text=f"🧹 {t('app_title')}",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = ctk.CTkLabel(
            text_box,
            text=t("app_subtitle"),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXT_MUTED
        )
        self.subtitle_label.pack(anchor="w", pady=(2, 0))

        # Right Controls: Language & Total Size Badge
        right_box = ctk.CTkFrame(top_bar, fg_color="transparent")
        right_box.pack(side="right")

        # Language Segmented Button
        cur_lang = get_language()
        self.lang_btn = ctk.CTkSegmentedButton(
            right_box,
            values=["TR", "EN"],
            width=75,
            height=30,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            selected_color=COLOR_PRIMARY,
            command=self._handle_lang_switch
        )
        self.lang_btn.set("TR" if cur_lang == "tr" else "EN")
        self.lang_btn.pack(side="left", padx=(0, 10))

        # Total Size Badge
        self.total_badge = ctk.CTkLabel(
            right_box,
            text=t("total_detected", size="0.00 B"),
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=COLOR_PRIMARY,
            fg_color="#0f172a",
            corner_radius=8,
            height=34,
            padx=14
        )
        self.total_badge.pack(side="left")

        # 2. Middle Navigation Tabs (Segmented Navigation)
        nav_bar = ctk.CTkFrame(self, fg_color="transparent")
        nav_bar.pack(fill="x", padx=24, pady=(0, 10))

        self.tab_buttons_frame = ctk.CTkFrame(nav_bar, fg_color="#0f172a", corner_radius=8, height=36)
        self.tab_buttons_frame.pack(side="left")

        self.tab_keys = ["cache", "projects", "large_files", "stats"]
        self.tab_widgets: dict[str, ctk.CTkButton] = {}

        tab_labels = {
            "cache": t("tab_cache"),
            "projects": t("tab_projects"),
            "large_files": t("tab_large_files"),
            "stats": t("tab_stats")
        }

        for k in self.tab_keys:
            btn = ctk.CTkButton(
                self.tab_buttons_frame,
                text=tab_labels[k],
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold" if k == "cache" else "normal"),
                fg_color=COLOR_PRIMARY if k == "cache" else "transparent",
                hover_color="#059669" if k == "cache" else "#1e293b",
                height=32,
                corner_radius=6,
                command=lambda key=k: self.set_tab(key)
            )
            btn.pack(side="left", padx=3, pady=2)
            self.tab_widgets[k] = btn

        # 3. Bottom Sub-Bar: Categories & Quick Selects (Shown only on Cache tab)
        self.category_sub_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.category_sub_bar.pack(fill="x", padx=24, pady=(0, 12))

        # Category Buttons (Left)
        self.cat_frame = ctk.CTkFrame(self.category_sub_bar, fg_color="transparent")
        self.cat_frame.pack(side="left")

        for cat_key, cat_name in CATEGORIES.items():
            btn = ctk.CTkButton(
                self.cat_frame,
                text=cat_name,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold" if cat_key == "all" else "normal"),
                fg_color=COLOR_PRIMARY if cat_key == "all" else "#334155",
                hover_color="#059669" if cat_key == "all" else "#475569",
                height=28,
                corner_radius=6,
                command=lambda k=cat_key: self.set_category(k)
            )
            btn.pack(side="left", padx=(0, 6))
            self.category_buttons[cat_key] = btn

        # Quick selection helpers (Right)
        select_frame = ctk.CTkFrame(self.category_sub_bar, fg_color="transparent")
        select_frame.pack(side="right")

        self.sel_all_btn = ctk.CTkButton(
            select_frame,
            text=t("select_all"),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color="#1e293b",
            hover_color="#334155",
            border_width=1,
            border_color="#475569",
            height=28,
            width=85,
            corner_radius=6,
            command=self.on_select_all
        )
        self.sel_all_btn.pack(side="left", padx=(0, 6))

        self.desel_all_btn = ctk.CTkButton(
            select_frame,
            text=t("deselect_all"),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color="#1e293b",
            hover_color="#334155",
            border_width=1,
            border_color="#475569",
            height=28,
            width=85,
            corner_radius=6,
            command=self.on_deselect_all
        )
        self.desel_all_btn.pack(side="left")

    def _handle_lang_switch(self, val: str):
        code = "tr" if val == "TR" else "en"
        set_language(code)
        settings.set_language(code)
        if self.on_language_change:
            self.on_language_change(code)

    def set_tab(self, key: str):
        self.active_tab = key
        for k, btn in self.tab_widgets.items():
            if k == key:
                btn.configure(fg_color=COLOR_PRIMARY, hover_color="#059669", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"))
            else:
                btn.configure(fg_color="transparent", hover_color="#1e293b", font=ctk.CTkFont(family="Segoe UI", size=11, weight="normal"))

        # Toggle category sub bar visibility
        if key == "cache":
            self.category_sub_bar.pack(fill="x", padx=24, pady=(0, 12))
            self.total_badge.pack(side="left")
        else:
            self.category_sub_bar.pack_forget()
            if key in ("projects", "large_files"):
                self.total_badge.pack_forget()

        if self.on_tab_change:
            self.on_tab_change(key)

    def set_category(self, key: str):
        self.active_category = key
        for cat_key, btn in self.category_buttons.items():
            if cat_key == key:
                btn.configure(fg_color=COLOR_PRIMARY, hover_color="#059669", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"))
            else:
                btn.configure(fg_color="#334155", hover_color="#475569", font=ctk.CTkFont(family="Segoe UI", size=11, weight="normal"))
        
        if self.on_category_change:
            self.on_category_change(key)

    def update_total_size(self, text: str):
        self.total_badge.configure(text=text)
