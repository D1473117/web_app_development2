from .db import get_db

class Budget:
    @staticmethod
    def create_or_update(data):
        """
        新增或是更新某一個月份的預算設定上限。
        :param data: dict，包含 month (YYYY-MM) 還有 amount
        :return: int (紀錄 ID)，若失敗回傳 None
        """
        try:
            db = get_db()
            cursor = db.cursor()
            month = data.get('month')
            amount = data.get('amount')
            
            existing = cursor.execute("SELECT id FROM budgets WHERE month = ?", (month,)).fetchone()
            if existing:
                cursor.execute("UPDATE budgets SET amount = ? WHERE month = ?", (amount, month))
                last_id = existing['id']
            else:
                cursor.execute("INSERT INTO budgets (month, amount) VALUES (?, ?)", (month, amount))
                last_id = cursor.lastrowid
            db.commit()
            return last_id
        except Exception as e:
            print(f"Budget.create_or_update Error: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_by_month(month):
        """
        取得單一個月份所設定的總預算設定。
        :param month: str, 'YYYY-MM'
        :return: dict 或 None
        """
        try:
            db = get_db()
            row = db.execute("SELECT * FROM budgets WHERE month = ?", (month,)).fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Budget.get_by_month Error: {e}")
            return None
        finally:
            db.close()
            
    @staticmethod
    def get_all():
        """
        取得系統內歷史以來的全部預算設定紀錄。
        :return: list of dict
        """
        try:
            db = get_db()
            rows = db.execute("SELECT * FROM budgets ORDER BY month DESC").fetchall()
            return [dict(ix) for ix in rows]
        except Exception as e:
            print(f"Budget.get_all Error: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def delete(budget_id):
        """
        刪除某一筆預算設定點。
        :param budget_id: int
        :return: bool (成功或失敗)
        """
        try:
            db = get_db()
            db.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
            db.commit()
            return True
        except Exception as e:
            print(f"Budget.delete Error: {e}")
            return False
        finally:
            db.close()
