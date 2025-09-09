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

class InventoryManagementTab(QDialog):
    def _build_inventory_management_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        form = QFormLayout()
        layout.addLayout(form)

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