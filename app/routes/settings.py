import datetime
from flask import Blueprint, request, redirect, url_for, flash, render_template
from app.models.category import Category
from app.models.budget import Budget

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET'])
def view_settings():
    month = request.args.get('month')
    if not month:
        month = datetime.datetime.now().strftime('%Y-%m')
        
    categories = Category.get_all()
    budget = Budget.get_by_month(month)
    
    # 拆分收入與支出類別給表單好分類呈現
    income_cats = [c for c in categories if c['type'] == 'income']
    expense_cats = [c for c in categories if c['type'] == 'expense']
    
    return render_template(
        'settings.html',
        income_cats=income_cats,
        expense_cats=expense_cats,
        budget=budget,
        current_month=month
    )

@settings_bp.route('/settings/budget', methods=['POST'])
def update_budget():
    month = request.form.get('month')
    amount = request.form.get('amount')
    
    if not month or not amount:
        flash("請輸入並確認您選擇的時間與預算金額範圍", "danger")
        return redirect(url_for('settings.view_settings'))
        
    try:
        data = {
            'month': month,
            'amount': float(amount)
        }
        if Budget.create_or_update(data):
            flash(f"已順利應用 {month} 月份新預算上限", "success")
        else:
            flash("預算建立遇到不明錯誤", "danger")
    except ValueError:
        flash("數字格式填寫有誤", "danger")
        
    return redirect(url_for('settings.view_settings', month=month))

@settings_bp.route('/settings/categories', methods=['POST'])
def create_category():
    name = request.form.get('name')
    type_ = request.form.get('type')
    
    if not name or not type_:
        flash("新增類別需要提供名稱和歸屬！", "danger")
        return redirect(url_for('settings.view_settings'))
        
    data = {
        'name': name.strip(),
        'type': type_,
        'is_default': 0
    }
    
    if Category.create(data):
        flash(f"自訂類別「{name}」建立成功", "success")
    else:
        flash("設定過程錯誤", "danger")
        
    return redirect(url_for('settings.view_settings'))

@settings_bp.route('/settings/categories/<int:id>/delete', methods=['POST'])
def delete_category(id):
    if Category.delete(id):
        flash("自訂類別已被移除！相關的歷史明細並不會被清除掉。", "success")
    else:
        flash("刪除失敗！系統預設類別不允許被刪除。", "danger")
    return redirect(url_for('settings.view_settings'))
