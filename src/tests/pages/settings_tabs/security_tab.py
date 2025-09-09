from PySide6.QtWidgets import QWidget, QFormLayout, QCheckBox, QSpinBox
from tests.pages.settings_tabs.utils import hwrap
from tests.pages.settings_tabs.settings_model import AppSettings

class SecurityTab(QWidget):
    def __init__(self, model: AppSettings):
        super().__init__()
        form = QFormLayout(self)
        self.auto_lock = QSpinBox()
        self.auto_lock.setRange(0, 120)
        self.auto_lock.setValue(model.auto_lock_minutes)
        self.pin_for_refunds = QCheckBox()
        self.pin_for_refunds.setChecked(model.require_pin_for_refunds)
        form.addRow("Auto-lock after (minutes)", self.auto_lock)
        form.addRow("Require PIN for refunds", self.pin_for_refunds)

    def collect(self, model: AppSettings) -> AppSettings:
        model.auto_lock_minutes = self.auto_lock.value()
        model.require_pin_for_refunds = self.pin_for_refunds.isChecked()
        return model

    def apply_model(self, model: AppSettings):
        self.auto_lock.setValue(model.auto_lock_minutes)
        self.pin_for_refunds.setChecked(model.require_pin_for_refunds)
