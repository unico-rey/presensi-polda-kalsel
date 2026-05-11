import sqlalchemy
from sqlalchemy import text
from backend.db.database import DATABASE_URL

def fix_schema():
    print("Attempting to fix database schema...")
    engine = sqlalchemy.create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        try:
            print("Checking if 'foto' column exists in 'absensi' table...")
            result = connection.execute(text("SHOW COLUMNS FROM absensi LIKE 'foto'"))
            column_exists = result.fetchone() is not None
            
            if not column_exists:
                print("Column 'foto' not found. Adding it now...")
                # LONGTEXT is enough for base64
                connection.execute(text("ALTER TABLE absensi ADD COLUMN foto LONGTEXT"))
                # In SQLAlchemy 2.0+ we need to commit manually for DDL if not in autocommit mode
                connection.execute(text("COMMIT"))
                print("✅ Successfully added 'foto' column to 'absensi' table.")
            else:
                print("✅ Column 'foto' already exists.")
                
        except Exception as e:
            print(f"❌ Error fixing schema: {e}")

if __name__ == "__main__":
    fix_schema()
