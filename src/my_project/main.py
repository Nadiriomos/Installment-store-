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
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

