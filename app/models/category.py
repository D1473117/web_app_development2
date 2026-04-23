from .db import get_db

class Category:
    @staticmethod
    def create(data):
        """
        新增分類。
        :param data: dict，包含 name, type, is_default
        :return: int (新增的紀錄 ID)，若失敗回傳 None
        """
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO categories (name, type, is_default) VALUES (?, ?, ?)", 
                (data.get('name'), data.get('type'), data.get('is_default', 0))
            )
            db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Category.create Error: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_all():
        """
        取得所有可用的分類。
        :return: list of dict
        """
        try:
            db = get_db()
            categories = db.execute("SELECT * FROM categories ORDER BY type ASC, id ASC").fetchall()
            return [dict(ix) for ix in categories]
        except Exception as e:
            print(f"Category.get_all Error: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def get_by_id(category_id):
        """
        根據 ID 取得單一分類。
        :param category_id: int
        :return: dict 或 None
        """
        try:
            db = get_db()
            row = db.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Category.get_by_id Error: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def update(category_id, data):
        """
        更新指定的分類名稱或是種類。
        :param category_id: int
        :param data: dict，包含 name, type
        :return: bool (成功或失敗)
        """
        try:
            db = get_db()
            db.execute(
                "UPDATE categories SET name = ?, type = ? WHERE id = ?",
                (data.get('name'), data.get('type'), category_id)
            )
            db.commit()
            return True
        except Exception as e:
            print(f"Category.update Error: {e}")
            return False
        finally:
            db.close()

    @staticmethod
    def delete(category_id):
        """
        刪除特定分類。若為預設分類 (is_default = 1) 則不允許被刪除。
        :param category_id: int
        :return: bool (成功或失敗)
        """
        try:
            db = get_db()
            db.execute("DELETE FROM categories WHERE id = ? AND is_default = 0", (category_id,))
            db.commit()
            return True
        except Exception as e:
            print(f"Category.delete Error: {e}")
            return False
        finally:
            db.close()
