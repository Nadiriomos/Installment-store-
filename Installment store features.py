# Standard library
import os
import time
import shutil
import sqlite3
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
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon



# === DB setup ===
class Database:
    def create_connection():
        conn = sqlite3.connect("installment_store.db")
        return conn

    def create_table():

        conn = create_connection()
        cursor = conn.cursor()


        conn.commit()
        conn.close()