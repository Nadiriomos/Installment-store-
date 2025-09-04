# Utility function to get screen geometry
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QRect

def get_screen_geometry(app: QApplication, full_screen: bool = False) -> QRect:
    """
    Returns the QRect geometry of the primary screen.

    :param app: QApplication instance
    :param full_screen: 
        - True  -> Full screen size (including taskbar/docks).
        - False -> Available area (excluding taskbar/docks).
    """
    screen = app.primaryScreen()
    return screen.geometry() if full_screen else screen.availableGeometry()

# Helper function to create a sidebar button
from PySide6.QtWidgets import (QPushButton)
from PySide6.QtGui import (QIcon, QFont, QPalette, QColor)
from PySide6.QtCore import (Qt, QSize)


def make_sidebar_button(text: str, icon_path: str = None) -> QPushButton:
    btn = QPushButton(text)

    # Font settings
    font = QFont("Segoe UI", 12)   # family + size
    #font.setBold(True)             # optional
    btn.setFont(font)

    # Icon
    if icon_path:
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(24, 24))

    # Align text left with icon
    btn.setStyleSheet("text-align: left; padding: 8px;")
    btn.setCursor(Qt.PointingHandCursor)

    return btn