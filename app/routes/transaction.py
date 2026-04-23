import datetime
from flask import Blueprint, request, redirect, url_for, flash, render_template
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.budget import Budget

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/transactions', methods=['GET'])
def list_transactions():
    """
    HTTP GET '/transactions'
    讀取明細列表
    """
    month = request.args.get('month')
    if not month:
        month = datetime.datetime.now().strftime('%Y-%m')
        
    transactions = Transaction.get_all(month=month)
    categories = Category.get_all()
    
    return render_template(
        'transactions.html',
        transactions=transactions,
        categories=categories,
        current_month=month
    )

@transaction_bp.route('/transactions/add', methods=['GET'])
def add_transaction_page():
    """
    HTTP GET '/transactions/add'
    顯示新增明細表單頁面
    """
    categories = Category.get_all()
    return render_template(
        'add_transaction.html',
        categories=categories
    )

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    amount = request.form.get('amount')
    category_id = request.form.get('category_id')
    type_ = request.form.get('type')
    date_str = request.form.get('date')
    note = request.form.get('note')

    if not amount or not category_id or not type_ or not date_str:
        flash("請填寫所有必填欄位 (金額, 類別, 類型, 日期)", "danger")
        return redirect(url_for('transaction.list_transactions'))
        
    try:
        amount = float(amount)
        category_id = int(category_id)
        
        data = {
            'amount': amount,
            'category_id': category_id,
            'type': type_,
            'date': date_str,
            'note': note
        }
        
        tx_id = Transaction.create(data)
        if tx_id:
            flash("新增收支紀錄成功！", "success")
            
            # --- 預算超支檢查區塊 ---
            month = date_str[:7]
            budget = Budget.get_by_month(month=month)
            if budget and type_ == 'expense':
                all_tx = Transaction.get_all(month=month)
                total_expense = sum(t['amount'] for t in all_tx if t['type'] == 'expense')
                if total_expense >= budget['amount']:
                    flash(f"⚠️ 提醒：您 {month} 月份支用已經超標（支出 {total_expense} / 預算 {budget['amount']}）！", "warning")
        else:
            flash("新增紀錄發生失敗。", "danger")
            
    except ValueError:
        flash("無效的金額或類別傳入格式", "danger")
        
    # 重導去對應日期的那個月份列表避免使用者找不到剛新增的項目    
    return redirect(url_for('transaction.list_transactions', month=date_str[:7] if date_str else None))

@transaction_bp.route('/transactions/<int:id>/edit', methods=['POST'])
def update_transaction(id):
    amount = request.form.get('amount')
    category_id = request.form.get('category_id')
    type_ = request.form.get('type')
    date_str = request.form.get('date')
    note = request.form.get('note')
    
    if not amount or not category_id or not type_ or not date_str:
        flash("欄位不可為空", "danger")
        return redirect(url_for('transaction.list_transactions'))
    
    try:
         data = {
            'amount': float(amount),
            'category_id': int(category_id),
            'type': type_,
            'date': date_str,
            'note': note
         }
         if Transaction.update(id, data):
             flash("紀錄更新成功", "success")
         else:
             flash("更新失敗", "danger")
    except ValueError:
         flash("資料型態有誤", "danger")
         
    return redirect(url_for('transaction.list_transactions'))

@transaction_bp.route('/transactions/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    if Transaction.delete(id):
        flash("紀錄已經順利刪除", "success")
    else:
        flash("刪除過程失敗", "danger")
    return redirect(url_for('transaction.list_transactions'))
