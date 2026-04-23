from .db import get_db

class Category:
    @staticmethod
    def create(name, type, is_default=0):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO categories (name, type, is_default) VALUES (?, ?, ?)", (name, type, is_default))
        db.commit()
        last_id = cursor.lastrowid
        db.close()
        return last_id

    @staticmethod
    def get_all():
        db = get_db()
        categories = db.execute("SELECT * FROM categories ORDER BY id ASC").fetchall()
        db.close()
        return [dict(ix) for ix in categories]

    @staticmethod
    def get_by_id(category_id):
        db = get_db()
        category = db.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
        db.close()
        return dict(category) if category else None

    @staticmethod
    def update(category_id, name, type):
        db = get_db()
        db.execute("UPDATE categories SET name = ?, type = ? WHERE id = ?", (name, type, category_id))
        db.commit()
        db.close()

    @staticmethod
    def delete(category_id):
        db = get_db()
        db.execute("DELETE FROM categories WHERE id = ? AND is_default = 0", (category_id,))
        db.commit()
        db.close()
