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
    QListWidgetItem, QFrame,
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
        self.tabs.addTab(self._build_inventory_management_tab(), "Inventory Management")

        # Buttons (same as SettingsPage)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.RestoreDefaults
            | QDialogButtonBox.Cancel
            | QDialogButtonBox.Ok
        )
        #self.buttons.clicked.connect(self._on_buttons)

        # Root layout
        root = QVBoxLayout(self)
        root.addWidget(self.tabs)
        root.addWidget(self.buttons)

        # Shortcuts (same idea as SettingsPage)
        self.buttons.button(QDialogButtonBox.Ok).setShortcut("Ctrl+Return")

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
        self.details = QLineEdit()
        self.details.setPlaceholderText("Type and press Enter to add more")
        
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
    
    # --------------------------
    # Tab: Inventory Management
    # --------------------------
    def _build_inventory_management_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)
        layout = QVBoxLayout(w)

        # brands
        form.addRow(QLabel("Brands:"))
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        form.addRow(line)


        # add brand button
        self.new_brand = QLineEdit()
        self.add_brand_btn = QPushButton("Add New Brand")

        # delete brand button
        self.brand = QComboBox()
        self.brand.addItems([""])
        self.delete_brand_btn = QPushButton("Delete Selected Brand")

        # layout       
        form.addRow("add new brand", self.new_brand)
        form.addRow(self.add_brand_btn)
        form.addRow("select brand to delete", self.brand)
        form.addRow(self.delete_brand_btn)
        form.addRow(line)

        # categories
        form.addRow(QLabel("Categories:"))
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        form.addRow(line)

        # add category button
        self.new_category = QLineEdit()
        self.add_category_btn = QPushButton("Add New Category")

        # delete category button
        self.category = QComboBox()
        self.category.addItems([""])
        self.delete_category_btn = QPushButton("Delete Selected Category")

        # layout
        form.addRow("add new category", self.new_category)
        form.addRow(self.add_category_btn)
        form.addRow("select category to delete", self.category)
        form.addRow(self.delete_category_btn)
        form.addRow(line)


        # tags
        form.addRow(QLabel("Tags:"))
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        form.addRow(line)

        # add tag button
        self.new_tag = QLineEdit()
        self.add_tag_btn = QPushButton("Add New Tag")

        # delete tag button
        self.tag = QComboBox()
        self.tag.addItems([""])
        self.delete_tag_btn = QPushButton("Delete Selected Tag")

        # layout       
        form.addRow("add new tag", self.new_tag)
        form.addRow(self.add_tag_btn)
        form.addRow("select tag to delete", self.tag)
        form.addRow(self.delete_tag_btn)
        form.addRow(line)

        return w


# ------------------------------
# Demo launcher
# ------------------------------
if __name__ == "__main__":
    app = QApplication([])
    inventory_page = InventoryPage()
    inventory_page.show()
    app.exec()