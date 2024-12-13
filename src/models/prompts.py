import sqlite3

class Prompts:
    def __init__(self, db_path):
        self.db = db_path

    def get_all_prompts(self):
        #Voor Roos: Hier moet jouw functie komen te staan!

    def get_one_prompt(self, prompt_id):
        con = sqlite3.connect(self.db)

        cur = con.cursor()

        cur.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))

        cur.close()

        return cur.fetchone()

