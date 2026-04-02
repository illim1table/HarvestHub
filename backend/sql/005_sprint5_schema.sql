ALTER TABLE orders
  ADD COLUMN payment_trade_no VARCHAR(64) NULL,
  ADD COLUMN paid_at DATETIME NULL,
  ADD COLUMN completed_at DATETIME NULL,
  ADD COLUMN cancelled_at DATETIME NULL;

CREATE INDEX idx_orders_payment_trade_no ON orders(payment_trade_no);
