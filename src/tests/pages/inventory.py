from __future__ import annotations

import os
import sys
import json
import hashlib
import secrets
import webbrowser
import urllib.parse
from dataclasses import dataclass, asdict
from typing import List, Dict, Any


from PySide6.QtCore import Qt, QSettings, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QApplication,QCheckBox,QComboBox,QDialog,QDialogButtonBox,QFormLayout,QHBoxLayout,
    QHeaderView,QHeaderView,QInputDialog,QLineEdit,QMessageBox,QPushButton,QTextEdit,
    QPushButton,QSpinBox,QTabWidget,QTableView,QVBoxLayout,
    QWidget,QFileDialog,QLabel,QDoubleSpinBox, QFrame
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from tests.pages.inventory_tabs.new_product import NewProductTab
from tests.pages.inventory_tabs.inventory_management import InventoryManagementTab
from tests.pages.inventory_tabs.Supplier_Management import SupplierManagementTab
# ------------------------------
# Inventory page (QDialog)
# ------------------------------
class InventoryPage(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Inventory")
        self.setMinimumSize(720, 560)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(NewProductTab(), "New Product")
        self.tabs.addTab(InventoryManagementTab(), "Inventory Management")
        self.tabs.addTab(SupplierManagementTab(), "Suppliers Management")

        # Buttons (same as SettingsPage)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Cancel
            | QDialogButtonBox.Ok
        )
        #self.buttons.clicked.connect(self._on_buttons)

        # Root layout
        root = QVBoxLayout(self)
        root.addWidget(self.tabs)
        root.addWidget(self.buttons)

        # Shortcuts (same idea as SettingsPage)
        self.buttons.button(QDialogButtonBox.Ok).setShortcut("Ctrl+Return")

# ------------------------------
# Demo launcher
# ------------------------------
if __name__ == "__main__":
    app = QApplication([])
    inventory_page = InventoryPage()
    inventory_page.show()
    app.exec()