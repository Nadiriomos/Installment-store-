from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox, QLineEdit
from PySide6.QtGui import QDoubleValidator
from tests.pages.settings_tabs.utils import hwrap
from tests.pages.settings_tabs.settings_model import AppSettings

class FinanceTab(QWidget):
    def __init__(self, model: AppSettings, on_restart_required=None):
        super().__init__()
        self._on_restart_required = on_restart_required
        form = QFormLayout(self)
        self.currency = QComboBox()
        self.currency.addItems(["USD", "EUR", "DZD"])
        self.currency.setCurrentText(model.currency)
        if self._on_restart_required:
            self.currency.currentTextChanged.connect(self._on_restart_required)
        self.default_frequency = QComboBox()
        self.default_frequency.addItems(["Weekly", "Biweekly", "Monthly"])
        self.default_frequency.setCurrentText(model.default_frequency)
        self.installment_fee = QLineEdit(str(model.installment_fee))
        self.installment_fee.setValidator(QDoubleValidator(0.0, 1_000_000.0, 2, self))
        form.addRow("Currency", self.currency)
        form.addRow("Default frequency", self.default_frequency)
        form.addRow("Installment percentage", self.installment_fee)

    def collect(self, model: AppSettings) -> AppSettings:
        model.currency = self.currency.currentText()
        model.default_frequency = self.default_frequency.currentText()
        model.installment_fee = float(self.installment_fee.text() or 0)
        return model

    def apply_model(self, model: AppSettings):
        self.currency.setCurrentText(model.currency)
        self.default_frequency.setCurrentText(model.default_frequency)
        self.installment_fee.setText(str(model.installment_fee))
