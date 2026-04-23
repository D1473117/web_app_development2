from flask import Blueprint, request, redirect, url_for, flash, render_template

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/transactions', methods=['GET'])
def list_transactions():
    """
    HTTP GET '/transactions'
    負責讀取資料庫中某個月（或所有）的收支明細清單與所有的分類選項，
    並將數列結果傳遞給 transactions.html 以便在表格上渲染與提供下拉選單。
    """
    pass

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    """
    HTTP POST '/transactions'
    接收來自前端的新增表單資料（包含金額、日期、分類等），驗證必填項後寫入資料庫。
    接著與當月預算比對，若總額超出則設定警告提醒 (Flash Message)，
    最後統一重導向回 GET /transactions。
    """
    pass

@transaction_bp.route('/transactions/<int:id>/edit', methods=['POST'])
def update_transaction(id):
    """
    HTTP POST '/transactions/<id>/edit'
    接收編輯表單傳入的新數據，針對指定的紀錄 ID 更新資料，
    完成後重導向。
    """
    pass

@transaction_bp.route('/transactions/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """
    HTTP POST '/transactions/<id>/delete'
    刪除資料庫內符合該 ID 的收支紀錄明細，
    完成後重導向至清單頁首。
    """
    pass
