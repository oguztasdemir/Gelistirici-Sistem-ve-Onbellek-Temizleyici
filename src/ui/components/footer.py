import customtkinter as ctk
from typing import Callable, Optional
from src.i18n import t
from src.config import (
    COLOR_CARD_BG, COLOR_PRIMARY, COLOR_PRIMARY_HOVER, 
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_CARD_BORDER
)

class FooterComponent(ctk.CTkFrame):
    """Modern alt kontrol alanı: İlerleme göstergesi, canlı durum ve temizleme butonları."""

    def __init__(
        self,
        parent,
        on_scan_clicked: Optional[Callable[[], None]] = None,
        on_clean_clicked: Optional[Callable[[], None]] = None,
        on_toggle_logs: Optional[Callable[[], None]] = None
    ):
        super().__init__(
            parent,
            fg_color=COLOR_CARD_BG,
            corner_radius=8,
            border_width=1,
            border_color=COLOR_CARD_BORDER
        )
        self.on_scan_clicked = on_scan_clicked
        self.on_clean_clicked = on_clean_clicked
        self.on_toggle_logs = on_toggle_logs

        self.setup_ui()

    def setup_ui(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="x", padx=16, pady=10)

        # Progress bar (top of footer)
        self.progress_bar = ctk.CTkProgressBar(
            main_container,
            height=4,
            progress_color=COLOR_PRIMARY,
            fg_color="#090d16",
            corner_radius=2
        )
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.set(0)

        # Bottom Action Controls Row
        ctrl_row = ctk.CTkFrame(main_container, fg_color="transparent")
        ctrl_row.pack(fill="x")

        # Left side: Status text & Log toggle
        left_box = ctk.CTkFrame(ctrl_row, fg_color="transparent")
        left_box.pack(side="left", fill="both", expand=True)

        self.status_label = ctk.CTkLabel(
            left_box,
            text=f"● {t('status_ready')}",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        self.status_label.pack(anchor="w")

        self.log_toggle_btn = ctk.CTkButton(
            left_box,
            text=t("btn_toggle_logs"),
            font=ctk.CTkFont(family="Segoe UI", size=10),
            fg_color="transparent",
            hover_color="#182334",
            text_color=COLOR_TEXT_MUTED,
            height=22,
            corner_radius=4,
            command=self.on_toggle_logs
        )
        self.log_toggle_btn.pack(anchor="w", pady=(2, 0))

        # Right side: Action Buttons
        right_box = ctk.CTkFrame(ctrl_row, fg_color="transparent")
        right_box.pack(side="right")

        self.scan_btn = ctk.CTkButton(
            right_box,
            text=t("btn_rescan"),
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#182334",
            hover_color="#24344d",
            border_width=1,
            border_color="#2a3a52",
            width=140,
            height=36,
            corner_radius=6,
            command=self.on_scan_clicked
        )
        self.scan_btn.pack(side="left", padx=(0, 8))

        self.clean_btn = ctk.CTkButton(
            right_box,
            text=t("btn_clean_selected"),
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color="#ffffff",
            width=230,
            height=36,
            corner_radius=6,
            command=self.on_clean_clicked
        )
        self.clean_btn.pack(side="left")

    def update_labels(self):
        self.log_toggle_btn.configure(text=t("btn_toggle_logs"))
        self.scan_btn.configure(text=t("btn_rescan"))

    def set_status(self, text: str, is_active: bool = False):
        bullet = "⏳ " if is_active else "● "
        self.status_label.configure(
            text=f"{bullet}{text}",
            text_color=COLOR_PRIMARY if not is_active else "#38bdf8"
        )

    def set_clean_button_text(self, text: str):
        self.clean_btn.configure(text=text)

    def set_progress(self, val: float):
        self.progress_bar.set(val)

    def start_indeterminate(self):
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

    def stop_indeterminate(self):
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")

    def set_buttons_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.scan_btn.configure(state=state)
        self.clean_btn.configure(state=state)
