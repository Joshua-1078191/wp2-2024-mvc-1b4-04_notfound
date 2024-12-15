from lib.database.db import get_db

def view_table_contents(table_name):
    conn = get_db()
    try:
        print(f"\n=== Contents of {table_name} table ===")
        cursor = conn.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cursor.description]
        print("Columns:", columns)
        
        rows = cursor.fetchall()
        print(f"\nFound {len(rows)} rows:")
        for row in rows:
            print(dict(row))
            
    except Exception as e:
        print(f"Error reading {table_name}: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    tables = ["users", "questions", "prompts"]
    for table in tables:
        view_table_contents(table)
