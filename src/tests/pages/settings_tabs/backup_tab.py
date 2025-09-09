from PySide6.QtWidgets import QWidget, QFormLayout, QCheckBox, QLineEdit, QPushButton, QHBoxLayout, QFileDialog
from tests.pages.settings_tabs.utils import hwrap
from tests.pages.settings_tabs.settings_model import AppSettings

class BackupTab(QWidget):
    def __init__(self, model: AppSettings):
        super().__init__()
        form = QFormLayout(self)
        self.auto_backup = QCheckBox()
        self.auto_backup.setChecked(model.auto_backup_daily)
        self.backup_dir = QLineEdit(model.backup_dir)
        choose = QPushButton("Choose folder…")
        choose.clicked.connect(self._choose_backup_dir)
        row = QHBoxLayout()
        row.addWidget(self.backup_dir)
        row.addWidget(choose)
        form.addRow("Daily auto-backup", self.auto_backup)
        form.addRow("Backup directory", hwrap(row))

    def _choose_backup_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Choose backup directory")
        if path:
            self.backup_dir.setText(path)

    def collect(self, model: AppSettings) -> AppSettings:
        model.auto_backup_daily = self.auto_backup.isChecked()
        model.backup_dir = self.backup_dir.text()
        return model

    def apply_model(self, model: AppSettings):
        self.auto_backup.setChecked(model.auto_backup_daily)
        self.backup_dir.setText(model.backup_dir)
