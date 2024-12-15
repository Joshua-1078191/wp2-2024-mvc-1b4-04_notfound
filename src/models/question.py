from lib.database.db import get_db
from datetime import datetime
import uuid

class Question:
    def __init__(self, questions_id, question, user_id, prompts_id, taxonomy_bloom=None, 
                 rtti=None, exported=False, date_created=None, niveau_jaar=None, vak=None):
        self.questions_id = questions_id
        self.question = question
        self.user_id = user_id
        self.prompts_id = prompts_id
        self.taxonomy_bloom = taxonomy_bloom
        self.rtti = rtti
        self.exported = exported
        self.date_created = datetime.strptime(date_created, '%Y-%m-%d %H:%M:%S') if isinstance(date_created, str) else date_created
        self.niveau_jaar = niveau_jaar
        self.vak = vak

    @staticmethod
    def get_all_questions():
        conn = get_db()
        try:
            # Join questions with users and prompts to get all required information
            questions = conn.execute('''
                SELECT q.questions_id, q.question, u.display_name, p.prompt, 
                       q.taxonomy_bloom, q.rtti, q.date_created
                FROM questions q
                LEFT JOIN users u ON q.user_id = u.user_id
                LEFT JOIN prompts p ON q.prompts_id = p.prompts_id
                ORDER BY q.date_created DESC
            ''').fetchall()
            return questions
        finally:
            conn.close()

    @staticmethod
    def get_questions_filtered(zoekwoord=None):
        conn = get_db()
        try:
            query = '''
                SELECT q.questions_id, q.question, u.display_name, p.prompt, 
                       q.taxonomy_bloom, q.rtti, q.date_created
                FROM questions q
                LEFT JOIN users u ON q.user_id = u.user_id
                LEFT JOIN prompts p ON q.prompts_id = p.prompts_id
                WHERE 1=1
            '''
            params = []

            if zoekwoord:
                query += ' AND (q.question LIKE ? OR u.display_name LIKE ? OR p.prompt LIKE ?)'
                params.extend([f'%{zoekwoord}%', f'%{zoekwoord}%', f'%{zoekwoord}%'])

            query += ' ORDER BY q.date_created DESC'

            questions = conn.execute(query, params).fetchall()
            return questions
        finally:
            conn.close()

    @staticmethod
    def create_question(question_text, prompt_text, user_id, taxonomy_bloom, rtti):
        conn = get_db()
        try:
            # First create the prompt
            cursor = conn.execute('''
                INSERT INTO prompts (user_id, prompt, questions_count, questions_correct)
                VALUES (?, ?, 0, 0)
            ''', (user_id, prompt_text))
            prompt_id = cursor.lastrowid
            
            # Then create the question
            cursor = conn.execute('''
                INSERT INTO questions (questions_id, prompts_id, user_id, question, taxonomy_bloom, rtti)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (str(uuid.uuid4()), prompt_id, user_id, question_text, taxonomy_bloom, rtti))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating question: {e}")
            return False
        finally:
            conn.close()
