import os
import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk

from src.i18n import t
from src.core.duplicate_finder import DuplicateFinderEngine, DuplicateFileGroup
from src.utils.formatters import format_bytes
from src.utils.system_helper import open_folder_in_explorer
from src.config import (
    COLOR_BG_DARK, COLOR_CARD_BG, COLOR_CARD_BORDER,
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_ACCENT,
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_DANGER
)

class DuplicateFinderView(ctk.CTkFrame):
    """Kopya ve yinelenen dosyaları bularak disk alanı kazandıran görünüm."""

    def __init__(self, parent, on_log_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.on_log = on_log_callback
        self.engine = DuplicateFinderEngine()
        self.found_groups: list[DuplicateFileGroup] = []
        self.is_scanning = False
        self.selected_files: set[str] = set()

        self.setup_ui()

    def setup_ui(self):
        # 1. Header Box
        header_box = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=8, border_width=1, border_color=COLOR_CARD_BORDER)
        header_box.pack(fill="x", pady=(0, 10), padx=2)

        top_info = ctk.CTkFrame(header_box, fg_color="transparent")
        top_info.pack(fill="x", padx=16, pady=(12, 8))

        title = ctk.CTkLabel(
            top_info,
            text="👯‍♂️ Kopya Dosya Bulucu (Duplicate Finder)",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        title.pack(anchor="w")

        desc = ctk.CTkLabel(
            top_info,
            text="Farklı klasörlerde birden fazla kopyası bulunan birebir aynı dosyaları (MD5 hash) tespit edip silin.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXT_MUTED
        )
        desc.pack(anchor="w", pady=(2, 0))

        # Path Picker Row
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
        self.path_entry.insert(0, os.path.join(os.path.expanduser("~"), "Downloads"))

        browse_btn = ctk.CTkButton(
            picker_row,
            text="📁 Klasör Seç",
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
            text="🔍 Kopyaları Ara",
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
            text="0 kopya grup bulundu",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        self.summary_label.pack(side="left")

        self.delete_btn = ctk.CTkButton(
            toolbar,
            text="🗑️ Seçili Kopyaları Sil",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=COLOR_DANGER,
            hover_color="#dc2626",
            height=28,
            command=self.start_delete
        )
        self.delete_btn.pack(side="right")

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
            messagebox.showwarning("Uyarı", "Geçerli bir dizin seçiniz.")
            return

        self.is_scanning = True
        self.scan_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
        self.summary_label.configure(text="Kopyalar aranıyor...")

        if self.on_log:
            self.on_log(f"🔍 Kopya dosyalar taranıyor: {target_dir}")

        threading.Thread(target=self._scan_worker, args=(target_dir,), daemon=True).start()

    def _scan_worker(self, target_dir: str):
        groups = self.engine.scan_duplicates(target_dir)
        self.after(0, lambda: self._on_scan_completed(groups))

    def _on_scan_completed(self, groups: list[DuplicateFileGroup]):
        self.found_groups = groups
        self.is_scanning = False
        self.scan_btn.configure(state="normal")
        self.delete_btn.configure(state="normal")
        self.populate_items()

        total_wasted = sum(g.size_bytes * (len(g.files) - 1) for g in groups)
        if self.on_log:
            self.on_log(f"✅ Kopya taraması bitti. {len(groups)} kopya grup ({format_bytes(total_wasted)} israf) bulundu.")

    def populate_items(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        self.selected_files.clear()

        if not self.found_groups:
            lbl = ctk.CTkLabel(
                self.scroll_frame,
                text="Bu dizinde herhangi bir kopya dosya bulunamadı.",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=COLOR_TEXT_MUTED
            )
            lbl.pack(pady=40)
            self.summary_label.configure(text="0 kopya grup bulundu")
            return

        total_wasted = sum(g.size_bytes * (len(g.files) - 1) for g in self.found_groups)
        self.summary_label.configure(
            text=f"Toplam {len(self.found_groups)} kopya grup bulundu ({format_bytes(total_wasted)} israf)"
        )

        for group in self.found_groups:
            card = ctk.CTkFrame(
                self.scroll_frame,
                fg_color=COLOR_CARD_BG,
                corner_radius=6,
                border_width=1,
                border_color=COLOR_CARD_BORDER
            )
            card.pack(fill="x", pady=4, padx=2)

            # Group header
            gh = ctk.CTkFrame(card, fg_color="transparent")
            gh.pack(fill="x", padx=12, pady=(8, 4))

            fname = os.path.basename(group.files[0])
            g_title = ctk.CTkLabel(
                gh,
                text=f"📄 {fname}  ({len(group.files)} kopya - {group.formatted_size} adet)",
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=COLOR_PRIMARY
            )
            g_title.pack(side="left")

            wasted_badge = ctk.CTkLabel(
                gh,
                text=f"Kurtarılabilir: {group.wasted_size}",
                font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                text_color=COLOR_ACCENT,
                fg_color="#0f172a",
                corner_radius=4,
                padx=8,
                height=22
            )
            wasted_badge.pack(side="right")

            # Files list (First file is original, rest are auto-checked copies)
            for idx, p in enumerate(group.files):
                frow = ctk.CTkFrame(card, fg_color="transparent")
                frow.pack(fill="x", padx=12, pady=2)

                is_copy = (idx > 0)
                if is_copy:
                    self.selected_files.add(p)

                var = ctk.BooleanVar(value=is_copy)

                tag = "[ORİJİNAL] " if idx == 0 else "[KOPYA] "
                chk = ctk.CTkCheckBox(
                    frow,
                    text=f"{tag}{p}",
                    variable=var,
                    font=ctk.CTkFont(family="Segoe UI", size=10),
                    text_color=COLOR_TEXT_MAIN if not is_copy else "#cbd5e1",
                    checkbox_width=16,
                    checkbox_height=16,
                    corner_radius=3,
                    command=lambda path=p, v=var: self._on_toggle(path, v)
                )
                chk.pack(side="left")

                exp_btn = ctk.CTkButton(
                    frow,
                    text="📂",
                    width=24,
                    height=22,
                    fg_color="transparent",
                    hover_color="#334155",
                    command=lambda path=os.path.dirname(p): open_folder_in_explorer(path)
                )
                exp_btn.pack(side="right")

    def _on_toggle(self, path: str, var: ctk.BooleanVar):
        if var.get():
            self.selected_files.add(path)
        else:
            self.selected_files.discard(path)

    def start_delete(self):
        if not self.selected_files:
            messagebox.showinfo("Uyarı", "Lütfen silinecek en az bir kopya dosya seçin.")
            return

        confirm = messagebox.askyesno(
            "Onay",
            f"Seçilen {len(self.selected_files)} adet kopya dosya kalıcı olarak silinecektir.\nDevam etmek istiyor musunuz?"
        )
        if not confirm:
            return

        deleted = 0
        freed = 0
        for p in list(self.selected_files):
            try:
                if os.path.exists(p):
                    sz = os.path.getsize(p)
                    os.remove(p)
                    freed += sz
                    deleted += 1
            except Exception:
                pass

        messagebox.showinfo("Başarılı", f"🎉 {deleted} adet kopya dosya silindi.\nKurtarılan Alan: {format_bytes(freed)}")
        self.start_scan()
