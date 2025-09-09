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
# Inventory Management     
# ------------------------------

class InventoryManagementTab(QWidget):
    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        form = QFormLayout()
        root.addLayout(form)

        # --- Brands ---
        form.addRow(QLabel("Brands:"))
        form.addRow(self._line())

        self.new_brand = QLineEdit()
        self.add_brand_btn = QPushButton("Add New Brand")
        brand_add_row = QHBoxLayout()
        brand_add_row.addWidget(self.new_brand)
        brand_add_row.addWidget(self.add_brand_btn)
        form.addRow("Add new brand", self._wrap(brand_add_row))

        self.brand = QComboBox()
        self.brand.addItems([""])
        self.delete_brand_btn = QPushButton("Delete Selected Brand")
        brand_del_row = QHBoxLayout()
        brand_del_row.addWidget(self.brand)
        brand_del_row.addWidget(self.delete_brand_btn)
        form.addRow("Select brand to delete", self._wrap(brand_del_row))

        form.addRow(self._line())

        # --- Categories ---
        form.addRow(QLabel("Categories:"))
        form.addRow(self._line())

        self.new_category = QLineEdit()
        self.add_category_btn = QPushButton("Add New Category")
        cat_add_row = QHBoxLayout()
        cat_add_row.addWidget(self.new_category)
        cat_add_row.addWidget(self.add_category_btn)
        form.addRow("Add new category", self._wrap(cat_add_row))

        self.category = QComboBox()
        self.category.addItems([""])
        self.delete_category_btn = QPushButton("Delete Selected Category")
        cat_del_row = QHBoxLayout()
        cat_del_row.addWidget(self.category)
        cat_del_row.addWidget(self.delete_category_btn)
        form.addRow("Select category to delete", self._wrap(cat_del_row))

        form.addRow(self._line())

        # --- Tags ---
        form.addRow(QLabel("Tags:"))
        form.addRow(self._line())

        self.new_tag = QLineEdit()
        self.add_tag_btn = QPushButton("Add New Tag")
        tag_add_row = QHBoxLayout()
        tag_add_row.addWidget(self.new_tag)
        tag_add_row.addWidget(self.add_tag_btn)
        form.addRow("Add new tag", self._wrap(tag_add_row))

        self.tag = QComboBox()
        self.tag.addItems([""])
        self.delete_tag_btn = QPushButton("Delete Selected Tag")
        tag_del_row = QHBoxLayout()
        tag_del_row.addWidget(self.tag)
        tag_del_row.addWidget(self.delete_tag_btn)
        form.addRow("Select tag to delete", self._wrap(tag_del_row))

        form.addRow(self._line())

    # --- helpers ---
    def _line(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def _wrap(self, layout: QHBoxLayout):
        """QFormLayout.addRow expects a QWidget; wrap an HBox into a QWidget."""
        w = QWidget()
        w.setLayout(layout)
        return w
    
# ------------------------------
# Demo launcher
if __name__ == "__main__":
    app = QApplication([])

    dlg = QDialog()
    dlg.setWindowTitle("Inventory Management Tab Demo")
    dlg.setMinimumSize(720, 600)
    dlg.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

    tab = InventoryManagementTab()

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