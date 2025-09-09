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
# Supplier Management
# ------------------------------

class SupplierManagementTab(QWidget):
    def __init__(self):
        super().__init__()

        form = QFormLayout(self)  # <-- attach layout to self

        # Fields
        self.supplier_name  = QLineEdit()
        self.supplier_email = QLineEdit()
        self.supplier_phone1 = QLineEdit()
        self.supplier_phone2 = QLineEdit()

        # Social + button
        self.supplier_social_media = QLineEdit()
        open_button = QPushButton("Open")
        open_button.clicked.connect(self._open_social_media)
        sm_row = QHBoxLayout()
        sm_row.addWidget(self.supplier_social_media)
        sm_row.addWidget(open_button)

        self.supplier_address = QTextEdit()

        # Add rows
        form.addRow("Name", self.supplier_name)
        form.addRow("Email", self.supplier_email)
        form.addRow("Phone 1", self.supplier_phone1)
        form.addRow("Phone 2", self.supplier_phone2)
        form.addRow("Social Media", sm_row)
        form.addRow("Address", self.supplier_address)

    def _open_social_media(self):
        url = self.supplier_social_media.text().strip()
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url
        if url:
            webbrowser.open(url)