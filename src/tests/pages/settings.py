from __future__ import annotations

import sys
from dataclasses import dataclass, asdict
from typing import Dict, Any

from PySide6.QtCore import Qt, QSettings, QTimer
from PySide6.QtGui import QIntValidator, QDoubleValidator, QIcon
from PySide6.QtWidgets import (QApplication,QCheckBox,QComboBox,QDialog,QDialogButtonBox,QFormLayout,
    QGridLayout,QGroupBox,QHBoxLayout,QLabel,QLineEdit,QMessageBox,QPushButton,QSpinBox,QTabWidget,
    QVBoxLayout,QWidget,QFileDialog,
)


# ------------------------------
# Data model for settings (defaults)
# ------------------------------
@dataclass
class AppSettings:
    # General / Business
    store_name: str = "My Store"
    logo_path: str = ""
    contact_phone: str = ""
    addres: str = ""

    # Finance / Installments
    currency: str = "USD"
    default_frequency: str = "Monthly"  # Weekly, Biweekly, Monthly
    installment_fee: float = 15    # installment presantage fee

    # Inventory
    low_stock_alerts: bool = True
    low_stock_threshold: int = 5
    barcode_enabled: bool = False

    # Reports / Dashboard
    default_report_period: str = "Monthly"  # Daily, Weekly, Monthly
    show_outstanding_metric: bool = True
    show_sales_trend: bool = True

    # Security
    auto_lock_minutes: int = 10
    require_pin_for_refunds: bool = True

    # Notifications
    notify_upcoming_due: bool = True
    notify_low_stock: bool = True

    # Backup / Data
    auto_backup_daily: bool = True
    backup_dir: str = ""

    # UI / App
    language: str = "English"
    theme: str = "System"  # Light, Dark, System
    date_format: str = "DD/MM/YYYY"
    startup_page: str = "Dashboard"  # Dashboard, Sales, Inventory, Reports


# ------------------------------
# Settings dialog
# ------------------------------
class SettingsPage(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(720, 560)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self._restart_required = False

        self.settings = QSettings("YourCompany", "YourApp")
        self.model = self._load_settings()

        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_general_tab(), "General")
        self.tabs.addTab(self._build_finance_tab(), "Finance")
        self.tabs.addTab(self._build_inventory_tab(), "Inventory")
        self.tabs.addTab(self._build_reports_tab(), "Reports")
        self.tabs.addTab(self._build_security_tab(), "Security")
        self.tabs.addTab(self._build_notifications_tab(), "Notifications")
        self.tabs.addTab(self._build_backup_tab(), "Backup & Data")
        self.tabs.addTab(self._build_ui_tab(), "UI & App")

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.RestoreDefaults
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply
            | QDialogButtonBox.StandardButton.Ok
        )
        self.buttons.clicked.connect(self._on_buttons)

        root = QVBoxLayout(self)
        root.addWidget(self.tabs)
        root.addWidget(self.buttons)

        # keyboard shortcuts (simple)
        self.buttons.button(QDialogButtonBox.StandardButton.Ok).setShortcut("Ctrl+Return")
        self.buttons.button(QDialogButtonBox.StandardButton.Apply).setShortcut("Ctrl+S")

    # --------------------------
    # Tabs
    # --------------------------
    def _build_general_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.store_name = QLineEdit(self.model.store_name)
        self.logo_path = QLineEdit(self.model.logo_path)
        browse_logo = QPushButton("Browse…")
        browse_logo.clicked.connect(self._choose_logo)
        logo_row = QHBoxLayout()
        logo_row.addWidget(self.logo_path)
        logo_row.addWidget(browse_logo)

        self.contact_phone = QLineEdit(self.model.contact_phone)
        self.addres = QLineEdit(self.model.addres)

        form.addRow("Store name", self.store_name)
        form.addRow("Logo path", self._hwrap(logo_row))
        form.addRow("Contact phone", self.contact_phone)
        form.addRow("Address", self.addres)
        return w

    def _build_finance_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.currency = QComboBox()
        self.currency.addItems(["USD", "EUR", "DZD"])  # add your region
        self.currency.setCurrentText(self.model.currency)
        self.currency.currentTextChanged.connect(self._mark_restart_required)

        self.default_frequency = QComboBox()
        self.default_frequency.addItems(["Weekly", "Biweekly", "Monthly"]) 
        self.default_frequency.setCurrentText(self.model.default_frequency)

        self.installment_fee = QLineEdit(str(self.model.installment_fee))
        self.installment_fee.setValidator(QDoubleValidator(0.0, 1_000_000.0, 2, self))

        form.addRow("Currency", self.currency)
        form.addRow("Default frequency", self.default_frequency)
        form.addRow("installment percentage", self.installment_fee)
        return w

    def _build_inventory_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.low_stock_alerts = QCheckBox()
        self.low_stock_alerts.setChecked(self.model.low_stock_alerts)

        self.low_stock_threshold = QSpinBox()
        self.low_stock_threshold.setRange(0, 100000)
        self.low_stock_threshold.setValue(self.model.low_stock_threshold)

        self.barcode_enabled = QCheckBox()
        self.barcode_enabled.setChecked(self.model.barcode_enabled)

        form.addRow("Low-stock alerts", self.low_stock_alerts)
        form.addRow("Low-stock threshold", self.low_stock_threshold)
        form.addRow("Enable barcode scanning", self.barcode_enabled)
        return w

    def _build_reports_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.report_period = QComboBox()
        self.report_period.addItems(["Daily", "Weekly", "Monthly"]) 
        self.report_period.setCurrentText(self.model.default_report_period)

        self.show_outstanding = QCheckBox()
        self.show_outstanding.setChecked(self.model.show_outstanding_metric)

        self.show_sales_trend = QCheckBox()
        self.show_sales_trend.setChecked(self.model.show_sales_trend)

        form.addRow("Default report period", self.report_period)
        form.addRow("Show Outstanding metric", self.show_outstanding)
        form.addRow("Show Sales Trend graph", self.show_sales_trend)
        return w

    def _build_security_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.auto_lock = QSpinBox()
        self.auto_lock.setRange(0, 120)
        self.auto_lock.setValue(self.model.auto_lock_minutes)

        self.pin_for_refunds = QCheckBox()
        self.pin_for_refunds.setChecked(self.model.require_pin_for_refunds)

        form.addRow("Auto-lock after (minutes)", self.auto_lock)
        form.addRow("Require PIN for refunds", self.pin_for_refunds)
        return w

    def _build_notifications_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.notify_upcoming = QCheckBox()
        self.notify_upcoming.setChecked(self.model.notify_upcoming_due)

        self.notify_lowstock = QCheckBox()
        self.notify_lowstock.setChecked(self.model.notify_low_stock)

        form.addRow("Upcoming installment reminders", self.notify_upcoming)
        form.addRow("Low-stock notifications", self.notify_lowstock)
        return w

    def _build_backup_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.auto_backup = QCheckBox()
        self.auto_backup.setChecked(self.model.auto_backup_daily)

        self.backup_dir = QLineEdit(self.model.backup_dir)
        choose_dir = QPushButton("Choose folder…")
        choose_dir.clicked.connect(self._choose_backup_dir)
        row = QHBoxLayout()
        row.addWidget(self.backup_dir)
        row.addWidget(choose_dir)

        form.addRow("Daily auto-backup", self.auto_backup)
        form.addRow("Backup directory", self._hwrap(row))
        return w

    def _build_ui_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.language = QComboBox()
        self.language.addItems(["English", "Français", "العربية"])
        self.language.setCurrentText(self.model.language)
        self.language.currentTextChanged.connect(self._mark_restart_required)

        self.theme = QComboBox()
        self.theme.addItems(["Light", "Dark", "System"]) 
        self.theme.setCurrentText(self.model.theme)

        self.date_format = QComboBox()
        self.date_format.addItems(["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"]) 
        self.date_format.setCurrentText(self.model.date_format)
        self.date_format.currentTextChanged.connect(self._mark_restart_required)

        self.startup_page = QComboBox()
        self.startup_page.addItems(["Dashboard", "Sales", "Inventory", "Reports"]) 
        self.startup_page.setCurrentText(self.model.startup_page)

        form.addRow("Language", self.language)
        form.addRow("Theme", self.theme)
        form.addRow("Date format", self.date_format)
        form.addRow("Startup page", self.startup_page)
        return w

    # --------------------------
    # Helpers
    # --------------------------
    def _hwrap(self, layout: QHBoxLayout) -> QWidget:
        w = QWidget()
        w.setLayout(layout)
        return w

    def _choose_logo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose logo", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.logo_path.setText(path)

    def _choose_backup_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Choose backup directory")
        if path:
            self.backup_dir.setText(path)

    def _mark_restart_required(self, *_):
        if not self._restart_required:
            self._restart_required = True

    # --------------------------
    # Persistence
    # --------------------------
    def _load_settings(self) -> AppSettings:
        s = AppSettings()
        sdict = asdict(s)
        for key in sdict.keys():
            if self.settings.contains(key):
                value = self.settings.value(key, sdict[key])
                # type adapt
                if isinstance(sdict[key], bool):
                    value = bool(str(value).lower() in ("1", "true", "yes"))
                elif isinstance(sdict[key], int):
                    try:
                        value = int(value)
                    except Exception:
                        pass
                elif isinstance(sdict[key], float):
                    try:
                        value = float(value)
                    except Exception:
                        pass
                setattr(s, key, value)
        return s

    def _collect(self) -> AppSettings:
        return AppSettings(
            # General
            store_name=self.store_name.text(),
            logo_path=self.logo_path.text(),
            contact_phone=self.contact_phone.text(),
            addres=self.addres.text(),
            # Finance
            currency=self.currency.currentText(),
            default_frequency=self.default_frequency.currentText(),
            installment_fee=float(self.installment_fee.text() or 0),
            # Inventory
            low_stock_alerts=self.low_stock_alerts.isChecked(),
            low_stock_threshold=self.low_stock_threshold.value(),
            barcode_enabled=self.barcode_enabled.isChecked(),
            # Reports
            default_report_period=self.report_period.currentText(),
            show_outstanding_metric=self.show_outstanding.isChecked(),
            show_sales_trend=self.show_sales_trend.isChecked(),
            # Security
            auto_lock_minutes=self.auto_lock.value(),
            require_pin_for_refunds=self.pin_for_refunds.isChecked(),
            # Notifications
            notify_upcoming_due=self.notify_upcoming.isChecked(),
            notify_low_stock=self.notify_lowstock.isChecked(),
            # Backup
            auto_backup_daily=self.auto_backup.isChecked(),
            backup_dir=self.backup_dir.text(),
            # UI
            language=self.language.currentText(),
            theme=self.theme.currentText(),
            date_format=self.date_format.currentText(),
            startup_page=self.startup_page.currentText(),
        )

    def _save(self, s: AppSettings):
        for k, v in asdict(s).items():
            self.settings.setValue(k, v)
        self.settings.sync()

    def _restore_defaults(self):
        confirm = QMessageBox.question(
            self,
            "Restore defaults",
            "Reset all settings to their default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.settings.clear()
            self.model = AppSettings()  # reset
            self._rebuild_from_model()
            self._restart_required = True

    def _rebuild_from_model(self):
        # Apply model back to widgets (used after restore)
        self.store_name.setText(self.model.store_name)
        self.logo_path.setText(self.model.logo_path)
        self.contact_phone.setText(self.model.contact_phone)
        self.addres.setText(self.model.addres)

        self.currency.setCurrentText(self.model.currency)
        self.default_frequency.setCurrentText(self.model.default_frequency)
        self.installment_fee.setText(str(self.model.installment_fee))

        self.low_stock_alerts.setChecked(self.model.low_stock_alerts)
        self.low_stock_threshold.setValue(self.model.low_stock_threshold)
        self.barcode_enabled.setChecked(self.model.barcode_enabled)

        self.report_period.setCurrentText(self.model.default_report_period)
        self.show_outstanding.setChecked(self.model.show_outstanding_metric)
        self.show_sales_trend.setChecked(self.model.show_sales_trend)

        self.auto_lock.setValue(self.model.auto_lock_minutes)
        self.pin_for_refunds.setChecked(self.model.require_pin_for_refunds)

        self.notify_upcoming.setChecked(self.model.notify_upcoming_due)
        self.notify_lowstock.setChecked(self.model.notify_low_stock)

        self.auto_backup.setChecked(self.model.auto_backup_daily)
        self.backup_dir.setText(self.model.backup_dir)

        self.language.setCurrentText(self.model.language)
        self.theme.setCurrentText(self.model.theme)
        self.date_format.setCurrentText(self.model.date_format)
        self.startup_page.setCurrentText(self.model.startup_page)

    # --------------------------
    # Button handling
    # --------------------------
    def _on_buttons(self, button):
        role = self.buttons.buttonRole(button)
        if role == QDialogButtonBox.ButtonRole.AcceptRole:  # OK
            self._apply()
            self.accept()
        elif role == QDialogButtonBox.ButtonRole.ApplyRole:  # Apply
            self._apply()
        elif role == QDialogButtonBox.ButtonRole.RejectRole:  # Cancel
            self.reject()
        elif role == QDialogButtonBox.ButtonRole.ResetRole:  # Restore defaults
            self._restore_defaults()

    def _apply(self):
        new_model = self._collect()
        self._save(new_model)
        self.model = new_model

        if self._restart_required:
            QMessageBox.information(
                self,
                "Restart required",
                "Some changes (language/date format/currency) may require restarting the app to fully apply.",
            )
            self._restart_required = False


# ------------------------------
# Demo launcher
# ------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("YourCompany")
    app.setApplicationName("YourApp")

    dlg = SettingsPage()
    if dlg.exec() == QDialog.DialogCode.Accepted:
        print("Settings saved:")
        print(asdict(dlg.model))
    sys.exit(0) 