import os
import sqlite3
from flask import Flask
from app.routes import register_routes

# 取得資料庫的絕對路徑
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')

def init_db():
    " 初始化資料庫，讀取 schema.sql 並建立資料表 "
    if not os.path.exists(os.path.dirname(DATABASE_PATH)):
        os.makedirs(os.path.dirname(DATABASE_PATH))
    conn = sqlite3.connect(DATABASE_PATH)
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("資料庫初始化完成！")

def create_app():
    app = Flask(__name__)
    
    # 基本設定 (實務上可從 os.environ 或 .env 讀取，MVP 暫設 dev 環境)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # 註冊所有在 app/routes/__init__.py 定義的 Blueprint
    register_routes(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    # 如果資料庫尚未建立，自動執行初始化
    if not os.path.exists(DATABASE_PATH):
        print("未偵測到資料庫檔案，正自動為您建立...")
        init_db()
    
    # 啟動應用程式
    app.run(debug=True)
