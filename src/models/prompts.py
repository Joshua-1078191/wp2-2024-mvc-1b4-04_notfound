import sqlite3


class Prompts:
    def __init__(self, db_path):
        self.db = db_path

    def prompt_all_view(self):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        prompt_all_data = cursor.execute("""SELECT * FROM prompts""").fetchall()

        if not prompt_all_data:
            return []

        result = [{
            "id": prompt_all["prompts_id"],
            "redacteur": prompt_all["user_id"],
            "name": prompt_all["prompt_name"],
            "prompt": prompt_all["prompt"],
            "categorised_questions": prompt_all["questions_count"],
            "correct_questions": prompt_all["questions_correct"],
            "creation_date": prompt_all["date_created"]
        } for prompt_all in prompt_all_data]

        con.commit()

        cursor.close()

        return result

    def get_one_prompt(self, prompt_id: int):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        prompt_data = cur.execute("""
        SELECT * FROM prompts WHERE prompts_id = ? LIMIT 1;
        """, (prompt_id,)).fetchone()

        if not prompt_data:
            return None

        result = {
            "prompt_id": prompt_data["prompts_id"],
            "redacteur": prompt_data["user_id"],
            "prompt_naam": prompt_data["prompt"],
            "categorised_questions": prompt_data["questions_count"],
            "correct_questions": prompt_data["questions_correct"],
            "creation_date": prompt_data["date_created"],
        }

        cur.close()

        return result

    def add_prompt(self, user_id: int, prompt_name: str, prompt: str, questions_count: int, questions_correct: int):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute(
            """
            INSERT INTO prompts (user_id, prompt_name, prompt, questions_count, questions_correct)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, prompt_name, prompt, questions_count, questions_correct)
        )

        con.commit()

        cur.close()

        if cur.lastrowid is None:
            return None

        return cur.lastrowid