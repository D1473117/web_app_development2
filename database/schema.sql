CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    is_default INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category_id INTEGER,
    type TEXT NOT NULL,
    date TEXT NOT NULL,
    note TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL UNIQUE,
    amount REAL NOT NULL
);

-- 插入系統預設類別資料
INSERT INTO categories (name, type, is_default) VALUES 
('食', 'expense', 1),
('衣', 'expense', 1),
('住', 'expense', 1),
('行', 'expense', 1),
('育樂', 'expense', 1),
('未分類', 'expense', 1),
('薪資', 'income', 1),
('獎金', 'income', 1),
('零用錢', 'income', 1);
