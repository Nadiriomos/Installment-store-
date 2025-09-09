from PySide6.QtWidgets import QWidget, QFormLayout, QCheckBox, QSpinBox
from tests.pages.settings_tabs.utils import hwrap
from tests.pages.settings_tabs.settings_model import AppSettings

class InventoryTab(QWidget):
    def __init__(self, model: AppSettings):
        super().__init__()
        form = QFormLayout(self)
        self.low_stock_alerts = QCheckBox()
        self.low_stock_alerts.setChecked(model.low_stock_alerts)
        self.low_stock_threshold = QSpinBox()
        self.low_stock_threshold.setRange(0, 100000)
        self.low_stock_threshold.setValue(model.low_stock_threshold)
        self.barcode_enabled = QCheckBox()
        self.barcode_enabled.setChecked(model.barcode_enabled)
        form.addRow("Low-stock alerts", self.low_stock_alerts)
        form.addRow("Low-stock threshold", self.low_stock_threshold)
        form.addRow("Enable barcode scanning", self.barcode_enabled)

    def collect(self, model: AppSettings) -> AppSettings:
        model.low_stock_alerts = self.low_stock_alerts.isChecked()
        model.low_stock_threshold = self.low_stock_threshold.value()
        model.barcode_enabled = self.barcode_enabled.isChecked()
        return model

    def apply_model(self, model: AppSettings):
        self.low_stock_alerts.setChecked(model.low_stock_alerts)
        self.low_stock_threshold.setValue(model.low_stock_threshold)
        self.barcode_enabled.setChecked(model.barcode_enabled)
