import sqlite3
import sys
import os

def migrate():
    db_path = "presensi.db"
    
    if not os.path.exists(db_path):
        print(f"[!] Database {db_path} tidak ditemukan.")
        sys.exit(1)
        
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Check if the column already exists
        c.execute("PRAGMA table_info(anggota)")
        columns = [row[1] for row in c.fetchall()]
        if "no_wa" not in columns:
            print("[+] Menambahkan kolom no_wa ke tabel anggota...")
            c.execute("ALTER TABLE anggota ADD COLUMN no_wa VARCHAR(20) DEFAULT NULL")
            conn.commit()
            print("[✓] Kolom no_wa berhasil ditambahkan.")
        else:
            print("[i] Kolom no_wa sudah ada, tidak perlu migrasi.")
            
        conn.close()
    except Exception as e:
        print(f"[!] Gagal migrasi: {e}")

if __name__ == "__main__":
    migrate()
