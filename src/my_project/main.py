# Standard library
import sys, os
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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.my_project.utils.helpers import get_screen_geometry, make_sidebar_button
from src.tests.pages.dashboard import DashboardPage
from src.tests.pages.customers import CustomersPage
from src.tests.pages.payments import PaymentsPage
from src.tests.pages.reports import ReportsPage
from src.tests.pages.inventory import InventoryPage
from src.tests.pages.settings import SettingsPage
from src.tests.pages.contact import ContactPage
# === home page ui ===



class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home Page")
        self.showMaximized()

        # set geometry
        geometry = get_screen_geometry(app)
        self.setGeometry(geometry)

        # shortcut
        QShortcut(QKeySequence("Esc"), self, activated=self.close)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Sidebar + Content
        sidebar = self._build_sidebar()
        self.content_stack = self._build_content()

        # Layout assembly
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack, stretch=1)

    # === Sidebar ===
    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("QFrame { background: #2c3e50; }")

        layout = QVBoxLayout(sidebar)

        # --- Top buttons ---
        top_buttons = [
            ("Dashboard", "src/icons/dashboard.png", 0),
            ("Customers", "src/icons/customer.png", 1),
            ("Payments", "src/icons/payments.png", 2),
            ("Reports", "src/icons/report.png", 3),
            ("Inventory", "src/icons/inventory.png", 4)
        ]
        for text, icon, index in top_buttons:
            btn = make_sidebar_button(text, icon)
            btn.clicked.connect(lambda _, i=index: self.content_stack.setCurrentIndex(i))
            layout.addWidget(btn)

        layout.addStretch()  # pushes next widgets down

        # --- Bottom buttons ---
        bottom_buttons = [
            ("Settings", "src/icons/settings.png", 5),
            ("Contact", "src/icons/contact.png", 6),
        ]
        for text, icon, index in bottom_buttons:
            btn = make_sidebar_button(text, icon)
            btn.clicked.connect(lambda _, i=index: self.content_stack.setCurrentIndex(i))
            layout.addWidget(btn)

        return sidebar

    # === Content Area ===
    def _build_content(self):
        stack = QStackedWidget()
        stack.addWidget(DashboardPage())  # index 0
        stack.addWidget(CustomersPage())  # index 1
        stack.addWidget(PaymentsPage())   # index 2
        stack.addWidget(ReportsPage())    # index 3
        stack.addWidget(InventoryPage())  # index 4
        stack.addWidget(SettingsPage())   # index 5
        stack.addWidget(ContactPage())    # index 6
        return stack


if __name__ == "__main__":
    app = QApplication([])
    home_page = HomePage()
    home_page.show()
    app.exec()