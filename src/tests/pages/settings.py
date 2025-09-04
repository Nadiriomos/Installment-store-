from __future__ import annotations

import sys
import json
import hashlib
import secrets
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

from PySide6.QtCore import Qt, QSettings, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTableView,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLabel,
)


# ------------------------------
# Data model for settings (defaults)
# ------------------------------
@dataclass
class AppSettings:
    # General / Business
    store_name: str = "My Store"
    logo_path: str = ""
    contact_phone: str = ""
    addres: str = ""

    # Finance / Installments
    currency: str = "USD"
    default_frequency: str = "Monthly"  # Weekly, Biweekly, Monthly
    installment_fee: float = 15.0        # installment percentage fee

    # Inventory
    low_stock_alerts: bool = True
    low_stock_threshold: int = 5
    barcode_enabled: bool = False

    # Reports / Dashboard
    default_report_period: str = "Monthly"  # Daily, Weekly, Monthly
    show_outstanding_metric: bool = True
    show_sales_trend: bool = True

    # Security
    auto_lock_minutes: int = 10
    require_pin_for_refunds: bool = True

    # Notifications
    notify_upcoming_due: bool = True
    notify_low_stock: bool = True

    # Backup / Data
    auto_backup_daily: bool = True
    backup_dir: str = ""

    # UI / App
    language: str = "English"
    theme: str = "System"  # Light, Dark, System
    date_format: str = "DD/MM/YYYY"
    startup_page: str = "Dashboard"  # Dashboard, Sales, Inventory, Reports


# ------------------------------
# PIN hashing helpers
# ------------------------------

def hash_pin(pin: str, salt_hex: str | None = None) -> tuple[str, str]:
    """Return (pin_hash_hex, salt_hex). Uses SHA-256 over (salt + pin)."""
    if salt_hex is None:
        salt_hex = secrets.token_hex(16)  # 128-bit salt
    h = hashlib.sha256()
    h.update(bytes.fromhex(salt_hex))
    h.update(pin.encode("utf-8"))
    return h.hexdigest(), salt_hex


def verify_pin(pin: str, pin_hash_hex: str, salt_hex: str) -> bool:
    return hash_pin(pin, salt_hex)[0] == pin_hash_hex


# ------------------------------
# Users & Roles table model
# ------------------------------
class UsersRolesModel(QAbstractTableModel):
    COLS = ["Username", "Role", "Active", "PIN"]

    def __init__(self, rows: List[Dict[str, Any]] | None = None, parent: QWidget | None = None):
        super().__init__(parent)
        self._rows: List[Dict[str, Any]] = rows or []

    # Qt model basics
    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        return len(self.COLS)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        r, c = index.row(), index.column()
        row = self._rows[r]
        if role in (Qt.DisplayRole, Qt.EditRole):
            if c == 0:
                return row.get("username", "")
            elif c == 1:
                return row.get("role", "Cashier")
            elif c == 2:
                return "Yes" if row.get("active", True) and role == Qt.DisplayRole else row.get("active", True)
            elif c == 3:
                # Mask: show dots if a hash exists
                return "••••" if role == Qt.DisplayRole and row.get("pin_hash") else (row.get("pin_hash", "")[:8] + "…" if role == Qt.EditRole and row.get("pin_hash") else "")
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.COLS[section]
        return super().headerData(section, orientation, role)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        base = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() in (0, 1, 2):
            base |= Qt.ItemIsEditable
        return base

    def setData(self, index: QModelIndex, value, role=Qt.EditRole):
        if role != Qt.EditRole or not index.isValid():
            return False
        r, c = index.row(), index.column()
        row = self._rows[r]
        if c == 0:
            row["username"] = str(value).strip()
        elif c == 1:
            row["role"] = str(value)
        elif c == 2:
            row["active"] = (value if isinstance(value, bool) else str(value).lower() in ("1", "true", "yes", "y"))
        else:
            return False
        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        return True

    # API helpers
    def add_user(self, username: str, role: str, active: bool = True, pin: str | None = None):
        user = {"username": username, "role": role, "active": active}
        if pin:
            pin_hash, salt = hash_pin(pin)
            user["pin_hash"] = pin_hash
            user["salt"] = salt
        self.beginInsertRows(QModelIndex(), len(self._rows), len(self._rows))
        self._rows.append(user)
        self.endInsertRows()

    def remove_user(self, row: int):
        if 0 <= row < len(self._rows):
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._rows[row]
            self.endRemoveRows()

    def set_pin(self, row: int, pin: str):
        if 0 <= row < len(self._rows):
            pin_hash, salt = hash_pin(pin)
            self._rows[row]["pin_hash"] = pin_hash
            self._rows[row]["salt"] = salt
            idx = self.index(row, 3)
            self.dataChanged.emit(idx, idx, [Qt.DisplayRole])

    def to_list(self) -> List[Dict[str, Any]]:
        return self._rows


# ------------------------------
# User editor dialog
# ------------------------------
class UserEditor(QDialog):
    def __init__(self, parent: QWidget | None = None, *, username: str = "", role: str = "Cashier", active: bool = True, ask_pin: bool = True):
        super().__init__(parent)
        self.setWindowTitle("User")
        self.setModal(True)

        self.name_edit = QLineEdit(username)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Owner", "Manager", "Cashier"])
        self.role_combo.setCurrentText(role)
        self.active_check = QCheckBox()
        self.active_check.setChecked(active)
        self.pin_edit = QLineEdit("")
        self.pin_edit.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow("Username", self.name_edit)
        form.addRow("Role", self.role_combo)
        form.addRow("Active", self.active_check)
        if ask_pin:
            form.addRow("PIN (optional)", self.pin_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        root = QVBoxLayout(self)
        root.addLayout(form)
        root.addWidget(buttons)

    def values(self) -> Dict[str, Any]:
        return {
            "username": self.name_edit.text().strip(),
            "role": self.role_combo.currentText(),
            "active": self.active_check.isChecked(),
            "pin": self.pin_edit.text(),
        }


# ------------------------------
# Permissions tab widget
# ------------------------------
PERMISSIONS = [
    "manage_users",       # add/edit/remove users
    "refunds",            # allow processing refunds
    "edit_prices",        # change product prices
    "view_reports",       # access reports
    "manage_inventory",   # add products, adjust stock
]
DEFAULT_ROLE_PERMS = {
    "Owner": {p: True for p in PERMISSIONS},
    "Manager": {
        "manage_users": False,
        "refunds": True,
        "edit_prices": True,
        "view_reports": True,
        "manage_inventory": True,
    },
    "Cashier": {
        "manage_users": False,
        "refunds": False,
        "edit_prices": False,
        "view_reports": False,
        "manage_inventory": False,
    },
}


class PermissionsTab(QWidget):
    def __init__(self, settings: QSettings, parent: QWidget | None = None):
        super().__init__(parent)
        self.settings = settings
        self._checkboxes: Dict[tuple[str, str], QCheckBox] = {}
        layout = QVBoxLayout(self)

        grid = QFormLayout()
        # One row per role, each with a horizontal list of checkboxes
        self.role_boxes: Dict[str, List[QCheckBox]] = {}
        perms = self._load_permissions()
        for role in ("Owner", "Manager", "Cashier"):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            boxes: List[QCheckBox] = []
            for p in PERMISSIONS:
                cb = QCheckBox(p)
                cb.setChecked(perms.get(role, DEFAULT_ROLE_PERMS[role]).get(p, False))
                boxes.append(cb)
                self._checkboxes[(role, p)] = cb
                row_layout.addWidget(cb)
            row_layout.addStretch(1)
            self.role_boxes[role] = boxes
            grid.addRow(role, row_widget)

        layout.addLayout(grid)
        self.hint = QLabel("Configure what each role can do. Changes apply on Save/Apply.")
        self.hint.setWordWrap(True)
        layout.addWidget(self.hint)
        layout.addStretch(1)

    def _load_permissions(self) -> Dict[str, Dict[str, bool]]:
        if self.settings.contains("permissions"):
            try:
                return json.loads(self.settings.value("permissions", "{}"))
            except Exception:
                return DEFAULT_ROLE_PERMS.copy()
        return DEFAULT_ROLE_PERMS.copy()

    def values(self) -> Dict[str, Dict[str, bool]]:
        out: Dict[str, Dict[str, bool]] = {"Owner": {}, "Manager": {}, "Cashier": {}}
        for (role, p), cb in self._checkboxes.items():
            out.setdefault(role, {})[p] = cb.isChecked()
        return out


# ------------------------------
# Login dialog
# ------------------------------
class LoginDialog(QDialog):
    def __init__(self, settings: QSettings, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.settings = settings
        users = self._load_users()

        self.user_combo = QComboBox()
        active_users = [u for u in users if u.get("active", True)]
        self._users = active_users
        self.user_combo.addItems([u["username"] for u in active_users])

        self.pin_edit = QLineEdit()
        self.pin_edit.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow("User", self.user_combo)
        form.addRow("PIN", self.pin_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._try_login)
        buttons.rejected.connect(self.reject)

        root = QVBoxLayout(self)
        root.addLayout(form)
        root.addWidget(buttons)

    def _load_users(self) -> List[Dict[str, Any]]:
        try:
            return json.loads(self.settings.value("users", "[]"))
        except Exception:
            return []

    def _try_login(self):
        name = self.user_combo.currentText()
        pin = self.pin_edit.text()
        user = next((u for u in self._users if u.get("username") == name), None)
        if not user:
            QMessageBox.warning(self, "Login", "Unknown user")
            return
        pin_hash = user.get("pin_hash", "")
        salt = user.get("salt", "")
        if pin_hash and salt and verify_pin(pin, pin_hash, salt):
            self.accept()
        else:
            QMessageBox.warning(self, "Login", "Invalid PIN")


# ------------------------------
# Settings dialog (with Users & Roles + Permissions tabs)
# ------------------------------
class SettingsPage(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(980, 680)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self._restart_required = False

        self.settings = QSettings("YourCompany", "YourApp")
        self.model = self._load_settings()

        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_general_tab(), "General")
        self.tabs.addTab(self._build_finance_tab(), "Finance")
        self.tabs.addTab(self._build_inventory_tab(), "Inventory")
        self.tabs.addTab(self._build_reports_tab(), "Reports")
        self.tabs.addTab(self._build_security_tab(), "Security")
        self.tabs.addTab(self._build_notifications_tab(), "Notifications")
        self.tabs.addTab(self._build_backup_tab(), "Backup & Data")
        self.tabs.addTab(self._build_ui_tab(), "UI & App")
        self.permissions_tab = PermissionsTab(self.settings)
        self.tabs.addTab(self._build_users_tab(), "Users & Roles")
        self.tabs.addTab(self.permissions_tab, "Permissions")

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.RestoreDefaults
            | QDialogButtonBox.Cancel
            | QDialogButtonBox.Apply
            | QDialogButtonBox.Ok
        )
        self.buttons.clicked.connect(self._on_buttons)

        root = QVBoxLayout(self)
        root.addWidget(self.tabs)
        root.addWidget(self.buttons)

        # keyboard shortcuts
        self.buttons.button(QDialogButtonBox.Ok).setShortcut("Ctrl+Return")
        self.buttons.button(QDialogButtonBox.Apply).setShortcut("Ctrl+S")

    # --------------------------
    # Tabs
    # --------------------------
    def _build_general_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.store_name = QLineEdit(self.model.store_name)
        self.logo_path = QLineEdit(self.model.logo_path)
        browse_logo = QPushButton("Browse…")
        browse_logo.clicked.connect(self._choose_logo)
        logo_row = QHBoxLayout()
        logo_row.addWidget(self.logo_path)
        logo_row.addWidget(browse_logo)

        self.contact_phone = QLineEdit(self.model.contact_phone)
        self.addres_edit = QLineEdit(self.model.addres)

        form.addRow("Store name", self.store_name)
        form.addRow("Logo path", self._hwrap(logo_row))
        form.addRow("Contact phone", self.contact_phone)
        form.addRow("Address", self.addres_edit)
        return w

    def _build_finance_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.currency = QComboBox()
        self.currency.addItems(["USD", "EUR", "DZD"])  # extend as needed
        self.currency.setCurrentText(self.model.currency)
        self.currency.currentTextChanged.connect(self._mark_restart_required)

        self.default_frequency = QComboBox()
        self.default_frequency.addItems(["Weekly", "Biweekly", "Monthly"])
        self.default_frequency.setCurrentText(self.model.default_frequency)

        self.installment_fee = QLineEdit(str(self.model.installment_fee))
        self.installment_fee.setValidator(QDoubleValidator(0.0, 1000.0, 2, self))

        form.addRow("Currency", self.currency)
        form.addRow("Default frequency", self.default_frequency)
        form.addRow("Installment percentage (%)", self.installment_fee)
        return w

    def _build_inventory_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.low_stock_alerts = QCheckBox()
        self.low_stock_alerts.setChecked(self.model.low_stock_alerts)

        self.low_stock_threshold = QSpinBox()
        self.low_stock_threshold.setRange(0, 100000)
        self.low_stock_threshold.setValue(self.model.low_stock_threshold)

        self.barcode_enabled = QCheckBox()
        self.barcode_enabled.setChecked(self.model.barcode_enabled)

        form.addRow("Low-stock alerts", self.low_stock_alerts)
        form.addRow("Low-stock threshold", self.low_stock_threshold)
        form.addRow("Enable barcode scanning", self.barcode_enabled)
        return w

    def _build_reports_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.report_period = QComboBox()
        self.report_period.addItems(["Daily", "Weekly", "Monthly"])
        self.report_period.setCurrentText(self.model.default_report_period)

        self.show_outstanding = QCheckBox()
        self.show_outstanding.setChecked(self.model.show_outstanding_metric)

        self.show_sales_trend = QCheckBox()
        self.show_sales_trend.setChecked(self.model.show_sales_trend)

        form.addRow("Default report period", self.report_period)
        form.addRow("Show Outstanding metric", self.show_outstanding)
        form.addRow("Show Sales Trend graph", self.show_sales_trend)
        return w

    def _build_security_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.auto_lock = QSpinBox()
        self.auto_lock.setRange(0, 120)
        self.auto_lock.setValue(self.model.auto_lock_minutes)

        self.pin_for_refunds = QCheckBox()
        self.pin_for_refunds.setChecked(self.model.require_pin_for_refunds)

        form.addRow("Auto-lock after (minutes)", self.auto_lock)
        form.addRow("Require PIN for refunds", self.pin_for_refunds)
        return w

    def _build_notifications_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.notify_upcoming = QCheckBox()
        self.notify_upcoming.setChecked(self.model.notify_upcoming_due)

        self.notify_lowstock = QCheckBox()
        self.notify_lowstock.setChecked(self.model.notify_low_stock)

        form.addRow("Upcoming installment reminders", self.notify_upcoming)
        form.addRow("Low-stock notifications", self.notify_lowstock)
        return w

    def _build_backup_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.auto_backup = QCheckBox()
        self.auto_backup.setChecked(self.model.auto_backup_daily)

        self.backup_dir = QLineEdit(self.model.backup_dir)
        choose_dir = QPushButton("Choose folder…")
        choose_dir.clicked.connect(self._choose_backup_dir)
        row = QHBoxLayout()
        row.addWidget(self.backup_dir)
        row.addWidget(choose_dir)

        form.addRow("Daily auto-backup", self.auto_backup)
        form.addRow("Backup directory", self._hwrap(row))
        return w

    def _build_ui_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)

        self.language = QComboBox()
        self.language.addItems(["English", "Français", "العربية"])
        self.language.setCurrentText(self.model.language)
        self.language.currentTextChanged.connect(self._mark_restart_required)

        self.theme = QComboBox()
        self.theme.addItems(["Light", "Dark", "System"])
        self.theme.setCurrentText(self.model.theme)

        self.date_format = QComboBox()
        self.date_format.addItems(["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        self.date_format.setCurrentText(self.model.date_format)
        self.date_format.currentTextChanged.connect(self._mark_restart_required)

        self.startup_page = QComboBox()
        self.startup_page.addItems(["Dashboard", "Sales", "Inventory", "Reports"])
        self.startup_page.setCurrentText(self.model.startup_page)

        form.addRow("Language", self.language)
        form.addRow("Theme", self.theme)
        form.addRow("Date format", self.date_format)
        form.addRow("Startup page", self.startup_page)
        return w

    def _build_users_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)

        self.users_model = UsersRolesModel(self._load_users())
        table = QTableView()
        table.setModel(self.users_model)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSelectionBehavior(QTableView.SelectRows)
        table.setSelectionMode(QTableView.SingleSelection)
        self.users_table = table

        row = QHBoxLayout()
        self.btn_add = QPushButton("Add user")
        self.btn_edit = QPushButton("Edit…")
        self.btn_pin = QPushButton("Set/Change PIN…")
        self.btn_remove = QPushButton("Remove")
        row.addWidget(self.btn_add)
        row.addWidget(self.btn_edit)
        row.addWidget(self.btn_pin)
        row.addStretch(1)
        row.addWidget(self.btn_remove)

        self.btn_add.clicked.connect(self._on_user_add)
        self.btn_edit.clicked.connect(self._on_user_edit)
        self.btn_pin.clicked.connect(self._on_user_pin)
        self.btn_remove.clicked.connect(self._on_user_remove)

        hint = QLabel("Roles: Owner (full), Manager, Cashier. PINs are securely hashed.")
        hint.setWordWrap(True)

        layout.addWidget(table)
        layout.addLayout(row)
        layout.addWidget(hint)
        return w

    # --------------------------
    # Helpers
    # --------------------------
    def _hwrap(self, layout: QHBoxLayout) -> QWidget:
        w = QWidget()
        w.setLayout(layout)
        return w

    def _choose_logo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose logo", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.logo_path.setText(path)

    def _choose_backup_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Choose backup directory")
        if path:
            self.backup_dir.setText(path)

    def _mark_restart_required(self, *_):
        if not self._restart_required:
            self._restart_required = True

    # --------------------------
    # Users & permissions persistence
    # --------------------------
    def _load_users(self) -> List[Dict[str, Any]]:
        if self.settings.contains("users"):
            try:
                return json.loads(self.settings.value("users", "[]"))
            except Exception:
                return []
        # default admin user on first run
        return [{"username": "owner", "role": "Owner", "active": True}]

    def _save_users(self):
        self.settings.setValue("users", json.dumps(self.users_model.to_list()))

    def _load_permissions(self) -> Dict[str, Dict[str, bool]]:
        if self.settings.contains("permissions"):
            try:
                return json.loads(self.settings.value("permissions", "{}"))
            except Exception:
                return DEFAULT_ROLE_PERMS.copy()
        return DEFAULT_ROLE_PERMS.copy()

    def _save_permissions(self, data: Dict[str, Dict[str, bool]]):
        self.settings.setValue("permissions", json.dumps(data))

    # --------------------------
    # Settings persistence
    # --------------------------
    def _load_settings(self) -> AppSettings:
        s = AppSettings()
        sdict = asdict(s)
        for key in sdict.keys():
            if self.settings.contains(key):
                value = self.settings.value(key, sdict[key])
                # type adapt
                if isinstance(sdict[key], bool):
                    value = str(value).lower() in ("1", "true", "yes")
                elif isinstance(sdict[key], int):
                    try:
                        value = int(value)
                    except Exception:
                        pass
                elif isinstance(sdict[key], float):
                    try:
                        value = float(value)
                    except Exception:
                        pass
                setattr(s, key, value)
        # ensure default permissions exist
        if not self.settings.contains("permissions"):
            self._save_permissions(DEFAULT_ROLE_PERMS.copy())
        return s

    def _collect(self) -> AppSettings:
        return AppSettings(
            # General
            store_name=self.store_name.text(),
            logo_path=self.logo_path.text(),
            contact_phone=self.contact_phone.text(),
            addres=self.addres_edit.text(),
            # Finance
            currency=self.currency.currentText(),
            default_frequency=self.default_frequency.currentText(),
            installment_fee=float(self.installment_fee.text() or 0),
            # Inventory
            low_stock_alerts=self.low_stock_alerts.isChecked(),
            low_stock_threshold=self.low_stock_threshold.value(),
            barcode_enabled=self.barcode_enabled.isChecked(),
            # Reports
            default_report_period=self.report_period.currentText(),
            show_outstanding_metric=self.show_outstanding.isChecked(),
            show_sales_trend=self.show_sales_trend.isChecked(),
            # Security
            auto_lock_minutes=self.auto_lock.value(),
            require_pin_for_refunds=self.pin_for_refunds.isChecked(),
            # Notifications
            notify_upcoming_due=self.notify_upcoming.isChecked(),
            notify_low_stock=self.notify_lowstock.isChecked(),
            # Backup
            auto_backup_daily=self.auto_backup.isChecked(),
            backup_dir=self.backup_dir.text(),
            # UI
            language=self.language.currentText(),
            theme=self.theme.currentText(),
            date_format=self.date_format.currentText(),
            startup_page=self.startup_page.currentText(),
        )

    def _save(self, s: AppSettings):
        for k, v in asdict(s).items():
            self.settings.setValue(k, v)
        # Save users & permissions
        self._save_users()
        self._save_permissions(self.permissions_tab.values())
        self.settings.sync()

    def _restore_defaults(self):
        confirm = QMessageBox.question(
            self,
            "Restore defaults",
            "Reset all settings to their default values?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.settings.clear()
            self.model = AppSettings()  # reset
            # Reset users to default admin
            self.users_model = UsersRolesModel(self._load_users())
            self.users_table.setModel(self.users_model)
            # Reset permissions
            self.permissions_tab = PermissionsTab(self.settings)
            # Rebuild visible widgets
            self._rebuild_from_model()
            self._restart_required = True

    def _rebuild_from_model(self):
        # Apply model back to widgets (used after restore)
        self.store_name.setText(self.model.store_name)
        self.logo_path.setText(self.model.logo_path)
        self.contact_phone.setText(self.model.contact_phone)
        self.addres_edit.setText(self.model.addres)

        self.currency.setCurrentText(self.model.currency)
        self.default_frequency.setCurrentText(self.model.default_frequency)
        self.installment_fee.setText(str(self.model.installment_fee))

        self.low_stock_alerts.setChecked(self.model.low_stock_alerts)
        self.low_stock_threshold.setValue(self.model.low_stock_threshold)
        self.barcode_enabled.setChecked(self.model.barcode_enabled)

        self.report_period.setCurrentText(self.model.default_report_period)
        self.show_outstanding.setChecked(self.model.show_outstanding_metric)
        self.show_sales_trend.setChecked(self.model.show_sales_trend)

        self.auto_lock.setValue(self.model.auto_lock_minutes)
        self.pin_for_refunds.setChecked(self.model.require_pin_for_refunds)

        self.notify_upcoming.setChecked(self.model.notify_upcoming_due)
        self.notify_lowstock.setChecked(self.model.notify_low_stock)

        self.auto_backup.setChecked(self.model.auto_backup_daily)
        self.backup_dir.setText(self.model.backup_dir)

        self.language.setCurrentText(self.model.language)
        self.theme.setCurrentText(self.model.theme)
        self.date_format.setCurrentText(self.model.date_format)
        self.startup_page.setCurrentText(self.model.startup_page)

    # --------------------------
    # Button handling
    # --------------------------
    def _on_buttons(self, button):
        role = self.buttons.buttonRole(button)
        if role == QDialogButtonBox.AcceptRole:  # OK
            self._apply()
            self.accept()
        elif role == QDialogButtonBox.ApplyRole:  # Apply
            self._apply()
        elif role == QDialogButtonBox.RejectRole:  # Cancel
            self.reject()
        elif role == QDialogButtonBox.ResetRole:  # Restore defaults
            self._restore_defaults()

    def _apply(self):
        new_model = self._collect()
        self._save(new_model)
        self.model = new_model

        if self._restart_required:
            QMessageBox.information(
                self,
                "Restart required",
                "Some changes (language/date format/currency) may require restarting the app to fully apply.",
            )
            self._restart_required = False

    # --------------------------
    # Users actions
    # --------------------------
    def _current_row(self) -> int:
        idx = self.users_table.currentIndex()
        return idx.row() if idx.isValid() else -1

    def _on_user_add(self):
        dlg = UserEditor(self)
        if dlg.exec() == QDialog.Accepted:
            vals = dlg.values()
            if not vals["username"]:
                QMessageBox.warning(self, "Validation", "Username is required")
                return
            # ensure unique username
            if any(u["username"].lower() == vals["username"].lower() for u in self.users_model.to_list()):
                QMessageBox.warning(self, "Validation", "Username already exists")
                return
            self.users_model.add_user(vals["username"], vals["role"], vals["active"], vals.get("pin") or None)
            self._save_users()

    def _on_user_edit(self):
        r = self._current_row()
        if r < 0:
            return
        user = self.users_model.to_list()[r]
        dlg = UserEditor(self, username=user.get("username", ""), role=user.get("role", "Cashier"), active=user.get("active", True), ask_pin=False)
        if dlg.exec() == QDialog.Accepted:
            vals = dlg.values()
            # update inline
            self.users_model.setData(self.users_model.index(r, 0), vals["username"])  # username
            self.users_model.setData(self.users_model.index(r, 1), vals["role"])      # role
            self.users_model.setData(self.users_model.index(r, 2), vals["active"])    # active
            self._save_users()

    def _on_user_pin(self):
        r = self._current_row()
        if r < 0:
            return
        pin, ok = QInputDialog.getText(self, "Set PIN", "Enter new PIN (numbers only recommended):", QLineEdit.Password)
        if ok and pin:
            self.users_model.set_pin(r, pin)
            self._save_users()

    def _on_user_remove(self):
        r = self._current_row()
        if r < 0:
            return
        if QMessageBox.question(self, "Remove user", "Delete the selected user?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.users_model.remove_user(r)
            self._save_users()


# ------------------------------
# Demo launcher
# ------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("YourCompany")
    app.setApplicationName("YourApp")

    # Example: show login first (optional)
    settings = QSettings("YourCompany", "YourApp")
    login = LoginDialog(settings)
    if login.exec() != QDialog.Accepted:
        sys.exit(0)

    dlg = SettingsPage()
    if dlg.exec() == QDialog.Accepted:
        print("Settings saved:")
        print(asdict(dlg.model))
    sys.exit(0)
