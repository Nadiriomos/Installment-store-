from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox
from tests.pages.settings_tabs.utils import hwrap
from tests.pages.settings_tabs.settings_model import AppSettings

class UITab(QWidget):
    def __init__(self, model: AppSettings, on_restart_required=None):
        super().__init__()
        self._on_restart_required = on_restart_required
        form = QFormLayout(self)
        self.language = QComboBox()
        self.language.addItems(["English", "Français", "العربية"])
        self.language.setCurrentText(model.language)
        if self._on_restart_required:
            self.language.currentTextChanged.connect(self._on_restart_required)
        self.theme = QComboBox()
        self.theme.addItems(["Light", "Dark", "System"])
        self.theme.setCurrentText(model.theme)
        self.date_format = QComboBox()
        self.date_format.addItems(["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        self.date_format.setCurrentText(model.date_format)
        if self._on_restart_required:
            self.date_format.currentTextChanged.connect(self._on_restart_required)
        self.startup_page = QComboBox()
        self.startup_page.addItems(["Dashboard", "Sales", "Inventory", "Reports"])
        self.startup_page.setCurrentText(model.startup_page)
        form.addRow("Language", self.language)
        form.addRow("Theme", self.theme)
        form.addRow("Date format", self.date_format)
        form.addRow("Startup page", self.startup_page)

    def collect(self, model: AppSettings) -> AppSettings:
        model.language = self.language.currentText()
        model.theme = self.theme.currentText()
        model.date_format = self.date_format.currentText()
        model.startup_page = self.startup_page.currentText()
        return model

    def apply_model(self, model: AppSettings):
        self.language.setCurrentText(model.language)
        self.theme.setCurrentText(model.theme)
        self.date_format.setCurrentText(model.date_format)
        self.startup_page.setCurrentText(model.startup_page)
