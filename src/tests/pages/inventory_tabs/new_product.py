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

# ------------------------------
# New Product 
# ------------------------------
class NewProductTab(QDialog):
    def _build_new_product_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        form = QFormLayout()
        layout.addLayout(form)

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
