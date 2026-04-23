from flask import Blueprint, request, redirect, url_for, flash, render_template

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET'])
def view_settings():
    """
    HTTP GET '/settings'
    查詢所有的類別項目與當月的設定預算額度，並傳送給 settings.html 進行版面渲染。
    """
    pass

@settings_bp.route('/settings/budget', methods=['POST'])
def update_budget():
    """
    HTTP POST '/settings/budget'
    接收來自表單的當月總預算數字並執行新增或修改至 budgets 表單之中，
    成功後重導向至設定頁。
    """
    pass

@settings_bp.route('/settings/categories', methods=['POST'])
def create_category():
    """
    HTTP POST '/settings/categories'
    接收收支類型字串與自訂分類名稱，新增至 categories 以作為後續選項來源，
    完成後重導向。
    """
    pass

@settings_bp.route('/settings/categories/<int:id>/delete', methods=['POST'])
def delete_category(id):
    """
    HTTP POST '/settings/categories/<id>/delete'
    刪除特定 id 且不屬於系統預設的自訂收支分類。
    若違反規則將於 Controller 中被擋下並跳開錯誤，
    最後重導向。
    """
    pass
