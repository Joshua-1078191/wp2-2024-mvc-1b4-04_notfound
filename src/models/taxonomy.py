import sqlite3

class Taxonomy:
    def __init__(self, db_path):
        self.db = db_path

    def get_all_taxonomies(self):
        """Get all taxonomies for the dropdown"""
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        try:
            query = 'SELECT taxonomy_id, name FROM taxonomy ORDER BY taxonomy_id'
            taxonomies = con.execute(query).fetchall()
            result = {(taxonomy["taxonomy_id"], taxonomy["name"]) for taxonomy in taxonomies}
            return result
        finally:
            con.close()