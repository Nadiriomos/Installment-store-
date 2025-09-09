from PySide6.QtWidgets import QWidget

def hwrap(layout) -> QWidget:
    w = QWidget()
    w.setLayout(layout)
    return w
