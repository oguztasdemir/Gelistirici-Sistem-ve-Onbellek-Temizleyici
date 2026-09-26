import threading
from tkinter import messagebox
import customtkinter as ctk

from src.i18n import t, get_language
from src.config import (
    APP_TITLE, DEFAULT_APPEARANCE, TARGETS,
    COLOR_BG_DARK, COLOR_CARD_BORDER
)
from src.core.settings import settings
from src.core.scanner import ScannerEngine, ScanResult
from src.core.cleaner import CleanerEngine
from src.ui.components.sidebar import SidebarComponent
from src.ui.components.top_bar import TopBarComponent
from src.ui.components.target_card import TargetCardComponent
from src.ui.components.log_panel import LogPanelComponent
from src.ui.components.footer import FooterComponent
from src.ui.components.project_cleaner_view import ProjectCleanerView
from src.ui.components.disk_analyzer_view import DiskAnalyzerView
from src.ui.components.duplicate_finder_view import DuplicateFinderView
from src.ui.components.startup_view import StartupManagerView
from src.ui.components.settings_view import SettingsView
from src.ui.dialogs.detail_dialog import TargetDetailDialog
from src.utils.formatters import format_bytes


class CacheCleanerApp(ctk.CTk):
    """Modern sol panelli, çok sekmeli ve profesyonel Önbellek & Disk Kurtarma Uygulaması."""

    def __init__(self):
        super().__init__()

        # Appearance setup
        ctk.set_appearance_mode(DEFAULT_APPEARANCE)
        ctk.set_default_color_theme("green")

        self.title(f"{t('app_title')} - {t('app_subtitle')}")
        self.geometry("1120x780")
        self.minsize(960, 660)
        self.configure(fg_color=COLOR_BG_DARK)

        # Core Engines
        self.scanner = ScannerEngine()
        self.cleaner = CleanerEngine()

        # State management
        self.current_tab = "cache"
        self.is_scanning = False
        self.is_cleaning = False
        self.selected_category = "all"
        self.search_query = ""
        self.show_logs = False
        self.scan_results: dict[str, ScanResult] = {}
        self.target_cards: dict[str, TargetCardComponent] = {}
        self.excluded_paths: set[str] = set()

        # Setup GUI structure
        self.setup_ui()

        # Start initial scan
        self.after(200, self.start_scan)

    def setup_ui(self):
        # 1. Left Sidebar Navigation (Sticky Left)
        self.sidebar = SidebarComponent(
            self,
            active_tab=self.current_tab,
            on_tab_select=self.on_tab_changed,
            on_language_change=self.on_language_changed
        )
        self.sidebar.pack(side="left", fill="y")

        # 2. Right Main Content Area
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.pack(side="right", fill="both", expand=True, padx=20, pady=16)

        # Top Bar (Title & Category Filters & Stat Cards)
        self.top_bar = TopBarComponent(
            self.main_area,
            on_category_change=self.on_category_changed,
            on_search_change=self.on_search_changed,
            on_select_all=self.select_all_targets,
            on_deselect_all=self.deselect_all_targets
        )
        self.top_bar.pack(fill="x", pady=(0, 10))

        # Content View Container
        self.view_container = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.view_container.pack(fill="both", expand=True)

        # -------------------------------------------------------------
        # View A: Cache View (Cards + Log + Bottom Footer)
        # -------------------------------------------------------------
        self.cache_view_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        self.cache_view_frame.pack(fill="both", expand=True)

        # Scrollable Target Cards Frame
        self.cards_scroll = ctk.CTkScrollableFrame(
            self.cache_view_frame,
            fg_color=COLOR_BG_DARK,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            corner_radius=8
        )
        self.cards_scroll.pack(fill="both", expand=True, pady=(0, 8))

        for key, info in TARGETS.items():
            card = TargetCardComponent(
                self.cards_scroll,
                key=key,
                info=info,
                initial_checked=True,
                on_toggle=self.on_card_toggled,
                on_open_detail=self.open_detail_dialog
            )
            card.pack(fill="x", pady=2, padx=2)
            self.target_cards[key] = card

        # Collapsible Log Panel (Initially hidden or minimal)
        self.log_panel = LogPanelComponent(self.cache_view_frame, height=95)
        # Hidden by default to provide clean card workspace

        # Footer Actions (Sticky Bottom)
        self.footer = FooterComponent(
            self.main_area,
            on_scan_clicked=self.start_scan,
            on_clean_clicked=self.start_clean,
            on_toggle_logs=self.toggle_logs_visibility
        )
        self.footer.pack(fill="x", side="bottom", pady=(8, 0))

        # -------------------------------------------------------------
        # Other Views (Initially Hidden)
        # -------------------------------------------------------------
        self.project_view = ProjectCleanerView(self.view_container, on_log_callback=self.log)
        self.disk_analyzer_view = DiskAnalyzerView(self.view_container, on_log_callback=self.log)
        self.duplicate_view = DuplicateFinderView(self.view_container, on_log_callback=self.log)
        self.startup_view = StartupManagerView(self.view_container)
        self.settings_view = SettingsView(self.view_container, on_language_changed_callback=self.on_language_changed)

    def log(self, text: str):
        self.log_panel.log(text)

    def toggle_logs_visibility(self):
        self.show_logs = not self.show_logs
        if self.show_logs:
            self.log_panel.pack(fill="x", side="bottom", pady=(4, 0))
        else:
            self.log_panel.pack_forget()

    def on_tab_changed(self, tab_key: str):
        self.current_tab = tab_key

        # Hide all view containers
        self.cache_view_frame.pack_forget()
        self.project_view.pack_forget()
        self.disk_analyzer_view.pack_forget()
        self.duplicate_view.pack_forget()
        self.startup_view.pack_forget()
        self.settings_view.pack_forget()
        self.footer.pack_forget()

        if tab_key == "cache":
            self.top_bar.set_view_title(
                title=t("cache_view_title"),
                subtitle=t("cache_view_desc"),
                show_categories=True
            )
            self.footer.pack(fill="x", side="bottom", pady=(8, 0))
            self.cache_view_frame.pack(fill="both", expand=True)
            self.update_total_summary()

        elif tab_key == "projects":
            self.top_bar.set_view_title(
                title=t("project_view_title"),
                subtitle=t("project_view_desc"),
                show_categories=False
            )
            self.project_view.pack(fill="both", expand=True)

        elif tab_key == "large_files":
            self.top_bar.set_view_title(
                title=t("large_files_view_title"),
                subtitle=t("large_files_view_desc"),
                show_categories=False
            )
            self.disk_analyzer_view.pack(fill="both", expand=True)

        elif tab_key == "duplicates":
            self.top_bar.set_view_title(
                title=t("duplicate_view_title"),
                subtitle=t("duplicate_view_desc"),
                show_categories=False
            )
            self.duplicate_view.pack(fill="both", expand=True)

        elif tab_key == "startup":
            self.top_bar.set_view_title(
                title=t("startup_view_title"),
                subtitle=t("startup_view_desc"),
                show_categories=False
            )
            self.startup_view.refresh_apps()
            self.startup_view.pack(fill="both", expand=True)

        elif tab_key == "settings":
            self.top_bar.set_view_title(
                title=t("settings_view_title"),
                subtitle=t("settings_view_desc"),
                show_categories=False
            )
            self.settings_view.refresh_stats()
            self.settings_view.pack(fill="both", expand=True)

    def on_language_changed(self, lang_code: str):
        self.title(f"{t('app_title')} - {t('app_subtitle')}")
        self.sidebar.update_labels()
        self.top_bar.update_labels(self.current_tab)
        self.footer.update_labels()
        for card in self.target_cards.values():
            card.update_labels()
        self.update_total_summary()

    def on_category_changed(self, category_key: str):
        self.selected_category = category_key
        self._filter_cards()

    def on_search_changed(self, query: str):
        self.search_query = query
        self._filter_cards()

    def _filter_cards(self):
        for key, card in self.target_cards.items():
            info = TARGETS[key]
            cat = info.get("category", "dev")
            name = info.get("name", "").lower()
            desc = info.get("desc", "").lower()

            matches_cat = (self.selected_category == "all" or cat == self.selected_category)
            matches_search = (not self.search_query or self.search_query in name or self.search_query in desc or self.search_query in key.lower())

            if matches_cat and matches_search:
                card.pack(fill="x", pady=2, padx=2)
            else:
                card.pack_forget()

    def on_card_toggled(self, key: str, is_checked: bool):
        self.update_total_summary()

    def select_all_targets(self):
        for key, card in self.target_cards.items():
            cat = TARGETS[key].get("category", "dev")
            if self.selected_category == "all" or cat == self.selected_category:
                card.set_checked(True)
        self.update_total_summary()

    def deselect_all_targets(self):
        for key, card in self.target_cards.items():
            cat = TARGETS[key].get("category", "dev")
            if self.selected_category == "all" or cat == self.selected_category:
                card.set_checked(False)
        self.update_total_summary()

    def open_detail_dialog(self, key: str):
        result = self.scan_results.get(key)
        if not result or not result.detail_items:
            messagebox.showinfo("Bilgi", "Bu hedef için görüntülenecek ayrıntılı dosya listesi bulunamadı.")
            return

        dialog = TargetDetailDialog(
            parent=self,
            scan_result=result,
            excluded_paths=self.excluded_paths,
            on_update_callback=self.on_detail_preferences_updated
        )

    def on_detail_preferences_updated(self, target_key: str, updated_exclusions: set[str]):
        self.excluded_paths = updated_exclusions
        excluded_count = len(self.excluded_paths)
        if excluded_count > 0:
            self.log(f"🛡️ {TARGETS[target_key]['name']} için {excluded_count} öğe korumaya alındı (silinmeyecek).")
        self.update_total_summary()

    def update_total_summary(self):
        total_detected_bytes = 0
        total_selected_bytes = 0

        for key, res in self.scan_results.items():
            if res.is_available and key not in ("dns", "conda", "docker_daemon", "recycle_bin"):
                total_detected_bytes += res.total_bytes

        selected_count = 0
        for key, card in self.target_cards.items():
            if card.is_checked() and key in self.scan_results:
                res = self.scan_results[key]
                if res.is_available and key not in ("dns", "conda", "docker_daemon", "recycle_bin"):
                    selected_count += 1
                    if res.detail_items:
                        item_bytes = sum(
                            item.size_bytes for item in res.detail_items 
                            if item.path not in self.excluded_paths and not settings.is_whitelisted(item.path)
                        )
                        total_selected_bytes += item_bytes
                    else:
                        total_selected_bytes += res.total_bytes

        total_str = format_bytes(total_detected_bytes)
        selected_str = format_bytes(total_selected_bytes)

        self.top_bar.update_stats(
            total_detected_str=f"{total_str} ({len(self.scan_results)} hedef)",
            selected_str=f"{selected_str} ({selected_count} seçili)"
        )

        btn_text = f"✨ Seçilenleri Güvenle Temizle ({selected_str})" if total_selected_bytes > 0 else "✨ Seçilenleri Güvenle Temizle"
        self.footer.set_clean_button_text(btn_text)

    def start_scan(self):
        if self.is_scanning or self.is_cleaning:
            return

        self.is_scanning = True
        self.footer.set_buttons_enabled(False)
        self.footer.start_indeterminate()
        self.footer.set_status(t("status_scanning"), is_active=True)
        self.log_panel.clear_logs()
        self.log(t("log_scan_started"))

        threading.Thread(target=self._scan_worker, daemon=True).start()

    def _scan_worker(self):
        def progress_cb(name, current, total):
            self.after(0, lambda n=name, c=current, t=total: self._on_scan_progress(n, c, t))

        def item_cb(key, result):
            self.after(0, lambda k=key, r=result: self._on_scan_item_done(k, r))

        results = self.scanner.scan_all(
            progress_callback=progress_cb,
            item_callback=item_cb
        )

        self.after(0, lambda r=results: self._on_scan_completed(r))

    def _on_scan_progress(self, name: str, current: int, total: int):
        self.footer.set_status(f"Taranıyor ({current}/{total}): {name}...", is_active=True)
        self.log(f"İnceleniyor: {name}...")

    def _on_scan_item_done(self, key: str, result: ScanResult):
        self.scan_results[key] = result
        if key in self.target_cards:
            self.target_cards[key].update_result(result)
        self.update_total_summary()

    def _on_scan_completed(self, results: dict[str, ScanResult]):
        self.scan_results = results
        self.is_scanning = False
        self.footer.stop_indeterminate()
        self.footer.set_progress(1.0)
        self.footer.set_buttons_enabled(True)
        self.footer.set_status("Tarama tamamlandı")

        self.update_total_summary()

        total_detected = sum(r.total_bytes for r in results.values() if r.is_available)
        self.log(t("log_scan_completed", size=format_bytes(total_detected)))

    def start_clean(self):
        if self.is_scanning or self.is_cleaning:
            return

        selected_keys = [
            k for k, card in self.target_cards.items() 
            if card.is_checked() and self.scan_results.get(k) and self.scan_results[k].is_available
        ]

        if not selected_keys:
            messagebox.showwarning(
                t("dialog_warning_title"),
                "Temizlenecek geçerli bir önbellek kaynağı seçilmedi.\nLütfen listeden en az bir öğe işaretleyin."
            )
            return

        approx_bytes = 0
        for k in selected_keys:
            res = self.scan_results.get(k)
            if res and res.is_available and k not in ("dns", "conda", "docker_daemon", "recycle_bin"):
                if res.detail_items:
                    approx_bytes += sum(
                        item.size_bytes for item in res.detail_items 
                        if item.path not in self.excluded_paths and not settings.is_whitelisted(item.path)
                    )
                else:
                    approx_bytes += res.total_bytes

        msg = (
            f"Seçilen {len(selected_keys)} adet önbellek kaynağı temizlenecektir.\n\n"
            f"Tahmini Geri Kazanılacak Alan: {format_bytes(approx_bytes)}\n"
            f"Korunan Özel Dosyalar: {len(self.excluded_paths)} öğe\n\n"
            f"Devam etmek ve seçilenleri güvenle silmek istiyor musunuz?"
        )

        confirm = messagebox.askyesno(t("dialog_confirm_title"), msg)
        if not confirm:
            return

        self.is_cleaning = True
        self.footer.set_buttons_enabled(False)
        self.footer.set_progress(0.0)
        self.footer.set_status(t("status_cleaning"), is_active=True)
        self.log("🧼 Güvenli temizleme işlemi başlatıldı...")

        threading.Thread(
            target=self._clean_worker,
            args=(selected_keys,),
            daemon=True
        ).start()

    def _clean_worker(self, selected_keys: list[str]):
        def progress_cb(name, current, total):
            self.after(0, lambda n=name, c=current, t=total: self._on_clean_progress(n, c, t))

        def log_cb(msg):
            self.after(0, lambda m=msg: self.log(m))

        clean_result = self.cleaner.clean_all(
            selected_keys=selected_keys,
            scan_results=self.scan_results,
            excluded_paths=self.excluded_paths,
            progress_callback=progress_cb,
            log_callback=log_cb
        )

        # Record lifetime statistics
        settings.record_clean_session(clean_result.freed_bytes)

        self.after(0, lambda res=clean_result: self._on_clean_completed(res))

    def _on_clean_progress(self, name: str, current: int, total: int):
        pct = current / total
        self.footer.set_progress(pct)
        self.footer.set_status(f"Temizleniyor ({current}/{total}): {name}...", is_active=True)

    def _on_clean_completed(self, result):
        self.is_cleaning = False
        self.footer.set_progress(1.0)
        self.footer.set_buttons_enabled(True)
        self.footer.set_status(t("status_clean_done"))

        summary_msg = (
            f"🎉 Temizlik Başarıyla Tamamlandı!\n\n"
            f"• Geri Kazanılan Net Alan: {result.formatted_freed}\n"
            f"• Silinen Öğe Sayısı: {result.deleted_items_count}\n"
            f"• Korunan/Kilitli Öğeler: {result.skipped_items_count}\n"
            f"• İşlem Süresi: {result.formatted_duration}"
        )

        self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        self.log(t("log_clean_completed", size=result.formatted_freed))
        self.log(f"⏱️ Süre: {result.formatted_duration} | Silinen: {result.deleted_items_count} | Atlanan: {result.skipped_items_count}")
        self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        messagebox.showinfo(t("dialog_success_title"), summary_msg)

        # Re-scan to update real-time statistics
        self.start_scan()
