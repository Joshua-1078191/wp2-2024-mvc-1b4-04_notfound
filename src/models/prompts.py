import sqlite3

from click import prompt

from src.utils.database import generate_query_params


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
            "questions_incorrect": prompt["questions_count"] - prompt["questions_correct"],
            "date_created": prompt["date_created"],
            "archived": prompt["archived"],
            "user_name": prompt["user_name"]
        } for prompt in prompts_all_data]

        cursor.close()
        return result

    def get_available_prompts(self):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        prompts_all_data = cursor.execute("""
            SELECT *
            FROM prompts
            WHERE prompts.archived == FALSE
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
            "questions_incorrect": prompt["questions_count"] - prompt["questions_correct"],
            "date_created": prompt["date_created"],
            "archived": prompt["archived"]
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

    def edit_prompt(self, prompts_id: int, user_id: int = None, prompt_name: str = None, prompt: str = None, questions_count: int = None, questions_correct: int = None, archived: bool = None):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # get query string and parameters
        query_params = generate_query_params(user_id=user_id, prompt_name=prompt_name, prompt=prompt, questions_count=questions_count, questions_correct=questions_correct, archived=archived)

        if not query_params:
            print(f"Error editing prompt: no new values provided")
            return False

        try:
            print(f"UPDATE prompts SET {query_params.query} WHERE prompts.prompts_id = ?")

            cur.execute(
                f"UPDATE prompts SET {query_params.query} WHERE prompts.prompts_id = ?",
                [*query_params.params, prompts_id]
            )

            con.commit()
            rows_affected = cur.rowcount
            cur.close()

            return rows_affected > 0
        except Exception as e:
            print(f"Error editing prompt: {e}")
            return False

    def add_prompt_question_result(self, prompts_id:int, is_correct:bool):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        try:
            cur.execute(
                f"UPDATE prompts SET questions_count = prompts.questions_count + 1, questions_correct = prompts.questions_correct + ? WHERE prompts.prompts_id = ?",
                [1 if is_correct else 0, prompts_id]
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
                AND prompts.questions_count == 0
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
            "archived": prompt_data["archived"],
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

    def copy_prompt(self, prompt_id: int):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        # Fetch the existing prompt
        cursor.execute("""
            SELECT user_id, prompt_name, prompt, questions_count, questions_correct
            FROM prompts WHERE prompts_id = ?
        """, (prompt_id,))
        prompt_data = cursor.fetchone()

        if not prompt_data:
            cursor.close()
            return None

        # Insert a new prompt with the same data
        cursor.execute("""
            INSERT INTO prompts (user_id, prompt_name, prompt, questions_count, questions_correct)
            VALUES (?, ?, ?, ?, ?)
        """, (prompt_data['user_id'], prompt_data['prompt_name'], prompt_data['prompt'],
              prompt_data['questions_count'], prompt_data['questions_correct']))

        con.commit()
        new_prompt_id = cursor.lastrowid
        cursor.close()
        return new_prompt_id
