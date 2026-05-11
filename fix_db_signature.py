import mysql.connector
import sys
import os

# Menambahkan parent directory ke sys.path agar bisa import app
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from backend.db.database import DATABASE_URL
    # Parse DATABASE_URL: mysql+mysqlconnector://user:pass@host/db
    # kita butuh host, user, password, database
    # Contoh: mysql+mysqlconnector://root:password@localhost/polda_db
    
    clean_url = DATABASE_URL.replace("mysql+mysqlconnector://", "")
    user_pass, host_db = clean_url.split("@")
    user, password = user_pass.split(":")
    host, db_name = host_db.split("/")
    
    # Connect
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = conn.cursor()
    
    # Add column
    print("Menambahkan kolom 'tanda_tangan' ke tabel 'absensi'...")
    cursor.execute("ALTER TABLE absensi ADD COLUMN tanda_tangan LONGTEXT")
    
    conn.commit()
    print("✅ Berhasil menambahkan kolom 'tanda_tangan'.")
    
except mysql.connector.Error as err:
    if err.errno == 1060:
        print("⚠️ Kolom 'tanda_tangan' sudah ada.")
    else:
        print(f"❌ Error: {err}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
