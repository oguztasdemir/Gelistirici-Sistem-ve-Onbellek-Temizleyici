import os
import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk

from src.i18n import t
from src.core.settings import settings
from src.core.project_cleaner import ProjectCleanerEngine, ProjectJunkItem
from src.utils.formatters import format_bytes
from src.utils.system_helper import open_folder_in_explorer
from src.config import (
    COLOR_BG_DARK, COLOR_CARD_BG, COLOR_CARD_BORDER,
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_ACCENT,
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_DANGER
)

class ProjectCleanerView(ctk.CTkFrame):
    """Yazılım projelerindeki bağımlılık ve önbellek kalıntılarını temizleme görünümü."""

    def __init__(self, parent, on_log_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.on_log = on_log_callback
        self.engine = ProjectCleanerEngine()
        self.found_items: list[ProjectJunkItem] = []
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
            text=t("project_cleaner_title"),
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        title.pack(anchor="w")

        desc = ctk.CTkLabel(
            top_info,
            text=t("project_cleaner_desc"),
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
        self.path_entry.insert(0, settings.get_last_project_dir())

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

        self.scan_btn = ctk.CTkButton(
            picker_row,
            text=t("btn_scan_projects"),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            width=130,
            height=34,
            command=self.start_scan
        )
        self.scan_btn.pack(side="left")

        # 2. Toolbar (Summary & Bulk Actions)
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 8))

        self.summary_label = ctk.CTkLabel(
            toolbar,
            text=t("project_item_count", count=0, size="0.00 B"),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        self.summary_label.pack(side="left")

        # Right actions
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

        self.clean_btn = ctk.CTkButton(
            actions_box,
            text=t("btn_clean_projects"),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=COLOR_DANGER,
            hover_color="#dc2626",
            height=28,
            command=self.start_clean
        )
        self.clean_btn.pack(side="left")

        # 3. Scrollable List of Found Projects
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
            settings.set_last_project_dir(chosen)

    def start_scan(self):
        if self.is_scanning:
            return

        target_dir = self.path_entry.get().strip()
        if not os.path.exists(target_dir):
            messagebox.showwarning(t("dialog_warning_title"), "Geçerli bir dizin seçiniz.")
            return

        settings.set_last_project_dir(target_dir)
        self.is_scanning = True
        self.scan_btn.configure(state="disabled")
        self.clean_btn.configure(state="disabled")
        self.summary_label.configure(text=t("status_scanning"))

        if self.on_log:
            self.on_log(f"🔍 Proje bağımlılıkları taranıyor: {target_dir}")

        threading.Thread(target=self._scan_worker, args=(target_dir,), daemon=True).start()

    def _scan_worker(self, target_dir: str):
        items = self.engine.scan_directory(target_dir)
        self.after(0, lambda: self._on_scan_completed(items))

    def _on_scan_completed(self, items: list[ProjectJunkItem]):
        self.found_items = items
        self.is_scanning = False
        self.scan_btn.configure(state="normal")
        self.clean_btn.configure(state="normal")
        self.populate_items()

        total_bytes = sum(item.size_bytes for item in items)
        if self.on_log:
            self.on_log(f"✅ Proje taraması tamamlandı. {len(items)} öğe ({format_bytes(total_bytes)}) bulundu.")

    def populate_items(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        self.item_vars.clear()

        if not self.found_items:
            empty_lbl = ctk.CTkLabel(
                self.scroll_frame,
                text="Bu dizinde herhangi bir proje bağımlılığı veya kalıntısı bulunamadı.",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=COLOR_TEXT_MUTED
            )
            empty_lbl.pack(pady=40)
            self.update_summary()
            return

        for item in self.found_items:
            card = ctk.CTkFrame(
                self.scroll_frame,
                fg_color=COLOR_CARD_BG,
                corner_radius=6,
                border_width=1,
                border_color=COLOR_CARD_BORDER,
                height=56
            )
            card.pack(fill="x", pady=3, padx=2)
            card.pack_propagate(False)

            var = ctk.BooleanVar(value=item.is_selected)
            self.item_vars[item.path] = var

            # Left side: Checkbox & Name
            left_box = ctk.CTkFrame(card, fg_color="transparent")
            left_box.pack(side="left", fill="both", expand=True, padx=12, pady=6)

            title_text = f"📁 [{item.project_name}]  {item.junk_type_title}"
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

            # Right side: Date, Explorer & Size Badge
            right_box = ctk.CTkFrame(card, fg_color="transparent")
            right_box.pack(side="right", padx=10)

            date_lbl = ctk.CTkLabel(
                right_box,
                text=item.formatted_date,
                font=ctk.CTkFont(family="Segoe UI", size=10),
                text_color=COLOR_TEXT_MUTED
            )
            date_lbl.pack(side="left", padx=(0, 10))

            exp_btn = ctk.CTkButton(
                right_box,
                text="📂",
                width=28,
                height=28,
                fg_color="transparent",
                hover_color="#334155",
                command=lambda p=item.path: open_folder_in_explorer(p)
            )
            exp_btn.pack(side="left", padx=(0, 8))

            size_badge = ctk.CTkLabel(
                right_box,
                text=item.formatted_size,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=COLOR_ACCENT,
                fg_color="#0f172a",
                corner_radius=4,
                width=90,
                height=26
            )
            size_badge.pack(side="right")

        self.update_summary()

    def _on_item_toggle(self, path: str, var: ctk.BooleanVar):
        for item in self.found_items:
            if item.path == path:
                item.is_selected = var.get()
                break
        self.update_summary()

    def select_all(self):
        for item in self.found_items:
            item.is_selected = True
            if item.path in self.item_vars:
                self.item_vars[item.path].set(True)
        self.update_summary()

    def deselect_all(self):
        for item in self.found_items:
            item.is_selected = False
            if item.path in self.item_vars:
                self.item_vars[item.path].set(False)
        self.update_summary()

    def update_summary(self):
        selected = [item for item in self.found_items if item.is_selected]
        selected_bytes = sum(item.size_bytes for item in selected)
        self.summary_label.configure(
            text=f"Seçilen: {len(selected)}/{len(self.found_items)} öğe ({format_bytes(selected_bytes)})"
        )

    def start_clean(self):
        selected = [item for item in self.found_items if item.is_selected]
        if not selected:
            messagebox.showinfo(t("dialog_warning_title"), "Lütfen silinecek en az bir proje klasörü seçin.")
            return

        tot_bytes = sum(item.size_bytes for item in selected)
        msg = t("confirm_project_clean", count=len(selected), size=format_bytes(tot_bytes))
        confirm = messagebox.askyesno(t("dialog_confirm_title"), msg)
        if not confirm:
            return

        self.scan_btn.configure(state="disabled")
        self.clean_btn.configure(state="disabled")

        threading.Thread(target=self._clean_worker, args=(selected,), daemon=True).start()

    def _clean_worker(self, selected: list[ProjectJunkItem]):
        def log_cb(m):
            if self.on_log:
                self.after(0, lambda msg=m: self.on_log(msg))

        freed, count = self.engine.clean_selected(selected, log_callback=log_cb)
        settings.record_clean_session(freed)
        self.after(0, lambda: self._on_clean_completed(freed, count))

    def _on_clean_completed(self, freed: int, count: int):
        self.scan_btn.configure(state="normal")
        self.clean_btn.configure(state="normal")
        messagebox.showinfo(t("dialog_success_title"), f"🎉 {count} adet proje bağımlılığı temizlendi.\nKurtarılan Alan: {format_bytes(freed)}")
        self.start_scan()
