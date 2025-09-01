# Standard library
import os
import time
import shutil
import webbrowser
import urllib.parse
from datetime import datetime
from socket import create_connection

# Third-party libraries
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from openpyxl import Workbook

# pySide6
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QFrame, QHBoxLayout,
                               QVBoxLayout, QWidget, QStackedWidget, QTableWidget, QTableWidgetItem,
                               QHeaderView, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import (QKeySequence, QShortcut, QPixmap)

# helpers
from utils.helpers import get_screen_geometry, make_sidebar_button

# === home page ui ===



class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home Page")
        self.showMaximized()   # full window

        # set geometry
        geometry = get_screen_geometry(app)
        self.setGeometry(geometry)

        # shortcuts
        QShortcut(QKeySequence("Esc"), self, activated=self.close)

        # Central widget (required for QMainWindow)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout (horizontal split)
        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("QFrame { background: #2c3e50; }")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.addWidget(make_sidebar_button("Dashboard", "src/icons/dashboard.png"))
        sidebar_layout.addWidget(make_sidebar_button("Customers", "src/icons/customer.png"))
        sidebar_layout.addWidget(make_sidebar_button("Payments", "src/icons/payments.png"))
        sidebar_layout.addWidget(make_sidebar_button("Reports", "src/icons/report.png"))

        sidebar_layout.addStretch()

        sidebar_layout.addWidget(make_sidebar_button("Settings", "src/icons/settings.png"))
        sidebar_layout.addWidget(make_sidebar_button("Contact", "src/icons/contact.png"))

        # Content
        content = QFrame()
        content.setStyleSheet("QFrame { background: #ecf0f1; }")

        content_layout = QVBoxLayout(content)

        # --- Centered PNG ---
        image_label = QLabel()
        pixmap = QPixmap("src/icons/home_page.png")
        image_label.setPixmap(pixmap.scaled(1000, 1000, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)

        content_layout.addStretch()
        content_layout.addWidget(image_label, alignment=Qt.AlignCenter)
        content_layout.addStretch()

        # Add frames to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content, stretch=1)  # content grows

        # Ensure content expands
        content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

if __name__ == "__main__":
    app = QApplication([])
    home_page = HomePage()
    home_page.show()
    app.exec()