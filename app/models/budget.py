from .db import get_db

class Budget:
    @staticmethod
    def create_or_update(month, amount):
        db = get_db()
        cursor = db.cursor()
        existing = cursor.execute("SELECT id FROM budgets WHERE month = ?", (month,)).fetchone()
        if existing:
            cursor.execute("UPDATE budgets SET amount = ? WHERE month = ?", (amount, month))
            db.commit()
            last_id = existing['id']
        else:
            cursor.execute("INSERT INTO budgets (month, amount) VALUES (?, ?)", (month, amount))
            db.commit()
            last_id = cursor.lastrowid
        db.close()
        return last_id

    @staticmethod
    def get_by_month(month):
        db = get_db()
        row = db.execute("SELECT * FROM budgets WHERE month = ?", (month,)).fetchone()
        db.close()
        return dict(row) if row else None

    @staticmethod
    def get_all():
        db = get_db()
        rows = db.execute("SELECT * FROM budgets ORDER BY month DESC").fetchall()
        db.close()
        return [dict(ix) for ix in rows]

    @staticmethod
    def delete(budget_id):
        db = get_db()
        db.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
        db.commit()
        db.close()
