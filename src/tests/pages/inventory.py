from __future__ import annotations

import os
import sys
import json
import hashlib
import secrets
from dataclasses import dataclass, asdict
from typing import List, Dict, Any


from PySide6.QtCore import Qt, QSettings, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTableView,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLabel,
    QAbstractItemView,
    QDoubleSpinBox,
    QTextEdit,
    QListWidget,
)

class Product:
    sku: str
    name_en: str
    brand: str = ""
    categories: List[str] = None
    sale_price: float = 0.0
    barcode: str = ""
    installment_allowed: bool = True
    track_serials: bool = False


# ------------------------------
# Inventory page (QDialog)
# ------------------------------
class InventoryPage(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Inventory")
        self.setMinimumSize(720, 560)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        # Persistence (same pattern as SettingsPage)
        # self.settings = QSettings("YourCompany", "YourApp")
        # self.products: List[Dict[str, Any]] = self._load_inventory()

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_new_product_tab(), "New Product")

        # Buttons (same as SettingsPage)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.RestoreDefaults
            | QDialogButtonBox.Cancel
            | QDialogButtonBox.Apply
            | QDialogButtonBox.Ok
        )
        #self.buttons.clicked.connect(self._on_buttons)

        # Root layout
        root = QVBoxLayout(self)
        root.addWidget(self.tabs)
        root.addWidget(self.buttons)

        # Shortcuts (same idea as SettingsPage)
        self.buttons.button(QDialogButtonBox.Ok).setShortcut("Ctrl+Return")
        self.buttons.button(QDialogButtonBox.Apply).setShortcut("Ctrl+S")

    # --------------------------
    # Tab: New Product
    # --------------------------
    def _build_new_product_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)
        layout = QVBoxLayout(w)

        # Minimal fields for a product

        self.name_en = QLineEdit()
        self.name_en.setPlaceholderText("Product name in English/French")
        # Keep it simple: start with a few brands. You can load from settings later.
        self.brand = QComboBox()
        self.brand.addItems([""])

        # Categories as a single line, comma-separated (keep minimal)
        self.categories = QLineEdit()
        self.categories.setPlaceholderText("e.g. Electronics, TV")

        # Details as multi-line text
        def _add_line(layout):
            line = QLineEdit()
            line.setPlaceholderText("Type and press Enter to add more")
            line.returnPressed.connect(lambda: _add_line(layout))
            layout.addWidget(line)
        
        self.details = QLineEdit()
        self.details.setPlaceholderText("Type and press Enter to add more")
        self.details.returnPressed.connect(lambda: _add_line(layout))

        layout.addWidget(self.details)


        # Sale price (>= 0)
        self.sale_price = QDoubleSpinBox()
        self.sale_price.setRange(0.0, 1_000_000_000.0)
        self.sale_price.setDecimals(2)

        # Optional fields
        self.barcode = QLineEdit()
        self.installment_allowed = QCheckBox("Installment allowed")
        self.installment_allowed.setChecked(True)


        # Layout
        form.addRow("Name (English) *", self.name_en)
        form.addRow("Brand", self.brand)
        form.addRow("Categories", self.categories)
        form.addRow("Details", self.details)
        form.addRow("Sale price *", self.sale_price)
        form.addRow("Barcode", self.barcode)
        form.addRow("", self.installment_allowed)

        return w

# ------------------------------
# Demo launcher
# ------------------------------
if __name__ == "__main__":
    app = QApplication([])
    inventory_page = InventoryPage()
    inventory_page.show()
    app.exec()