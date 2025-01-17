from lib.database.db import get_db

class User:
    def __init__(self, user_id, login, display_name, is_admin):
        self.user_id = user_id
        self.login = login
        self.display_name = display_name
        self.is_admin = is_admin

    @staticmethod
    def get_by_email(email):
        conn = get_db()
        try:
            user = conn.execute('SELECT * FROM users WHERE login = ?', (email,)).fetchone()
            if user:
                return User(user['user_id'], user['login'], user['display_name'], user['is_admin'])
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_credentials(email, password):
        conn = get_db()
        try:
            user = conn.execute('SELECT * FROM users WHERE login = ? AND password = ?', 
                              (email, password)).fetchone()
            if user:
                return User(user['user_id'], user['login'], user['display_name'], user['is_admin'])
            return None
        finally:
            conn.close()

    @staticmethod
    def create_user(email, password, display_name=None):
        if display_name is None:
            display_name = email.split('@')[0]
            
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (login, password, display_name, is_admin) VALUES (?, ?, ?, ?)',
                        (email, password, display_name, 0))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()
