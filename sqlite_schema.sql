-- SQLite schema for Installments Desktop (MVP)
-- Money is stored in integer centimes (DZD)
-- Timestamps are Unix milliseconds

CREATE TABLE app_meta (
  key TEXT PRIMARY KEY,
  value TEXT
);
INSERT INTO app_meta(key, value) VALUES ('schema_version','1');

CREATE TABLE customer (
  id INTEGER PRIMARY KEY,
  branch_id INTEGER NOT NULL DEFAULT 1,
  full_name TEXT NOT NULL,
  arabic_full_name TEXT,
  dob INTEGER,
  residency_flag INTEGER NOT NULL DEFAULT 1,
  net_income_cents INTEGER NOT NULL DEFAULT 0,
  notes TEXT,
  photo_url TEXT,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_customer_branch_name ON customer(branch_id, full_name);

CREATE TABLE contact_method (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('mobile','phone','email','whatsapp')),
  value TEXT NOT NULL,
  is_primary INTEGER NOT NULL DEFAULT 0,
  verified_at INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(customer_id) REFERENCES customer(id) ON DELETE CASCADE
);
CREATE INDEX idx_contact_customer ON contact_method(customer_id, type);

-- Products & stock
CREATE TABLE product (
  id INTEGER PRIMARY KEY,
  sku TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  arabic_name TEXT,
  category TEXT,
  price_ttc_cents INTEGER NOT NULL,
  tax_rate_bp INTEGER NOT NULL DEFAULT 0,
  warranty_months INTEGER DEFAULT 0,
  is_active INTEGER NOT NULL DEFAULT 1,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_product_active ON product(is_active);

CREATE TABLE stock (
  id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL,
  branch_id INTEGER NOT NULL DEFAULT 1,
  qty INTEGER NOT NULL DEFAULT 0,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(product_id) REFERENCES product(id)
);
CREATE UNIQUE INDEX idx_stock_unique ON stock(product_id, branch_id);

CREATE TABLE stock_ledger (
  id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL,
  branch_id INTEGER NOT NULL DEFAULT 1,
  movement TEXT NOT NULL CHECK (movement IN ('receive','sell','return','adjust','transfer_out','transfer_in')),
  qty_delta INTEGER NOT NULL,
  ref_entity TEXT,
  ref_id INTEGER,
  at INTEGER NOT NULL,
  created_at INTEGER NOT NULL,
  FOREIGN KEY(product_id) REFERENCES product(id)
);
CREATE INDEX idx_stock_ledger_prod_at ON stock_ledger(product_id, at);

-- Sales
CREATE TABLE sale (
  id INTEGER PRIMARY KEY,
  branch_id INTEGER NOT NULL DEFAULT 1,
  customer_id INTEGER,
  user_id INTEGER,
  type TEXT NOT NULL CHECK (type IN ('cash','instalment')),
  status TEXT NOT NULL CHECK (status IN ('draft','completed','void')) DEFAULT 'draft',
  subtotal_cents INTEGER NOT NULL DEFAULT 0,
  discount_cents INTEGER NOT NULL DEFAULT 0,
  tax_cents INTEGER NOT NULL DEFAULT 0,
  total_cents INTEGER NOT NULL,
  down_payment_cents INTEGER NOT NULL DEFAULT 0,
  invoice_id INTEGER,
  receipt_id INTEGER,
  completed_at INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(customer_id) REFERENCES customer(id)
);
CREATE INDEX idx_sale_branch_status ON sale(branch_id, status, completed_at);

CREATE TABLE sale_item (
  id INTEGER PRIMARY KEY,
  sale_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  qty INTEGER NOT NULL,
  unit_price_cents INTEGER NOT NULL,
  line_total_cents INTEGER NOT NULL,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(sale_id) REFERENCES sale(id) ON DELETE CASCADE,
  FOREIGN KEY(product_id) REFERENCES product(id)
);
CREATE INDEX idx_sale_item_sale ON sale_item(sale_id);

-- Payments
CREATE TABLE payment (
  id INTEGER PRIMARY KEY,
  branch_id INTEGER NOT NULL DEFAULT 1,
  contract_id INTEGER,
  installment_id INTEGER,
  sale_id INTEGER,
  channel TEXT NOT NULL CHECK (channel IN ('cash','tpe_card','qr_a2a','online_card','bank_transfer')),
  provider TEXT,
  provider_ref TEXT,
  amount_cents INTEGER NOT NULL,
  currency TEXT NOT NULL DEFAULT 'DZD',
  status TEXT NOT NULL CHECK (status IN ('pending','succeeded','failed','refunded')) DEFAULT 'succeeded',
  received_at INTEGER NOT NULL,
  idempotency_key TEXT UNIQUE,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_payment_status_time ON payment(status, received_at DESC);
CREATE INDEX idx_payment_contract_inst ON payment(contract_id, installment_id);

-- Offers / Contracts (lightweight for MVP)
CREATE TABLE offer (
  id INTEGER PRIMARY KEY,
  application_id INTEGER,
  term_months INTEGER NOT NULL CHECK (term_months BETWEEN 3 AND 60),
  apr_bp INTEGER NOT NULL DEFAULT 0,
  total_cost_cents INTEGER NOT NULL DEFAULT 0,
  total_repay_cents INTEGER NOT NULL,
  fees_cents INTEGER NOT NULL DEFAULT 0,
  insurance_cents INTEGER NOT NULL DEFAULT 0,
  pdf_attachment_id INTEGER,
  shown_at INTEGER,
  accepted_at INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE contract (
  id INTEGER PRIMARY KEY,
  sale_id INTEGER NOT NULL,
  offer_id INTEGER NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('issued','signed','cancelled')) DEFAULT 'issued',
  signed_at INTEGER,
  immutable_hash TEXT,
  pdf_attachment_id INTEGER,
  evidence_pack_id INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(sale_id) REFERENCES sale(id),
  FOREIGN KEY(offer_id) REFERENCES offer(id)
);
CREATE INDEX idx_contract_status ON contract(status, signed_at);

CREATE TABLE schedule (
  id INTEGER PRIMARY KEY,
  contract_id INTEGER NOT NULL,
  installments_count INTEGER NOT NULL,
  start_date INTEGER NOT NULL,
  generated_at INTEGER NOT NULL,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(contract_id) REFERENCES contract(id)
);

CREATE TABLE installment (
  id INTEGER PRIMARY KEY,
  schedule_id INTEGER NOT NULL,
  number INTEGER NOT NULL,
  due_date INTEGER NOT NULL,
  principal_cents INTEGER NOT NULL,
  interest_cents INTEGER NOT NULL DEFAULT 0,
  fees_cents INTEGER NOT NULL DEFAULT 0,
  due_cents INTEGER NOT NULL,
  paid_cents INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL CHECK (status IN ('upcoming','due','overdue','paid','written_off')) DEFAULT 'upcoming',
  paid_at INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(schedule_id) REFERENCES schedule(id)
);
CREATE INDEX idx_installment_due ON installment(status, due_date);

-- Audit & attachments
CREATE TABLE audit_log (
  id INTEGER PRIMARY KEY,
  actor_user_id INTEGER,
  device_id TEXT,
  action TEXT NOT NULL,
  entity TEXT NOT NULL,
  entity_id INTEGER,
  at INTEGER NOT NULL,
  details_json TEXT
);
CREATE INDEX idx_audit_at ON audit_log(at);

CREATE TABLE attachment (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL CHECK (kind IN ('pdf','image','binary')),
  path TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  size INTEGER NOT NULL,
  encryption_iv TEXT,
  created_at INTEGER NOT NULL
);

-- Sync checkpoint
CREATE TABLE sync_checkpoint (
  device_id TEXT PRIMARY KEY,
  vector_json TEXT NOT NULL,
  last_pull_at INTEGER,
  last_push_at INTEGER
);

-- FTS5 for customers (optional; requires FTS5 compiled in)
-- Populate via triggers
CREATE VIRTUAL TABLE IF NOT EXISTS fts_customers USING fts5(full_name, arabic_full_name, content='customer', content_rowid='id');

CREATE TRIGGER IF NOT EXISTS customer_ai AFTER INSERT ON customer BEGIN
  INSERT INTO fts_customers(rowid, full_name, arabic_full_name) VALUES (new.id, new.full_name, new.arabic_full_name);
END;
CREATE TRIGGER IF NOT EXISTS customer_ad AFTER DELETE ON customer BEGIN
  INSERT INTO fts_customers(fts_customers, rowid, full_name, arabic_full_name) VALUES('delete', old.id, old.full_name, old.arabic_full_name);
END;
CREATE TRIGGER IF NOT EXISTS customer_au AFTER UPDATE ON customer BEGIN
  INSERT INTO fts_customers(fts_customers, rowid, full_name, arabic_full_name) VALUES('delete', old.id, old.full_name, old.arabic_full_name);
  INSERT INTO fts_customers(rowid, full_name, arabic_full_name) VALUES (new.id, new.full_name, new.arabic_full_name);
END;
