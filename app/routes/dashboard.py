from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
def index():
    """
    HTTP GET '/'
    首頁路由，負責在進入系統時查詢：
    1. 當月的總支出與總收入
    2. 當月的總可用預算與狀態
    3. 生成圓餅圖所需的分類金額資料
    4. 撈取最新的幾筆收支紀錄
    將這些資料計算完畢後傳遞給 index.html 進行畫面渲染。
    """
    pass
