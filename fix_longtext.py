import sqlalchemy
from sqlalchemy import text
from backend.db.database import DATABASE_URL

def fix_schema():
    print("Attempting to fix LONGTEXT columns for foto and tanda_tangan...")
    engine = sqlalchemy.create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        try:
            print("Altering foto column to LONGTEXT...")
            connection.execute(text("ALTER TABLE absensi MODIFY COLUMN foto LONGTEXT"))
            print("Altering tanda_tangan column to LONGTEXT...")
            connection.execute(text("ALTER TABLE absensi MODIFY COLUMN tanda_tangan LONGTEXT"))
            connection.commit()
            print("Successfully updated columns.")
        except Exception as e:
            print(f"Error altering table: {e}")

if __name__ == "__main__":
    fix_schema()
