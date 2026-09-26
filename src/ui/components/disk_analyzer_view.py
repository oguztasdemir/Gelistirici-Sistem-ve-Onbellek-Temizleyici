import os
import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk

from src.i18n import t
from src.core.settings import settings
from src.core.large_files import LargeFileAnalyzerEngine, LargeFileInfo
from src.utils.formatters import format_bytes
from src.utils.system_helper import open_folder_in_explorer
from src.config import (
    COLOR_BG_DARK, COLOR_CARD_BG, COLOR_CARD_BORDER,
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_ACCENT,
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_DANGER
)

SIZE_FILTER_OPTIONS = {
    "50 MB": 50 * 1024 * 1024,
    "100 MB": 100 * 1024 * 1024,
    "250 MB": 250 * 1024 * 1024,
    "500 MB": 500 * 1024 * 1024,
    "1 GB": 1024 * 1024 * 1024,
    "2 GB": 2 * 1024 * 1024 * 1024
}

class DiskAnalyzerView(ctk.CTkFrame):
    """Diskteki büyük dosyaları tespit etme ve temizleme görünümü."""

    def __init__(self, parent, on_log_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.on_log = on_log_callback
        self.engine = LargeFileAnalyzerEngine()
        self.found_files: list[LargeFileInfo] = []
        self.is_scanning = False
        self.item_vars: dict[str, ctk.BooleanVar] = {}

        self.setup_ui()

    def setup_ui(self):
        # 1. Top Header Box
        header_box = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=8, border_width=1, border_color=COLOR_CARD_BORDER)
        header_box.pack(fill="x", pady=(0, 10), padx=2)

        top_info = ctk.CTkFrame(header_box, fg_color="transparent")
        top_info.pack(fill="x", padx=16, pady=(12, 8))

        title = ctk.CTkLabel(
            top_info,
            text=t("large_files_title"),
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=COLOR_ACCENT
        )
        title.pack(anchor="w")

        desc = ctk.CTkLabel(
            top_info,
            text=t("large_files_desc"),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXT_MUTED
        )
        desc.pack(anchor="w", pady=(2, 0))

        # Path picker line
        picker_row = ctk.CTkFrame(header_box, fg_color="transparent")
        picker_row.pack(fill="x", padx=16, pady=(0, 12))

        self.path_entry = ctk.CTkEntry(
            picker_row,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            height=34,
            fg_color=COLOR_BG_DARK,
            border_color=COLOR_CARD_BORDER
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.path_entry.insert(0, os.path.expanduser("~"))

        browse_btn = ctk.CTkButton(
            picker_row,
            text=t("btn_browse"),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color="#334155",
            hover_color="#475569",
            width=110,
            height=34,
            command=self.browse_directory
        )
        browse_btn.pack(side="left", padx=(0, 8))

        # Size threshold dropdown
        self.size_filter_combo = ctk.CTkComboBox(
            picker_row,
            values=list(SIZE_FILTER_OPTIONS.keys()),
            width=100,
            height=34,
            font=ctk.CTkFont(family="Segoe UI", size=11)
        )
        self.size_filter_combo.set("100 MB")
        self.size_filter_combo.pack(side="left", padx=(0, 8))

        self.scan_btn = ctk.CTkButton(
            picker_row,
            text=t("btn_scan_large_files"),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            width=130,
            height=34,
            command=self.start_scan
        )
        self.scan_btn.pack(side="left")

        # 2. Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 8))

        self.summary_label = ctk.CTkLabel(
            toolbar,
            text=t("large_files_found", count=0, size="0.00 B"),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        self.summary_label.pack(side="left")

        actions_box = ctk.CTkFrame(toolbar, fg_color="transparent")
        actions_box.pack(side="right")

        sel_all_btn = ctk.CTkButton(
            actions_box,
            text=t("select_all"),
            font=ctk.CTkFont(family="Segoe UI", size=10),
            fg_color="#1e293b",
            hover_color="#334155",
            border_width=1,
            border_color="#475569",
            width=80,
            height=28,
            command=self.select_all
        )
        sel_all_btn.pack(side="left", padx=(0, 6))

        desel_all_btn = ctk.CTkButton(
            actions_box,
            text=t("deselect_all"),
            font=ctk.CTkFont(family="Segoe UI", size=10),
            fg_color="#1e293b",
            hover_color="#334155",
            border_width=1,
            border_color="#475569",
            width=80,
            height=28,
            command=self.deselect_all
        )
        desel_all_btn.pack(side="left", padx=(0, 8))

        self.delete_btn = ctk.CTkButton(
            actions_box,
            text=t("btn_delete_large_files"),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=COLOR_DANGER,
            hover_color="#dc2626",
            height=28,
            command=self.start_delete
        )
        self.delete_btn.pack(side="left")

        # 3. Scrollable File List
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLOR_BG_DARK,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            corner_radius=8
        )
        self.scroll_frame.pack(fill="both", expand=True)

    def browse_directory(self):
        chosen = filedialog.askdirectory(initialdir=self.path_entry.get())
        if chosen:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, chosen)

    def start_scan(self):
        if self.is_scanning:
            return

        target_dir = self.path_entry.get().strip()
        if not os.path.exists(target_dir):
            messagebox.showwarning(t("dialog_warning_title"), "Geçerli bir dizin seçiniz.")
            return

        threshold_str = self.size_filter_combo.get()
        min_bytes = SIZE_FILTER_OPTIONS.get(threshold_str, 100 * 1024 * 1024)

        self.is_scanning = True
        self.scan_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
        self.summary_label.configure(text=t("status_scanning"))

        if self.on_log:
            self.on_log(f"🔍 Büyük dosyalar taranıyor ({threshold_str}+): {target_dir}")

        threading.Thread(
            target=self._scan_worker, 
            args=(target_dir, min_bytes), 
            daemon=True
        ).start()

    def _scan_worker(self, target_dir: str, min_bytes: int):
        files = self.engine.scan_large_files(target_dir, min_size_bytes=min_bytes)
        self.after(0, lambda: self._on_scan_completed(files))

    def _on_scan_completed(self, files: list[LargeFileInfo]):
        self.found_files = files
        self.is_scanning = False
        self.scan_btn.configure(state="normal")
        self.delete_btn.configure(state="normal")
        self.populate_items()

        total_bytes = sum(f.size_bytes for f in files)
        if self.on_log:
            self.on_log(f"✅ Büyük dosya taraması tamamlandı. {len(files)} dosya ({format_bytes(total_bytes)}) bulundu.")

    def populate_items(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        self.item_vars.clear()

        if not self.found_files:
            empty_lbl = ctk.CTkLabel(
                self.scroll_frame,
                text="Bu kriterlere uyan büyük dosya bulunamadı.",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=COLOR_TEXT_MUTED
            )
            empty_lbl.pack(pady=40)
            self.update_summary()
            return

        for item in self.found_files:
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

            var = ctk.BooleanVar(value=item.is_selected)
            self.item_vars[item.path] = var

            left_box = ctk.CTkFrame(card, fg_color="transparent")
            left_box.pack(side="left", fill="both", expand=True, padx=12, pady=6)

            title_text = f"[{item.category_label}]  {item.name}"
            chk = ctk.CTkCheckBox(
                left_box,
                text=title_text,
                variable=var,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=COLOR_TEXT_MAIN,
                checkbox_width=18,
                checkbox_height=18,
                corner_radius=4,
                command=lambda p=item.path, v=var: self._on_item_toggle(p, v)
            )
            chk.pack(anchor="w")

            path_lbl = ctk.CTkLabel(
                left_box,
                text=item.path,
                font=ctk.CTkFont(family="Segoe UI", size=9),
                text_color=COLOR_TEXT_MUTED
            )
            path_lbl.pack(anchor="w", padx=(26, 0))

            right_box = ctk.CTkFrame(card, fg_color="transparent")
            right_box.pack(side="right", padx=10)

            date_lbl = ctk.CTkLabel(
                right_box,
                text=item.formatted_date,
                font=ctk.CTkFont(family="Segoe UI", size=10),
                text_color=COLOR_TEXT_MUTED
            )
            date_lbl.pack(side="left", padx=(0, 10))

            parent_folder = os.path.dirname(item.path)
            exp_btn = ctk.CTkButton(
                right_box,
                text="📂",
                width=28,
                height=28,
                fg_color="transparent",
                hover_color="#334155",
                command=lambda p=parent_folder: open_folder_in_explorer(p)
            )
            exp_btn.pack(side="left", padx=(0, 8))

            size_badge = ctk.CTkLabel(
                right_box,
                text=item.formatted_size,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=COLOR_PRIMARY,
                fg_color="#0f172a",
                corner_radius=4,
                width=90,
                height=26
            )
            size_badge.pack(side="right")

        self.update_summary()

    def _on_item_toggle(self, path: str, var: ctk.BooleanVar):
        for item in self.found_files:
            if item.path == path:
                item.is_selected = var.get()
                break
        self.update_summary()

    def select_all(self):
        for item in self.found_files:
            item.is_selected = True
            if item.path in self.item_vars:
                self.item_vars[item.path].set(True)
        self.update_summary()

    def deselect_all(self):
        for item in self.found_files:
            item.is_selected = False
            if item.path in self.item_vars:
                self.item_vars[item.path].set(False)
        self.update_summary()

    def update_summary(self):
        selected = [f for f in self.found_files if f.is_selected]
        selected_bytes = sum(f.size_bytes for f in selected)
        self.summary_label.configure(
            text=f"Seçilen: {len(selected)}/{len(self.found_files)} dosya ({format_bytes(selected_bytes)})"
        )

    def start_delete(self):
        selected = [f for f in self.found_files if f.is_selected]
        if not selected:
            messagebox.showinfo(t("dialog_warning_title"), "Lütfen silinecek en az bir dosya seçin.")
            return

        tot_bytes = sum(f.size_bytes for f in selected)
        msg = t("confirm_large_file_delete", count=len(selected), size=format_bytes(tot_bytes))
        confirm = messagebox.askyesno(t("dialog_confirm_title"), msg)
        if not confirm:
            return

        self.scan_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")

        threading.Thread(target=self._delete_worker, args=(selected,), daemon=True).start()

    def _delete_worker(self, selected: list[LargeFileInfo]):
        def log_cb(m):
            if self.on_log:
                self.after(0, lambda msg=m: self.on_log(msg))

        freed, count = self.engine.delete_selected(selected, log_callback=log_cb)
        settings.record_clean_session(freed)
        self.after(0, lambda: self._on_delete_completed(freed, count))

    def _on_delete_completed(self, freed: int, count: int):
        self.scan_btn.configure(state="normal")
        self.delete_btn.configure(state="normal")
        messagebox.showinfo(t("dialog_success_title"), f"🎉 {count} adet büyük dosya silindi.\nKurtarılan Alan: {format_bytes(freed)}")
        self.start_scan()
