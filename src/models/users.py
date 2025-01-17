import sqlite3
from sqlite3 import Connection
from typing import Any
from src.utils.password import verify_password, hash_password, generate_salt
from src.utils.database import connect_database, generate_query_params

class Users:
    def __init__(self, database_path):
        self.database_path = database_path

    def get_all(self) -> list[dict[str, Any]]:
        conn, cursor = connect_database(self.database_path)

        # Fetch users
        users = cursor.execute("""
            SELECT * FROM users;
            """).fetchall()

        # Convert user to right format
        result = [{
            "name": user["display_name"],
            "email": user["login"],
            "isAdmin": user["is_admin"],
            "id": user["user_id"]
        } for user in users]

        return result

    def get(self, target_id: int) -> dict[str, Any] | None:
        conn, cursor = connect_database(self.database_path)

        # Fetch user
        user = cursor.execute("""
        SELECT * FROM users WHERE user_id = ? LIMIT 1;
        """, (target_id,)).fetchone()

        # Return none if no user found
        if not user:
            return None

        # Convert user to right format
        result = {
            "name": user["display_name"],
            "email": user["login"],
            "isAdmin": user["is_admin"],
            "id": user["user_id"]
        }

        return result

    def update(self, target_id:int, username:str | None = None, email: str | None = None, password: str | None = None, is_admin:bool | None = None):
        conn, cursor = connect_database(self.database_path)

        salt = None
        if password:
            salt = generate_salt()
            password = hash_password(password, salt)

        # get query string and parameters
        query_params = generate_query_params(login=email, display_name=username, password=password, salt=salt, is_admin=is_admin)

        try:
            cursor.execute(
                f"UPDATE users SET {query_params.query} WHERE user_id = ?",
                [*query_params.params, target_id]
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def register(self, username:str, email: str, password: str, is_admin:bool = False) -> bool:
        conn, cursor = connect_database(self.database_path)

        salt = generate_salt()
        hashed_password = hash_password(password, salt)

        try:
            cursor.execute(
                "INSERT INTO users (login, password, salt, display_name, is_admin) VALUES (?, ?, ?, ?, ?);",
                (email, hashed_password, salt, username, is_admin)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def delete(self, target_id:int):
        conn, cursor = connect_database(self.database_path)

        try:
            cursor.execute(
                """
                DELETE FROM users 
                WHERE users.user_id = ?
                """,
                (target_id,)
            )

            conn.commit()
            rows_affected = conn.rowcount
            conn.close()

            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def login(self, email: str, password: str) -> dict | None:
        conn, cursor = connect_database(self.database_path)

        # Fetch user
        user = cursor.execute("""
            SELECT * FROM users WHERE login = ? LIMIT 1;
            """, (email,)).fetchone()

        # Return none if no user found
        if not user:
            return None

        # Return none if password incorrect
        if not verify_password(password, user["password"], user["salt"]):
            return None

        # Convert user to right format
        result = {
            "name": user["display_name"],
            "email": user["login"],
            "isAdmin": user["is_admin"],
            "id": user["user_id"]
        }

        return result
