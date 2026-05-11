import sqlite3

def check_sqlite():
    try:
        conn = sqlite3.connect('presensi.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables: {tables}")
        
        for table in tables:
            tname = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {tname}")
            count = cursor.fetchone()[0]
            print(f"Table '{tname}' has {count} rows.")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_sqlite()
