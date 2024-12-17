import sqlite3


class Prompts:
    def __init__(self, db_path):
        self.db = db_path

    def prompt_all_view(self):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        prompts_all_data = cursor.execute("""
            SELECT 
                p.*,
                u.display_name as user_name
            FROM prompts p
            LEFT JOIN users u ON p.user_id = u.user_id
        """).fetchall()

        if not prompts_all_data:
            return []

        result = [{
            "id": prompt["prompts_id"],
            "user_id": prompt["user_id"],
            "name": prompt["prompt_name"],
            "prompt": prompt["prompt"],
            "questions_count": prompt["questions_count"],
            "questions_correct": prompt["questions_correct"],
            "date_created": prompt["date_created"],
            "user_name": prompt["user_name"]
        } for prompt in prompts_all_data]

        cursor.close()
        return result

    def add_prompt(self, user_id: int, prompt_name: str, prompt: str,
                  questions_count: int, questions_correct: int):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute(
            """
            INSERT INTO prompts (user_id, prompt_name, prompt, 
                               questions_count, questions_correct)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, prompt_name, prompt, questions_count, questions_correct)
        )

        con.commit()
        last_id = cur.lastrowid
        cur.close()

        return last_id

    def edit_prompt(self, prompts_id: int, user_id: int, prompt_name: str, prompt: str,
                   questions_count: int, questions_correct: int):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        try:
            cur.execute(
                """
                UPDATE prompts 
                SET user_id = ?,
                    prompt_name = ?, 
                    prompt = ?, 
                    questions_count = ?, 
                    questions_correct = ?
                WHERE prompts_id = ?
                """,
                (user_id, prompt_name, prompt, questions_count, questions_correct, prompts_id)
            )

            con.commit()
            rows_affected = cur.rowcount
            cur.close()

            return rows_affected > 0
        except Exception as e:
            print(f"Error editing prompt: {e}")
            return False

    def delete_prompt(self, prompts_id: int):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        try:
            cur.execute(
                """
                DELETE FROM prompts 
                WHERE prompts_id = ?
                """,
                (prompts_id,)
            )

            con.commit()
            rows_affected = cur.rowcount
            cur.close()

            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting prompt: {e}")
            return False

    def get_prompt(self, prompts_id: int):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        prompt_data = cursor.execute("""
            SELECT 
                p.*,
                u.display_name as user_name
            FROM prompts p
            LEFT JOIN users u ON p.user_id = u.user_id
            WHERE p.prompts_id = ?
        """, (prompts_id,)).fetchone()

        if not prompt_data:
            return None

        result = {
            "id": prompt_data["prompts_id"],
            "user_id": prompt_data["user_id"],
            "name": prompt_data["prompt_name"],
            "prompt": prompt_data["prompt"],
            "questions_count": prompt_data["questions_count"],
            "questions_correct": prompt_data["questions_correct"],
            "date_created": prompt_data["date_created"],
            "user_name": prompt_data["user_name"]
        }

        cursor.close()
        return result

    def get_all_users(self):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        users = cursor.execute("""
            SELECT user_id, display_name 
            FROM users 
            ORDER BY display_name
        """).fetchall()

        cursor.close()

        return [{"id": user["user_id"], "name": user["display_name"]} for user in users]
