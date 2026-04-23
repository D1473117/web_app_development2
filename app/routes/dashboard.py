import datetime
from flask import Blueprint, render_template
from app.models.transaction import Transaction
from app.models.budget import Budget
from app.models.category import Category

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
def index():
    """
    HTTP GET '/'
    首頁路由，負責取得當月統計並渲染
    """
    now = datetime.datetime.now()
    current_month = now.strftime('%Y-%m')
    
    # 撈取該月所有明細與預算上限
    transactions = Transaction.get_all(month=current_month)
    budget = Budget.get_by_month(month=current_month)
    
    # 快速計算當月總計金額
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    
    budget_limit = budget['amount'] if budget else 0
    remaining_budget = budget_limit - total_expense if budget_limit > 0 else 0
    
    # 彙整分類所佔金額給圓餅圖使用
    expense_data = {}
    for t in transactions:
        if t['type'] == 'expense':
            cat_name = t['category_name'] or '未分類'
            expense_data[cat_name] = expense_data.get(cat_name, 0) + t['amount']
            
    # 只取最近五筆呈現於首頁
    recent_transactions = transactions[:5]
    
    return render_template(
        'index.html',
        current_month=current_month,
        total_income=total_income,
        total_expense=total_expense,
        budget_limit=budget_limit,
        remaining_budget=remaining_budget,
        expense_data=expense_data,
        recent_transactions=recent_transactions
    )
