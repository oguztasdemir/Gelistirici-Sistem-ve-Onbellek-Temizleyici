import customtkinter as ctk
from typing import Callable, Optional
from src.config import (
    COLOR_CARD_BG, COLOR_CARD_BORDER, COLOR_PRIMARY, 
    COLOR_ACCENT, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_TEXT_DIM
)
from src.i18n import t, get_target_info_i18n
from src.core.scanner import ScanResult
from src.utils.system_helper import open_folder_in_explorer

class TargetCardComponent(ctk.CTkFrame):
    """Her bir önbellek hedefi için modern, anlaşılır ve çoklu dil destekli kart bileşeni."""

    def __init__(
        self,
        parent,
        key: str,
        info: dict,
        initial_checked: bool = True,
        on_toggle: Optional[Callable[[str, bool], None]] = None,
        on_open_detail: Optional[Callable[[str], None]] = None
    ):
        super().__init__(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=8,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            height=60
        )
        self.pack_propagate(False)

        self.key = key
        self.info = info
        self.on_toggle = on_toggle
        self.on_open_detail = on_open_detail
        self.scan_result: Optional[ScanResult] = None

        self.check_var = ctk.BooleanVar(value=initial_checked)
        self.setup_ui()

    def setup_ui(self):
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=12, pady=6)

        # 1. Left container: Checkbox + Icon + Title + Description
        left_box = ctk.CTkFrame(inner, fg_color="transparent")
        left_box.pack(side="left", fill="both", expand=True)

        # Checkbox
        self.checkbox = ctk.CTkCheckBox(
            left_box,
            text="",
            variable=self.check_var,
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=4,
            border_width=2,
            border_color="#334155",
            fg_color=COLOR_PRIMARY,
            hover_color="#059669",
            command=self._handle_toggle,
            width=24
        )
        self.checkbox.pack(side="left", padx=(0, 6))

        # Icon Avatar Badge
        icon = self.info.get("icon", "📦")
        icon_box = ctk.CTkFrame(
            left_box,
            width=32,
            height=32,
            corner_radius=6,
            fg_color="#182334"
        )
        icon_box.pack_propagate(False)
        icon_box.pack(side="left", padx=(0, 10))

        ic_lbl = ctk.CTkLabel(icon_box, text=icon, font=ctk.CTkFont(size=14))
        ic_lbl.pack(expand=True)

        # Text Info (Title & Description)
        text_box = ctk.CTkFrame(left_box, fg_color="transparent")
        text_box.pack(side="left", fill="both", expand=True)

        name_i18n, desc_i18n = get_target_info_i18n(self.key)
        if not name_i18n:
            name_i18n = self.info.get("name", self.key)
        if not desc_i18n:
            desc_i18n = self.info.get("desc", "")

        # Title line
        self.title_lbl = ctk.CTkLabel(
            text_box,
            text=name_i18n,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        self.title_lbl.pack(anchor="w")

        # Description line
        self.desc_label = ctk.CTkLabel(
            text_box,
            text=desc_i18n,
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=COLOR_TEXT_MUTED
        )
        self.desc_label.pack(anchor="w", pady=(1, 0))

        # 2. Right container: Safety Pill + Size Badge + Action Buttons
        right_box = ctk.CTkFrame(inner, fg_color="transparent")
        right_box.pack(side="right")

        # Safety badge
        is_safe = self.info.get("danger_level", "safe") == "safe"
        self.safety_badge = ctk.CTkLabel(
            right_box,
            text=t("badge_safe") if is_safe else t("badge_warning"),
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#34d399" if is_safe else "#fbbf24",
            fg_color="#064e3b" if is_safe else "#78350f",
            corner_radius=6,
            height=26,
            padx=8
        )
        self.safety_badge.pack(side="left", padx=(0, 8))

        # Size badge
        self.size_badge = ctk.CTkLabel(
            right_box,
            text="0 B",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=COLOR_TEXT_DIM,
            fg_color="#090d16",
            corner_radius=6,
            width=90,
            height=28
        )
        self.size_badge.pack(side="left", padx=(0, 8))

        # Detail button
        self.detail_btn = ctk.CTkButton(
            right_box,
            text=t("btn_detail"),
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            fg_color="#182334",
            hover_color="#24344d",
            border_width=1,
            border_color="#2a3a52",
            width=70,
            height=28,
            corner_radius=6,
            command=self._handle_open_detail
        )
        self.detail_btn.pack(side="left", padx=(0, 6))

        # Explorer folder button
        self.explorer_btn = ctk.CTkButton(
            right_box,
            text="📂",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color="#182334",
            hover_color="#24344d",
            border_width=1,
            border_color="#2a3a52",
            width=32,
            height=28,
            corner_radius=6,
            command=self._handle_open_explorer
        )
        self.explorer_btn.pack(side="left")

    def update_labels(self):
        name_i18n, desc_i18n = get_target_info_i18n(self.key)
        if not name_i18n:
            name_i18n = self.info.get("name", self.key)
        if not desc_i18n:
            desc_i18n = self.info.get("desc", "")

        self.title_lbl.configure(text=name_i18n)
        self.desc_label.configure(text=desc_i18n)

        is_safe = self.info.get("danger_level", "safe") == "safe"
        self.safety_badge.configure(text=t("badge_safe") if is_safe else t("badge_warning"))

        if self.scan_result and self.scan_result.detail_items:
            self.detail_btn.configure(text=t("btn_detail_count", count=len(self.scan_result.detail_items)))
        else:
            self.detail_btn.configure(text=t("btn_detail"))

    def _handle_toggle(self):
        if self.on_toggle:
            self.on_toggle(self.key, self.check_var.get())

    def _handle_open_detail(self):
        if self.on_open_detail:
            self.on_open_detail(self.key)

    def _handle_open_explorer(self):
        if self.scan_result and self.scan_result.valid_paths:
            open_folder_in_explorer(self.scan_result.valid_paths[0])
        else:
            paths = self.info.get("paths", [])
            for p in paths:
                if open_folder_in_explorer(p):
                    break

    def update_result(self, result: ScanResult):
        self.scan_result = result
        self.size_badge.configure(text=result.formatted_size)

        if not result.is_available or result.total_bytes == 0:
            self.size_badge.configure(text_color=COLOR_TEXT_DIM, fg_color="#090d16")
            self.detail_btn.configure(state="disabled")
            self.explorer_btn.configure(state="disabled")
        else:
            self.size_badge.configure(text_color=COLOR_PRIMARY, fg_color="#064e3b33")
            if result.detail_items:
                self.detail_btn.configure(
                    state="normal", 
                    text=t("btn_detail_count", count=len(result.detail_items))
                )
            else:
                self.detail_btn.configure(state="disabled", text=t("btn_detail"))
            
            if result.valid_paths:
                self.explorer_btn.configure(state="normal")
            else:
                self.explorer_btn.configure(state="disabled")

    def set_checked(self, checked: bool):
        self.check_var.set(checked)

    def is_checked(self) -> bool:
        return self.check_var.get()
