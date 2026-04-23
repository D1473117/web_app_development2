from flask import Flask
from .dashboard import dashboard_bp
from .transaction import transaction_bp
from .settings import settings_bp

def register_routes(app: Flask):
    """
    在主要的 Flask Application 啟動前，
    統一註冊各個 Blueprint 路由。
    """
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(settings_bp)
