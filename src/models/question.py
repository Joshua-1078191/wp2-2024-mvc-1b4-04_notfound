import sqlite3


class Questions:
    def __init__(self, db_path):
        self.db = db_path

    def questions_all_view(self):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        questions_all_data = cursor.execute("""
            SELECT 
                q.*,
                p.prompt as prompt_text,
                t.name as taxonomy_name
            FROM questions q
            LEFT JOIN prompts p ON q.prompts_id = p.prompts_id
            LEFT JOIN taxonomy t ON q.taxonomy_id = t.taxonomy_id
        """).fetchall()

        if not questions_all_data:
            return []

        result = [{
            "id": question["questions_id"],
            "question": question["question"],
            "subject": question["subject"],
            "grade": question["grade"],
            "education": question["education"],
            "prompts_id": question["prompts_id"],
            "answer": question["answer"],
            "taxonomy_id": question["taxonomy_id"],
            "prompt_text": question["prompt_text"],
            "taxonomy_name": question["taxonomy_name"]
        } for question in questions_all_data]

        con.commit()
        cursor.close()
        return result

    def add_question(self, question: str, subject: str, grade: str, education: str, 
                    prompts_id: int, answer: str, taxonomy_id: int):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute(
            """
            INSERT INTO questions (question, subject, grade, education, 
                                prompts_id, answer, taxonomy_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (question, subject, grade, education, prompts_id, answer, taxonomy_id)
        )

        con.commit()
        last_id = cur.lastrowid
        cur.close()

        return last_id

    def edit_question(self, questions_id: int, question: str, subject: str, grade: str, 
                     education: str, prompts_id: int, answer: str, taxonomy_id: int):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        try:
            cur.execute(
                """
                UPDATE questions 
                SET question = ?, 
                    subject = ?, 
                    grade = ?, 
                    education = ?,
                    prompts_id = ?, 
                    answer = ?, 
                    taxonomy_id = ?
                WHERE questions_id = ?
                """,
                (question, subject, grade, education, prompts_id, answer, taxonomy_id, questions_id)
            )

            con.commit()
            rows_affected = cur.rowcount
            cur.close()

            return rows_affected > 0
        except Exception as e:
            print(f"Error editing question: {e}")
            return False

    def delete_question(self, questions_id: int):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        try:
            cur.execute(
                """
                DELETE FROM questions 
                WHERE questions_id = ?
                """,
                (questions_id,)
            )

            con.commit()
            rows_affected = cur.rowcount
            cur.close()

            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting question: {e}")
            return False

    def get_question(self, questions_id: int):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        question_data = cursor.execute("""
            SELECT 
                q.*,
                p.prompt as prompt_text,
                t.name as taxonomy_name
            FROM questions q
            LEFT JOIN prompts p ON q.prompts_id = p.prompts_id
            LEFT JOIN taxonomy t ON q.taxonomy_id = t.taxonomy_id
            WHERE q.questions_id = ?
        """, (questions_id,)).fetchone()

        if not question_data:
            return None

        result = {
            "id": question_data["questions_id"],
            "question": question_data["question"],
            "subject": question_data["subject"],
            "grade": question_data["grade"],
            "education": question_data["education"],
            "prompts_id": question_data["prompts_id"],
            "answer": question_data["answer"],
            "taxonomy_id": question_data["taxonomy_id"],
            "prompt_text": question_data["prompt_text"],
            "taxonomy_name": question_data["taxonomy_name"]
        }

        cursor.close()
        return result
