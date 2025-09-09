from PySide6.QtWidgets import QWidget, QFormLayout, QCheckBox
from tests.pages.settings_tabs.utils import hwrap
from tests.pages.settings_tabs.settings_model import AppSettings
class NotificationsTab(QWidget):
    def __init__(self, model: AppSettings):
        super().__init__()
        form = QFormLayout(self)
        self.notify_upcoming = QCheckBox()
        self.notify_upcoming.setChecked(model.notify_upcoming_due)
        self.notify_lowstock = QCheckBox()
        self.notify_lowstock.setChecked(model.notify_low_stock)
        form.addRow("Upcoming installment reminders", self.notify_upcoming)
        form.addRow("Low-stock notifications", self.notify_lowstock)

    def collect(self, model: AppSettings) -> AppSettings:
        model.notify_upcoming_due = self.notify_upcoming.isChecked()
        model.notify_low_stock = self.notify_lowstock.isChecked()
        return model

    def apply_model(self, model: AppSettings):
        self.notify_upcoming.setChecked(model.notify_upcoming_due)
        self.notify_lowstock.setChecked(model.notify_low_stock)
