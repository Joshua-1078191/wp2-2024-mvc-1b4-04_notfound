import sqlite3


class Users:
    def __init__(self, database_path):
        self.database_path = database_path


    def get_all(self):
        # Connect to database
        con = sqlite3.connect(self.database_path)
        cursor = con.cursor()
        cursor.row_factory = sqlite3.Row # [] -> {}

        # Fetch users
        users = cursor.execute("""
        SELECT * FROM users;
        """).fetchall()

        # Convert users
        result = []
        for user in users:
            result.append({
                "name": user["display_name"],
                "email": user["login"],
                "isAdmin": user["is_admin"],
                "id": user["user_id"]
            })

        return result

    def get(self, id):
        return {
            "name": "John Doe",
            "email": "john@mail.com",
            "isAdmin": False,
            "id": 1
        }