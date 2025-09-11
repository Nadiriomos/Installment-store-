# Installment Store

A PySide6-based desktop app for managing installment sales, inventory, and suppliers.

## ✅ Current Progress

- [x] **Settings UI**
  - Split into tabs (General, Finance, Inventory, Notifications, Security, UI & App, Backup)
  - Persistence handled via `QSettings`
  - `AppSettings` dataclass for defaults and type safety

- [x] **Inventory Tabs**
  - `NewProductTab`, `InventoryManagementTab`, `SupplierManagementTab`
  - Basic layouts and input fields done

- [x] **Project Structure**
  - Tabs organized into separate files
  - `pyproject.toml` present

- [ ] **Database Layer**
  - Central `db/` package (`db/__init__.py`, `suppliers.py`, `products.py`, `inventory.py`)
  - `init_db()` to apply `sqlite_schema.sql` on startup

- [ ] **Supplier Management**
  - Connect Supplier tab to DB
  - CRUD operations (add, list; update/delete later)

- [ ] **Inventory Management**
  - Hook up brand/category/tag management to DB
  - Add table/list views

- [ ] **Reports Tab**
  - Needs to be re-added after refactor

- [ ] **Tests & Packaging**
  - Add smoke tests for DB + tabs
  - Provide run script (`python -m src.main`)

## 🚀 Next Steps

1. Create `db/` package with shared connection logic (`get_conn`, `init_db`).
2. Implement supplier CRUD in `db/suppliers.py`.
3. Call `init_db()` when the app starts.
4. Fix imports consistently (absolute or package-based).
5. Add README usage instructions (`poetry run python src/main.py`).
6. Add tests for supplier CRUD and settings persistence.

---

## How to Run (Dev)

```bash
# install dependencies
poetry install

# run app
poetry run python src/tests/pages/settings.py
```

Or with pip/venv:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/tests/pages/settings.py
```
