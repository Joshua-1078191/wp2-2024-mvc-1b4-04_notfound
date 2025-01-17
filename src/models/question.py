import sqlite3

from src.utils.database import connect_database, generate_query_params


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
                p.prompt_name as prompt_name,
                t.name as taxonomy_name
            FROM questions q
            LEFT JOIN prompts p ON q.prompts_id = p.prompts_id
            LEFT JOIN taxonomy t ON q.taxonomy_id = t.taxonomy_id
        """).fetchall()

        if not questions_all_data:
            return []

        result = self.__translate_questions(questions_all_data)

        con.commit()
        cursor.close()
        return result

    def export_questions(self):
        conn, cursor = connect_database(self.db)

        # Fetch users
        questions = cursor.execute("""
            SELECT * FROM questions WHERE questions.exported = FALSE;
            """).fetchall()

        if questions:
            # Mark questions as exported
            cursor.executemany("""
            UPDATE questions SET exported = TRUE WHERE questions.questions_id = ?
            """, [(question["questions_id"],) for question in questions])

            conn.commit()

        conn.close()

        return self.__translate_questions(questions)

    def export_all_questions(self):
        conn, cursor = connect_database(self.db)

        # Fetch users
        questions = cursor.execute("""
            SELECT * FROM questions;
            """).fetchall()

        if questions:
            # Mark questions as exported
            cursor.executemany("""
            UPDATE questions SET exported = TRUE WHERE questions.questions_id = ?
            """, [(question["questions_id"],) for question in questions])

            conn.commit()

        conn.close()

        return self.__translate_questions(questions)

    def __translate_questions(self, questions):
        result = [{
            "id": question["questions_id"],
            "question": question["question"],
            "subject": question["subject"],
            "grade": question["grade"],
            "education": question["education"],
            "prompts_id": question["prompts_id"],
            "answer": question["answer"],
            "taxonomy_id": question["taxonomy_id"],
        } for question in questions]

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

    def add_questions(self, questions: list[dict[str, object]]):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        query = '''
                   INSERT INTO questions (questions_id, question, subject, grade, education, answer)
                   VALUES (?, ?, ?, ?, ?, ?)
               '''

        params = [(question.get("questions_id"), question.get("question"), question.get("subject"),
                   question.get("grade"), question.get("education"), question.get("answer")) for question in
                  questions]

        print(params)

        cur.executemany(query, params)
        con.commit()

    def edit_question(self, questions_id: str, question: str = None, subject: str = None, grade: str = None,
                     education: str = None, prompts_id: int = None, answer: str = None, taxonomy_id: int = None):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # get query string and parameters
        query_params = generate_query_params(question=question, subject=subject, grade=grade, education=education, prompts_id=prompts_id, answer=answer, taxonomy_id=taxonomy_id)

        try:
            cur.execute(
                f"UPDATE questions SET {query_params.query} WHERE questions_id = ?",
                [*query_params.params, questions_id]
            )
            con.commit()
            rows_affected = cur.rowcount
            cur.close()

            return rows_affected > 0
        except Exception as e:
            print(f"Error editing question: {e}")
            return False

    def delete_question(self, questions_id: str):
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

    def get_paginated_questions(self, page: int = 1, per_page: int = 10):
        """
        Fetches a paginated list of questions.

        :param page: The current page number.
        :param per_page: The number of questions per page.
        :return: A list of questions for the specified page.
        """
        offset = (page - 1) * per_page
        query = "SELECT * FROM questions LIMIT ? OFFSET ?"
        params = (per_page, offset)

        conn, cursor = connect_database(self.db)
        cursor.execute(query, params)
        questions = cursor.fetchall()
        cursor.close()
        conn.close()

        return self.__translate_questions(questions)
