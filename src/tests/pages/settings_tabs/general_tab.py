from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QFileDialog
from tests.pages.settings_tabs.utils import hwrap
from tests.pages.settings_tabs.settings_model import AppSettings


class GeneralTab(QWidget):
    def __init__(self, model: AppSettings):
        super().__init__()
        form = QFormLayout(self)
        self.store_name = QLineEdit(model.store_name)
        self.logo_path = QLineEdit(model.logo_path)
        browse = QPushButton("Browse…")
        browse.clicked.connect(self._choose_logo)
        logo_row = QHBoxLayout()
        logo_row.addWidget(self.logo_path)
        logo_row.addWidget(browse)
        self.contact_phone = QLineEdit(model.contact_phone)
        self.addres = QLineEdit(model.addres)
        form.addRow("Store name", self.store_name)
        form.addRow("Logo path", hwrap(logo_row))
        form.addRow("Contact phone", self.contact_phone)
        form.addRow("Address", self.addres)

    def _choose_logo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose logo", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.logo_path.setText(path)

    def collect(self, model: AppSettings) -> AppSettings:
        model.store_name = self.store_name.text()
        model.logo_path = self.logo_path.text()
        model.contact_phone = self.contact_phone.text()
        model.addres = self.addres.text()
        return model

    def apply_model(self, model: AppSettings):
        self.store_name.setText(model.store_name)
        self.logo_path.setText(model.logo_path)
        self.contact_phone.setText(model.contact_phone)
        self.addres.setText(model.addres)
