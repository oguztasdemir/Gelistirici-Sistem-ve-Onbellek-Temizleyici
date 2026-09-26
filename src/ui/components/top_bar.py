import customtkinter as ctk
from typing import Callable, Optional
from src.i18n import t, get_language, get_category_name
from src.config import (
    CATEGORIES, COLOR_CARD_BG, COLOR_CARD_BORDER, COLOR_PRIMARY, 
    COLOR_PRIMARY_HOVER, COLOR_ACCENT, COLOR_TEXT_MAIN, 
    COLOR_TEXT_MUTED, COLOR_TEXT_DIM
)

class TopBarComponent(ctk.CTkFrame):
    """Ana içerik alanı için modern başlık, istatistik kartları ve filtre çubuğu."""

    def __init__(
        self,
        parent,
        on_category_change: Optional[Callable[[str], None]] = None,
        on_search_change: Optional[Callable[[str], None]] = None,
        on_select_all: Optional[Callable[[], None]] = None,
        on_deselect_all: Optional[Callable[[], None]] = None
    ):
        super().__init__(parent, fg_color="transparent")
        self.on_category_change = on_category_change
        self.on_search_change = on_search_change
        self.on_select_all = on_select_all
        self.on_deselect_all = on_deselect_all

        self.active_category = "all"
        self.category_buttons: dict[str, ctk.CTkButton] = {}

        self.setup_ui()

    def setup_ui(self):
        # 1. Header Row (Title & Subtitle)
        header_row = ctk.CTkFrame(self, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, 10))

        text_box = ctk.CTkFrame(header_row, fg_color="transparent")
        text_box.pack(side="left", fill="both", expand=True)

        self.title_lbl = ctk.CTkLabel(
            text_box,
            text=t("cache_view_title"),
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        self.title_lbl.pack(anchor="w")

        self.subtitle_lbl = ctk.CTkLabel(
            text_box,
            text=t("cache_view_desc"),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXT_MUTED
        )
        self.subtitle_lbl.pack(anchor="w", pady=(2, 0))

        # 2. Metric Stat Cards Row (Summary Dashboard)
        self.stats_row = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_row.pack(fill="x", pady=(0, 10))

        # Card 1: Total Detected
        self.card_total = self._create_stat_card(
            self.stats_row,
            icon="📊",
            title=t("stat_card_total_detected"),
            value="0 B",
            color=COLOR_ACCENT
        )
        self.card_total.pack(side="left", fill="both", expand=True, padx=(0, 6))

        # Card 2: Selected to Clean
        self.card_selected = self._create_stat_card(
            self.stats_row,
            icon="🎯",
            title=t("stat_card_selected_clean"),
            value="0 B",
            color=COLOR_PRIMARY
        )
        self.card_selected.pack(side="left", fill="both", expand=True, padx=(0, 6))

        # Card 3: Safety status
        self.card_safety = self._create_stat_card(
            self.stats_row,
            icon="🛡️",
            title=t("stat_card_safety_title"),
            value=t("stat_card_safety_val"),
            color="#34d399"
        )
        self.card_safety.pack(side="left", fill="both", expand=True)

        # 3. Filter and Search Bar Row
        self.cat_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.cat_bar.pack(fill="x", pady=(0, 4))

        # Category Buttons (Left)
        cat_frame = ctk.CTkFrame(self.cat_bar, fg_color="transparent")
        cat_frame.pack(side="left")

        for cat_key in CATEGORIES.keys():
            btn = ctk.CTkButton(
                cat_frame,
                text=get_category_name(cat_key),
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold" if cat_key == "all" else "normal"),
                fg_color=COLOR_PRIMARY if cat_key == "all" else "#141c2c",
                hover_color="#059669" if cat_key == "all" else "#1e2c44",
                border_width=1,
                border_color=COLOR_PRIMARY if cat_key == "all" else COLOR_CARD_BORDER,
                height=30,
                corner_radius=6,
                command=lambda k=cat_key: self.set_category(k)
            )
            btn.pack(side="left", padx=(0, 6))
            self.category_buttons[cat_key] = btn

        # Right Action & Search Box
        actions_box = ctk.CTkFrame(self.cat_bar, fg_color="transparent")
        actions_box.pack(side="right")

        # Search Input
        self.search_entry = ctk.CTkEntry(
            actions_box,
            placeholder_text=t("search_placeholder"),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            width=140,
            height=30,
            fg_color="#121824",
            border_color=COLOR_CARD_BORDER,
            corner_radius=6
        )
        self.search_entry.pack(side="left", padx=(0, 8))
        self.search_entry.bind("<KeyRelease>", self._handle_search)

        # Select All Button
        self.sel_all_btn = ctk.CTkButton(
            actions_box,
            text=t("btn_select_all"),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color="#141c2c",
            hover_color="#1e2c44",
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            width=88,
            height=30,
            corner_radius=6,
            command=self.on_select_all
        )
        self.sel_all_btn.pack(side="left", padx=(0, 6))

        # Deselect Button
        self.desel_all_btn = ctk.CTkButton(
            actions_box,
            text=t("btn_deselect_all"),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color="#141c2c",
            hover_color="#1e2c44",
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            width=88,
            height=30,
            corner_radius=6,
            command=self.on_deselect_all
        )
        self.desel_all_btn.pack(side="left")

    def _create_stat_card(self, parent, icon: str, title: str, value: str, color: str):
        card = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=8,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            height=58
        )
        card.pack_propagate(False)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=12, pady=6)

        # Icon box
        ic_lbl = ctk.CTkLabel(inner, text=icon, font=ctk.CTkFont(size=18))
        ic_lbl.pack(side="left", padx=(0, 10))

        tb = ctk.CTkFrame(inner, fg_color="transparent")
        tb.pack(side="left", fill="both", expand=True)

        t_lbl = ctk.CTkLabel(
            tb,
            text=title,
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=COLOR_TEXT_MUTED
        )
        t_lbl.pack(anchor="w")

        v_lbl = ctk.CTkLabel(
            tb,
            text=value,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=color
        )
        v_lbl.pack(anchor="w")

        card.title_label = t_lbl
        card.value_label = v_lbl
        return card

    def update_labels(self, current_tab: str = "cache"):
        tab_titles = {
            "cache": (t("cache_view_title"), t("cache_view_desc"), True),
            "projects": (t("project_view_title"), t("project_view_desc"), False),
            "large_files": (t("large_files_view_title"), t("large_files_view_desc"), False),
            "duplicates": (t("duplicate_view_title"), t("duplicate_view_desc"), False),
            "startup": (t("startup_view_title"), t("startup_view_desc"), False),
            "settings": (t("settings_view_title"), t("settings_view_desc"), False),
        }

        info = tab_titles.get(current_tab, (t("cache_view_title"), t("cache_view_desc"), True))
        self.set_view_title(info[0], info[1], info[2])

        # Update stat card titles
        self.card_total.title_label.configure(text=t("stat_card_total_detected"))
        self.card_selected.title_label.configure(text=t("stat_card_selected_clean"))
        self.card_safety.title_label.configure(text=t("stat_card_safety_title"))
        self.card_safety.value_label.configure(text=t("stat_card_safety_val"))

        # Update categories
        for cat_key, btn in self.category_buttons.items():
            btn.configure(text=get_category_name(cat_key))

        # Update buttons & search
        self.search_entry.configure(placeholder_text=t("search_placeholder"))
        self.sel_all_btn.configure(text=t("btn_select_all"))
        self.desel_all_btn.configure(text=t("btn_deselect_all"))

    def _handle_search(self, event=None):
        if self.on_search_change:
            query = self.search_entry.get().strip().lower()
            self.on_search_change(query)

    def set_category(self, key: str):
        self.active_category = key
        for cat_key, btn in self.category_buttons.items():
            if cat_key == key:
                btn.configure(
                    fg_color=COLOR_PRIMARY,
                    hover_color=COLOR_PRIMARY_HOVER,
                    border_color=COLOR_PRIMARY,
                    font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")
                )
            else:
                btn.configure(
                    fg_color="#141c2c",
                    hover_color="#1e2c44",
                    border_color=COLOR_CARD_BORDER,
                    font=ctk.CTkFont(family="Segoe UI", size=11, weight="normal")
                )

        if self.on_category_change:
            self.on_category_change(key)

    def set_view_title(self, title: str, subtitle: str, show_categories: bool = True):
        self.title_lbl.configure(text=title)
        self.subtitle_lbl.configure(text=subtitle)
        if show_categories:
            self.stats_row.pack(fill="x", pady=(0, 10))
            self.cat_bar.pack(fill="x", pady=(0, 4))
        else:
            self.stats_row.pack_forget()
            self.cat_bar.pack_forget()

    def update_stats(self, total_detected_str: str, selected_str: str, safety_str: str = None):
        self.card_total.value_label.configure(text=total_detected_str)
        self.card_selected.value_label.configure(text=selected_str)
        if safety_str:
            self.card_safety.value_label.configure(text=safety_str)
