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
                               QVBoxLayout, QWidget, QStackedWidget, QTableWidget, QTableWidgetItem,)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

# === home page ui ===


class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home Page")
        self.showMaximized()

        # === Central Widget (needed for QMainWindow) ===
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout (horizontal: sidebar + content)
        main_layout = QHBoxLayout(central_widget)

        # ----- Sidebar -----
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setStyleSheet("QFrame { background: #2c3e50; }")  # Dark sidebar
        sidebar.setFixedWidth(200)  # Sidebar width

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(15)

        # Add buttons to sidebar
        sidebar_layout.addWidget(QPushButton("Dashboard"))
        sidebar_layout.addWidget(QPushButton("Students"))
        sidebar_layout.addWidget(QPushButton("Payments"))
        sidebar_layout.addWidget(QPushButton("Reports"))
        sidebar_layout.addStretch()  # Push items up

        # ----- Main Content -----
        content = QFrame()
        content.setFrameShape(QFrame.StyledPanel)
        content.setStyleSheet("QFrame { background: #ecf0f1; }")

        content_layout = QVBoxLayout(content)
        content_layout.addWidget(QLabel("Welcome to Main Content"))

        # Add both frames to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content, stretch=1)


# === main ===
if __name__ == "__main__":
    app = QApplication([])
    home_page = HomePage()
    home_page.show()   
    app.exec()