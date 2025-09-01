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

