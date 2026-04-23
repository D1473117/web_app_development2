import sqlite3
import os

# 根據專案結構，取得 instance 資料夾路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'database.db')

def get_db():
    """與 SQLite 資料庫建立連線，設定 Row Factory 以字典方式存取欄位"""
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
