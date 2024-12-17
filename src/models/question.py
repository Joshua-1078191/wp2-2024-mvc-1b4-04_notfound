from lib.database.db import get_db

class Question:
    def __init__(self, question, subject, grade, education, prompts_id, answer, taxonomy_id, questions_id=None):
        self.questions_id = questions_id
        self.question = question
        self.subject = subject
        self.grade = grade
        self.education = education
        self.prompts_id = prompts_id
        self.answer = answer
        self.taxonomy_id = taxonomy_id

    @staticmethod
    def get_all_questions():
        conn = get_db()
        try:
            query = '''
                SELECT 
                    q.questions_id,
                    q.question,
                    q.subject,
                    q.grade,
                    q.education,
                    p.prompt,
                    q.answer,
                    t.name as taxonomy,
                    q.prompts_id,
                    q.taxonomy_id
                FROM questions q
                LEFT JOIN prompts p ON q.prompts_id = p.prompts_id
                LEFT JOIN taxonomy t ON q.taxonomy_id = t.taxonomy_id
                ORDER BY q.questions_id
            '''
            return conn.execute(query).fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_by_id(questions_id):
        """Get a single question by ID"""
        conn = get_db()
        try:
            query = '''
                SELECT 
                    q.questions_id,
                    q.question,
                    q.subject,
                    q.grade,
                    q.education,
                    q.prompts_id,
                    q.answer,
                    q.taxonomy_id
                FROM questions q
                WHERE q.questions_id = ?
            '''
            row = conn.execute(query, (questions_id,)).fetchone()
            if row:
                return Question(
                    questions_id=row[0],
                    question=row[1],
                    subject=row[2],
                    grade=row[3],
                    education=row[4],
                    prompts_id=row[5],
                    answer=row[6],
                    taxonomy_id=row[7]
                )
            return None
        finally:
            conn.close()

    def save(self):
        """Create or update a question"""
        conn = get_db()
        try:
            if self.questions_id:
                # Update existing question
                query = '''
                    UPDATE questions 
                    SET question = ?, subject = ?, grade = ?, education = ?,
                        prompts_id = ?, answer = ?, taxonomy_id = ?
                    WHERE questions_id = ?
                '''
                params = (self.question, self.subject, self.grade, self.education,
                         self.prompts_id, self.answer, self.taxonomy_id, self.questions_id)
            else:
                # Create new question
                query = '''
                    INSERT INTO questions (question, subject, grade, education,
                                        prompts_id, answer, taxonomy_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                '''
                params = (self.question, self.subject, self.grade, self.education,
                         self.prompts_id, self.answer, self.taxonomy_id)
            
            cursor = conn.execute(query, params)
            conn.commit()
            
            if not self.questions_id:
                self.questions_id = cursor.lastrowid
            return True
        except Exception as e:
            print(f"Error saving question: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(questions_id):
        """Delete a question by ID"""
        conn = get_db()
        try:
            query = 'DELETE FROM questions WHERE questions_id = ?'
            conn.execute(query, (questions_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting question: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_all_taxonomies():
        """Get all taxonomies for the dropdown"""
        conn = get_db()
        try:
            query = 'SELECT taxonomy_id, name FROM taxonomy ORDER BY taxonomy_id'
            return conn.execute(query).fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_all_prompts():
        """Get all prompts for the dropdown"""
        conn = get_db()
        try:
            query = 'SELECT prompts_id, prompt_name, prompt FROM prompts ORDER BY prompts_id'
            return conn.execute(query).fetchall()
        finally:
            conn.close()
