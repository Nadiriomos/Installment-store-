from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox, QCheckBox
from tests.pages.settings_tabs.utils import hwrap
from tests.pages.settings_tabs.settings_model import AppSettings

class ReportsTab(QWidget):
    def __init__(self, model: AppSettings):
        super().__init__()
        form = QFormLayout(self)
        self.report_period = QComboBox()
        self.report_period.addItems(["Daily", "Weekly", "Monthly"])
        self.report_period.setCurrentText(model.default_report_period)
        self.show_outstanding = QCheckBox()
        self.show_outstanding.setChecked(model.show_outstanding_metric)
        self.show_sales_trend = QCheckBox()
        self.show_sales_trend.setChecked(model.show_sales_trend)
        form.addRow("Default report period", self.report_period)
        form.addRow("Show Outstanding metric", self.show_outstanding)
        form.addRow("Show Sales Trend graph", self.show_sales_trend)

    def collect(self, model: AppSettings) -> AppSettings:
        model.default_report_period = self.report_period.currentText()
        model.show_outstanding_metric = self.show_outstanding.isChecked()
        model.show_sales_trend = self.show_sales_trend.isChecked()
        return model

    def apply_model(self, model: AppSettings):
        self.report_period.setCurrentText(model.default_report_period)
        self.show_outstanding.setChecked(model.show_outstanding_metric)
        self.show_sales_trend.setChecked(model.show_sales_trend)
