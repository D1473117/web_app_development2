from .db import get_db

class Transaction:
    @staticmethod
    def create(data):
        """
        新增一筆收支明細記錄。
        :param data: dict，包含 amount, category_id, type, date, note
        :return: int (新增的紀錄 ID)，若失敗則回傳 None
        """
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO transactions (amount, category_id, type, date, note) VALUES (?, ?, ?, ?, ?)",
                (data.get('amount'), data.get('category_id'), data.get('type'), data.get('date'), data.get('note', ''))
            )
            db.commit()
            last_id = cursor.lastrowid
            return last_id
        except Exception as e:
            print(f"Transaction.create Error: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_all(month=None):
        """
        取得所有收支紀錄，若提供 month 則過濾指定月份 (YYYY-MM)。
        :param month: str, 'YYYY-MM'
        :return: list of dict
        """
        try:
            db = get_db()
            query = """
                SELECT t.*, c.name as category_name
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
            """
            params = []
            if month:
                query += " WHERE strftime('%Y-%m', t.date) = ?"
                params.append(month)
            query += " ORDER BY t.date DESC, t.id DESC"
            transactions = db.execute(query, params).fetchall()
            return [dict(ix) for ix in transactions]
        except Exception as e:
            print(f"Transaction.get_all Error: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def get_by_id(transaction_id):
        """
        根據 ID 取得單筆收支明細與分類名稱。
        :param transaction_id: int
        :return: dict 或 None
        """
        try:
            db = get_db()
            row = db.execute(
                "SELECT t.*, c.name as category_name FROM transactions t LEFT JOIN categories c ON t.category_id = c.id WHERE t.id = ?",
                (transaction_id,)
            ).fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Transaction.get_by_id Error: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def update(transaction_id, data):
        """
        更新指定的收支明細。
        :param transaction_id: int
        :param data: dict
        :return: bool (成功或失敗)
        """
        try:
            db = get_db()
            db.execute(
                "UPDATE transactions SET amount = ?, category_id = ?, type = ?, date = ?, note = ? WHERE id = ?",
                (data.get('amount'), data.get('category_id'), data.get('type'), data.get('date'), data.get('note', ''), transaction_id)
            )
            db.commit()
            return True
        except Exception as e:
            print(f"Transaction.update Error: {e}")
            return False
        finally:
            db.close()

    @staticmethod
    def delete(transaction_id):
        """
        刪除特定收支明細。
        :param transaction_id: int
        :return: bool (成功或失敗)
        """
        try:
            db = get_db()
            db.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            db.commit()
            return True
        except Exception as e:
            print(f"Transaction.delete Error: {e}")
            return False
        finally:
            db.close()
