from .db import get_db

class Transaction:
    @staticmethod
    def create(amount, category_id, type, date, note=''):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO transactions (amount, category_id, type, date, note) VALUES (?, ?, ?, ?, ?)",
            (amount, category_id, type, date, note)
        )
        db.commit()
        last_id = cursor.lastrowid
        db.close()
        return last_id

    @staticmethod
    def get_all(month=None):
        db = get_db()
        query = """
            SELECT t.*, c.name as category_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
        """
        params = []
        if month:
            # month parameter in format 'YYYY-MM'
            query += " WHERE strftime('%Y-%m', t.date) = ?"
            params.append(month)
        query += " ORDER BY t.date DESC, t.id DESC"
        transactions = db.execute(query, params).fetchall()
        db.close()
        return [dict(ix) for ix in transactions]

    @staticmethod
    def get_by_id(transaction_id):
        db = get_db()
        row = db.execute(
            "SELECT t.*, c.name as category_name FROM transactions t LEFT JOIN categories c ON t.category_id = c.id WHERE t.id = ?",
            (transaction_id,)
        ).fetchone()
        db.close()
        return dict(row) if row else None

    @staticmethod
    def update(transaction_id, amount, category_id, type, date, note):
        db = get_db()
        db.execute(
            "UPDATE transactions SET amount = ?, category_id = ?, type = ?, date = ?, note = ? WHERE id = ?",
            (amount, category_id, type, date, note, transaction_id)
        )
        db.commit()
        db.close()

    @staticmethod
    def delete(transaction_id):
        db = get_db()
        db.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        db.commit()
        db.close()
