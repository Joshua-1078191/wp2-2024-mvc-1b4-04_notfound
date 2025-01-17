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
            result = {taxonomy["taxonomy_id"]: taxonomy["name"] for taxonomy in taxonomies}
            return result
        finally:
            con.close()

    def get_filtered_taxonomies(self, taxonomy_id):
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        taxonomies = cursor.execute("""
        SELECT * FROM taxonomy WHERE taxonomy_id = ?""", taxonomy_id).fetchall()

        cursor.close()
        con.close()

        return taxonomies

    def get_all_taxonomies_with_limit(self, limit: int, offset: int):
        """Get all taxonomies for the dropdown"""
        con = sqlite3.connect(self.db)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        limit = int(limit)
        offset = int(offset)

        taxonomies_with_limit = cursor.execute("""
        SELECT taxonomy_id, name FROM taxonomy ORDER BY taxonomy_id LIMIT ? OFFSET ?
        """, (limit, offset)).fetchall()

        result = [{
            "taxonomy_id" : taxonomies_with_limit["taxonomy_id"],
            "name" : taxonomies_with_limit["name"]
        } for taxonomies_with_limit in taxonomies_with_limit]

        con.close()

        return result

