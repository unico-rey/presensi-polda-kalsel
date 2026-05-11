from sqlalchemy import text
from backend.db.database import engine

def migrate():
    with engine.connect() as conn:
        print("Checking for missing columns and renaming columns...")
        
        # 1. ABSENSI TABLE
        result = conn.execute(text("SHOW COLUMNS FROM absensi"))
        absensi_cols = [row[0] for row in result.fetchall()]
        
        if "id_pegawai" in absensi_cols and "id_anggota" not in absensi_cols:
            print("Renaming 'id_pegawai' to 'id_anggota' in 'absensi'...")
            try:
                conn.execute(text("ALTER TABLE absensi CHANGE id_pegawai id_anggota VARCHAR(30) NOT NULL"))
                conn.commit()
                print("Column 'id_pegawai' renamed in 'absensi'.")
            except Exception as e:
                print(f"Error renaming: {e}")
        
        # 2. CUTI TABLE
        result = conn.execute(text("SHOW COLUMNS FROM cuti"))
        cuti_cols = [row[0] for row in result.fetchall()]
        
        if "id_pegawai" in cuti_cols and "id_anggota" not in cuti_cols:
            print("Renaming 'id_pegawai' to 'id_anggota' in 'cuti'...")
            try:
                conn.execute(text("ALTER TABLE cuti CHANGE id_pegawai id_anggota VARCHAR(30) NOT NULL"))
                conn.commit()
                print("Column 'id_pegawai' renamed in 'cuti'.")
            except Exception as e:
                print(f"Error renaming: {e}")
        
        # 3. Add other missing columns to absensi
        columns_to_add = [
            ("tanda_tangan", "LONGTEXT NULL"),
            ("foto", "LONGTEXT NULL"),
            ("foto_pulang", "LONGTEXT NULL"),
            ("tanda_tangan_pulang", "LONGTEXT NULL"),
            ("latitude", "VARCHAR(50) NULL"),
            ("longitude", "VARCHAR(50) NULL")
        ]
        
        # Refresh existing columns list
        result = conn.execute(text("SHOW COLUMNS FROM absensi"))
        existing_columns = [row[0] for row in result.fetchall()]
        
        for col_name, col_type in columns_to_add:
            if col_name not in existing_columns:
                print(f"Adding column '{col_name}'...")
                try:
                    conn.execute(text(f"ALTER TABLE absensi ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                    print(f"Column '{col_name}' added.")
                except Exception as e:
                    print(f"Error adding column '{col_name}': {e}")
            else:
                print(f"Column '{col_name}' already exists.")

        # 4. Data Conversion: Standardize 'Ijin' to 'Izin' (Case Insensitive)
        print("Standardizing all variations of 'Ijin' to 'Izin'...")
        try:
            conn.execute(text("UPDATE absensi SET status = 'Izin' WHERE LOWER(status) = 'ijin'"))
            conn.commit()
            print("Status records standardized.")
        except Exception as e:
            print(f"Error during standardization: {e}")

if __name__ == "__main__":
    migrate()
