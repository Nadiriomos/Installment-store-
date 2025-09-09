from __future__ import annotations

import os
import sys
from dataclasses import asdict
from typing import Any

from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import (
    QApplication, QDialog, QDialogButtonBox, QTabWidget, QVBoxLayout, QWidget
)

# --- your imports (keep as-is if these paths are correct) ---
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))  # points to .../src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from tests.pages.settings_tabs.settings_model import AppSettings
from tests.pages.settings_tabs.general_tab import GeneralTab
from tests.pages.settings_tabs.finance_tab import FinanceTab
from tests.pages.settings_tabs.inventory_tab import InventoryTab
from tests.pages.settings_tabs.notifications_tab import NotificationsTab
from tests.pages.settings_tabs.security_tab import SecurityTab
from tests.pages.settings_tabs.ui_tab import UITab
from tests.pages.settings_tabs.backup_tab import BackupTab
# Optional: if you have it
# from tests.pages.settings_tabs.reports_tab import ReportsTab


class SettingsPage(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(720, 560)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        # QSettings (set org/app in your main before showing this dialog)
        self.settings = QSettings("YourCompany", "YourApp")

        # Load model once and share it across all tabs
        self.model = self._load_settings()

        # Tabs
        self.tabs = QTabWidget()
        self.general_tab = GeneralTab(self.model)
        self.inventory_tab = InventoryTab(self.model)
        self.finance_tab = FinanceTab(self.model)
        self.notifications_tab = NotificationsTab(self.model)
        self.security_tab = SecurityTab(self.model)
        self.ui_tab = UITab(self.model)
        self.backup_tab = BackupTab(self.model)
        # self.reports_tab = ReportsTab(self.model)  # if you have it

        self.tabs.addTab(self.general_tab, "General")
        self.tabs.addTab(self.inventory_tab, "Inventory")
        self.tabs.addTab(self.finance_tab, "Finance")
        self.tabs.addTab(self.notifications_tab, "Notifications")
        self.tabs.addTab(self.security_tab, "Security")
        self.tabs.addTab(self.ui_tab, "UI & App")
        self.tabs.addTab(self.backup_tab, "Backup & Data")
        # self.tabs.addTab(self.reports_tab, "Reports")

        # Buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttons.clicked.connect(self._on_buttons)
        self.buttons.button(QDialogButtonBox.Ok).setShortcut("Ctrl+Return")

        # Root layout
        root = QVBoxLayout(self)
        root.addWidget(self.tabs)
        root.addWidget(self.buttons)

    # ---------- Persistence ----------
    def _load_settings(self) -> AppSettings:
        """
        Read values from QSettings into an AppSettings instance,
        keeping types consistent with defaults.
        """
        m = AppSettings()
        defaults = asdict(m)
        for key, default in defaults.items():
            if self.settings.contains(key):
                val: Any = self.settings.value(key, default)
                # type adapt to the default's type
                if isinstance(default, bool):
                    val = str(val).lower() in ("1", "true", "yes")
                elif isinstance(default, int):
                    try: val = int(val)
                    except: val = default
                elif isinstance(default, float):
                    try: val = float(val)
                    except: val = default
                setattr(m, key, val)
        return m

    def _save_settings(self, m: AppSettings) -> None:
        for k, v in asdict(m).items():
            self.settings.setValue(k, v)
        self.settings.sync()

    # ---------- Gather from tabs ----------
    def _collect(self) -> AppSettings:
        """
        Ask each tab to write its current UI values into a copy of the model,
        then return it.
        """
        merged = AppSettings(**asdict(self.model))  # copy
        merged = self.general_tab.collect(merged)
        merged = self.inventory_tab.collect(merged)
        merged = self.finance_tab.collect(merged)
        merged = self.notifications_tab.collect(merged)
        merged = self.security_tab.collect(merged)
        merged = self.ui_tab.collect(merged)
        merged = self.backup_tab.collect(merged)
        # merged = self.reports_tab.collect(merged)  # if present
        return merged

    def _apply_model_to_tabs(self) -> None:
        """
        Push the current model values back into each tab (useful if you add
        Restore Defaults later or reloading).
        """
        self.general_tab.apply_model(self.model)
        self.inventory_tab.apply_model(self.model)
        self.finance_tab.apply_model(self.model)
        self.notifications_tab.apply_model(self.model)
        self.security_tab.apply_model(self.model)
        self.ui_tab.apply_model(self.model)
        self.backup_tab.apply_model(self.model)
        # self.reports_tab.apply_model(self.model)

    # ---------- Buttons ----------
    def _on_buttons(self, button):
        role = self.buttons.buttonRole(button)
        if role == QDialogButtonBox.AcceptRole:  # OK
            new_model = self._collect()
            self._save_settings(new_model)
            self.model = new_model
            self.accept()
        elif role == QDialogButtonBox.RejectRole:  # Cancel
            self.reject()


# ---------- Demo launcher ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("YourCompany")
    app.setApplicationName("YourApp")

    dlg = SettingsPage()
    dlg.show()
    sys.exit(app.exec())
