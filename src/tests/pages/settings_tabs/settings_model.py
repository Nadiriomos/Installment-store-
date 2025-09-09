from dataclasses import dataclass

@dataclass
class AppSettings:
    store_name: str = "My Store"
    logo_path: str = ""
    contact_phone: str = ""
    addres: str = ""
    currency: str = "USD"
    default_frequency: str = "Monthly"
    installment_fee: float = 15.0
    low_stock_alerts: bool = True
    low_stock_threshold: int = 5
    barcode_enabled: bool = False
    default_report_period: str = "Monthly"
    show_outstanding_metric: bool = True
    show_sales_trend: bool = True
    auto_lock_minutes: int = 10
    require_pin_for_refunds: bool = True
    notify_upcoming_due: bool = True
    notify_low_stock: bool = True
    auto_backup_daily: bool = True
    backup_dir: str = ""
    language: str = "English"
    theme: str = "System"
    date_format: str = "DD/MM/YYYY"
    startup_page: str = "Dashboard"
