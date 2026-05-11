from sqlalchemy import create_engine, text
from backend.db.database import DATABASE_URL

def migrate():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE absensi ADD COLUMN waktu_pulang DATETIME NULL;"))
            conn.commit()
            print("Successfully added waktu_pulang column to absensi table.")
        except Exception as e:
            print("Error or already exists:", e)

if __name__ == "__main__":
    migrate()
