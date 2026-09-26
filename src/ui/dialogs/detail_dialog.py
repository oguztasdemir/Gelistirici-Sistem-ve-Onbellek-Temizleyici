import customtkinter as ctk
from typing import Callable, Optional
from src.core.scanner import ScanResult, TargetDetailItem
from src.utils.formatters import format_bytes
from src.utils.system_helper import open_folder_in_explorer
from src.config import (
    COLOR_BG_DARK, COLOR_CARD_BG, COLOR_CARD_BORDER, 
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_ACCENT, 
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED
)

class TargetDetailDialog(ctk.CTkToplevel):
    """
    Belirli bir önbellek hedefinin içindeki alt klasör ve dosyaları listeleyen,
    kullanıcının silinmesini istemediği öğeleri hariç tutmasına olanak tanıyan modal pencere.
    """

    def __init__(
        self, 
        parent, 
        scan_result: ScanResult, 
        excluded_paths: set[str],
        on_update_callback: Optional[Callable[[str, set[str]], None]] = None
    ):
        super().__init__(parent)
        self.parent = parent
        self.scan_result = scan_result
        self.excluded_paths = excluded_paths.copy()
        self.on_update_callback = on_update_callback
        
        self.title(f"🔍 Detaylı İnceleme: {scan_result.name}")
        self.geometry("760x580")
        self.minsize(680, 480)
        self.configure(fg_color=COLOR_BG_DARK)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self.item_checkboxes: dict[str, ctk.CTkCheckBox] = {}
        self.item_vars: dict[str, ctk.BooleanVar] = {}
        self.all_items = scan_result.detail_items.copy()
        self.filtered_items = self.all_items.copy()
        
        self.setup_ui()
        self.populate_items()

    def setup_ui(self):
        # 1. Header Frame
        header = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=0, height=80)
        header.pack(fill="x", side="top")
        
        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left", padx=20, pady=15)
        
        title = ctk.CTkLabel(
            title_box,
            text=f"📂 {self.scan_result.name}",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        title.pack(anchor="w")
        
        count_text = f"Toplam {len(self.all_items)} öğe ({self.scan_result.formatted_size})"
        subtitle = ctk.CTkLabel(
            title_box,
            text=count_text,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXT_MUTED
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # Explorer Button in Header
        if self.scan_result.valid_paths:
            primary_path = self.scan_result.valid_paths[0]
            explorer_btn = ctk.CTkButton(
                header,
                text="📂 Gezginde Aç",
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                fg_color="#334155",
                hover_color="#475569",
                width=120,
                height=32,
                command=lambda: open_folder_in_explorer(primary_path)
            )
            explorer_btn.pack(side="right", padx=20, pady=20)

        # 2. Filter & Bulk Action Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=20, pady=(15, 10))

        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="🔎 Dosya veya klasör ara...",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=34,
            fg_color=COLOR_CARD_BG,
            border_color=COLOR_CARD_BORDER
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        select_all_btn = ctk.CTkButton(
            toolbar,
            text="Tümünü Seç",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color="#334155",
            hover_color="#475569",
            width=90,
            height=34,
            command=self.select_all_items
        )
        select_all_btn.pack(side="left", padx=(0, 6))

        deselect_all_btn = ctk.CTkButton(
            toolbar,
            text="Seçimi Kaldır",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color="#334155",
            hover_color="#475569",
            width=90,
            height=34,
            command=self.deselect_all_items
        )
        deselect_all_btn.pack(side="left")

        # 3. Scrollable List of Items
        self.scroll_area = ctk.CTkScrollableFrame(
            self,
            fg_color=COLOR_BG_DARK,
            border_width=1,
            border_color=COLOR_CARD_BORDER
        )
        self.scroll_area.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # 4. Footer Bar
        footer = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, height=60, corner_radius=0)
        footer.pack(fill="x", side="bottom")

        self.info_label = ctk.CTkLabel(
            footer,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COLOR_TEXT_MUTED
        )
        self.info_label.pack(side="left", padx=20)

        save_btn = ctk.CTkButton(
            footer,
            text="💾 Tercihleri Kaydet ve Kapat",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            width=200,
            height=36,
            command=self.save_and_close
        )
        save_btn.pack(side="right", padx=20, pady=12)

    def on_search_change(self, event=None):
        query = self.search_entry.get().strip().lower()
        if not query:
            self.filtered_items = self.all_items.copy()
        else:
            self.filtered_items = [
                item for item in self.all_items 
                if query in item.name.lower() or query in item.path.lower()
            ]
        self.populate_items()

    def populate_items(self):
        # Clear existing widgets
        for widget in self.scroll_area.winfo_children():
            widget.destroy()

        if not self.filtered_items:
            empty_lbl = ctk.CTkLabel(
                self.scroll_area,
                text="Bu dizinde listelenecek alt öğe bulunamadı.",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=COLOR_TEXT_MUTED
            )
            empty_lbl.pack(pady=40)
            self.update_summary_info()
            return

        for item in self.filtered_items:
            # Container card
            item_frame = ctk.CTkFrame(
                self.scroll_area,
                fg_color=COLOR_CARD_BG,
                corner_radius=6,
                border_width=1,
                border_color=COLOR_CARD_BORDER,
                height=48
            )
            item_frame.pack(fill="x", pady=3, padx=2)
            item_frame.pack_propagate(False)

            # Checkbox state: True if NOT in excluded_paths
            is_included = item.path not in self.excluded_paths
            var = ctk.BooleanVar(value=is_included)
            self.item_vars[item.path] = var

            icon = "📁" if item.is_dir else "📄"
            chk = ctk.CTkCheckBox(
                item_frame,
                text=f"{icon} {item.name}",
                variable=var,
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=COLOR_TEXT_MAIN,
                checkbox_width=18,
                checkbox_height=18,
                corner_radius=4,
                command=lambda p=item.path, v=var: self.on_item_toggle(p, v)
            )
            chk.pack(side="left", padx=12, pady=12)

            # Open folder button for subfolder
            if item.is_dir:
                open_btn = ctk.CTkButton(
                    item_frame,
                    text="📂",
                    width=28,
                    height=28,
                    fg_color="transparent",
                    hover_color="#334155",
                    command=lambda p=item.path: open_folder_in_explorer(p)
                )
                open_btn.pack(side="right", padx=(0, 10))

            # Size badge
            size_badge = ctk.CTkLabel(
                item_frame,
                text=item.formatted_size,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=COLOR_ACCENT,
                fg_color="#0f172a",
                corner_radius=4,
                width=85,
                height=24
            )
            size_badge.pack(side="right", padx=10)

        self.update_summary_info()

    def on_item_toggle(self, path: str, var: ctk.BooleanVar):
        if var.get():
            self.excluded_paths.discard(path)
        else:
            self.excluded_paths.add(path)
        self.update_summary_info()

    def select_all_items(self):
        for item in self.filtered_items:
            self.excluded_paths.discard(item.path)
            if item.path in self.item_vars:
                self.item_vars[item.path].set(True)
        self.update_summary_info()

    def deselect_all_items(self):
        for item in self.filtered_items:
            self.excluded_paths.add(item.path)
            if item.path in self.item_vars:
                self.item_vars[item.path].set(False)
        self.update_summary_info()

    def update_summary_info(self):
        selected_count = sum(1 for item in self.all_items if item.path not in self.excluded_paths)
        selected_bytes = sum(item.size_bytes for item in self.all_items if item.path not in self.excluded_paths)
        self.info_label.configure(
            text=f"Silinecek: {selected_count}/{len(self.all_items)} öğe ({format_bytes(selected_bytes)})"
        )

    def save_and_close(self):
        if self.on_update_callback:
            self.on_update_callback(self.scan_result.key, self.excluded_paths)
        self.grab_release()
        self.destroy()
