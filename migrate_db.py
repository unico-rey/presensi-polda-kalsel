from sqlalchemy import text, inspect
from backend.db.database import engine

def migrate():
    inspector = inspect(engine)
    
    with engine.connect() as conn:
        print("Checking for missing columns and renaming columns (SQLite support)...")
        
        # 1. Check ABSENSI TABLE
        if "absensi" in inspector.get_table_names():
            columns = [c['name'] for c in inspector.get_columns("absensi")]
            
            # Rename logic (Manual for SQLite if needed, but usually we just add)
            if "id_pegawai" in columns and "id_anggota" not in columns:
                print("Note: 'id_pegawai' found. Renaming to 'id_anggota'...")
                # SQLite doesn't support RENAME COLUMN easily in older versions
                # For this local project, we'll try the simple ALTER if supported
                try:
                    conn.execute(text("ALTER TABLE absensi RENAME COLUMN id_pegawai TO id_anggota"))
                    conn.commit()
                    print("Column 'id_pegawai' renamed to 'id_anggota'.")
                except Exception as e:
                    print(f"Renaming failed (expected for old SQLite): {e}")
            
            # Add missing columns
            columns_to_add = [
                ("tanda_tangan", "TEXT"),
                ("foto", "TEXT"),
                ("latitude", "VARCHAR(50)"),
                ("longitude", "VARCHAR(50)")
            ]
            
            # Re-fetch columns after possible rename
            columns = [c['name'] for c in inspector.get_columns("absensi")]
            for col_name, col_type in columns_to_add:
                if col_name not in columns:
                    print(f"Adding column '{col_name}'...")
                    try:
                        conn.execute(text(f"ALTER TABLE absensi ADD COLUMN {col_name} {col_type}"))
                        conn.commit()
                        print(f"Column '{col_name}' added.")
                    except Exception as e:
                        print(f"Error adding column '{col_name}': {e}")
        
        # 2. Check CUTI TABLE (if exists)
        if "cuti" in inspector.get_table_names():
            columns = [c['name'] for c in inspector.get_columns("cuti")]
            if "id_pegawai" in columns and "id_anggota" not in columns:
                try:
                    conn.execute(text("ALTER TABLE cuti RENAME COLUMN id_pegawai TO id_anggota"))
                    conn.commit()
                except: pass

        # 3. Data Standardization
        print("Standardizing status records...")
        try:
            # SQLite uses LOWER() as well
            conn.execute(text("UPDATE absensi SET status = 'Izin' WHERE LOWER(status) = 'ijin'"))
            conn.commit()
            print("Status records standardized.")
        except Exception as e:
            print(f"Error during standardization: {e}")

if __name__ == "__main__":
    migrate()
