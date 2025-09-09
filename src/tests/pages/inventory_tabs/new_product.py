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
class NewProductTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        form = QFormLayout()
        layout.addLayout(form)

        # Minimal fields for a product
        self.name_en = QLineEdit()
        self.name_en.setPlaceholderText("Product name in English/French")

        self.brand = QComboBox()
        self.brand.addItems([""])

        self.categories = QLineEdit()
        self.categories.setPlaceholderText("e.g. Electronics, TV")

        self.details = QLineEdit()
        self.details.setPlaceholderText("Type and press Enter to add more")

        self.sale_price = QDoubleSpinBox()
        self.sale_price.setRange(0.0, 1_000_000_000.0)
        self.sale_price.setDecimals(2)

        self.barcode = QLineEdit()
        self.installment_allowed = QCheckBox("Installment allowed")
        self.installment_allowed.setChecked(True)

        # Add rows
        form.addRow("Name (English) *", self.name_en)
        form.addRow("Brand", self.brand)
        form.addRow("Categories", self.categories)
        form.addRow("Details", self.details)
        form.addRow("Sale price *", self.sale_price)
        form.addRow("Barcode", self.barcode)
        form.addRow("", self.installment_allowed)
# ------------------------------
# Demo launcher
# ------------------------------
if __name__ == "__main__":
    app = QApplication([])

    dlg = QDialog()
    dlg.setWindowTitle("Inventory Management Tab Demo")
    dlg.setMinimumSize(720, 600)
    dlg.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

    tab = NewProductTab()

    buttons = QDialogButtonBox(
        QDialogButtonBox.Cancel
        | QDialogButtonBox.Ok
    )
    buttons.button(QDialogButtonBox.Ok).setShortcut("Ctrl+Return")
    buttons.rejected.connect(dlg.reject)
    buttons.accepted.connect(dlg.accept)

    root = QVBoxLayout(dlg)
    root.addWidget(tab)
    root.addWidget(buttons)

    dlg.show()
    sys.exit(app.exec())