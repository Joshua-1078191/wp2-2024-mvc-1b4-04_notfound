import sqlite3


class Prompts:
    def __init__(self, db_path):
        self.db = db_path

    def prompt_all_view(self):
        con = sqlite3.connect(self.db)
        cursor = con.cursor()

        cursor.execute("""SELECT * FROM prompts""")
        con.commit()

        return cursor.fetchall()

    def get_one_prompt(self, prompt_id: int):
        con = sqlite3.connect(self.db)

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

    def add_prompt(self, user_id: int, prompt: str, questions_count: int, questions_correct: int):
        con = sqlite3.connect(self.db)

        cur = con.cursor()

        cur.execute(
            """
            INSERT INTO prompts (user_id, prompt, questions_count, questions_correct)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, prompt, questions_count, questions_correct)
        )

        con.commit()

        cur.close()

        if cur.lastrowid is None:
            return None

        return cur.lastrowid
