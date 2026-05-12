import sys
import os

# Append current dir to sys.path so we can import app modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from backend.db.database import SessionLocal, engine
from backend.models.models import Base, Jabatan, Pangkat, Admin
import uuid

def seed_data():
    db = SessionLocal()
    
    # List pangkat Polri
    pangkats = [
        "Jenderal Pol", "Komjen Pol", "Irjen Pol", "Brigjen Pol",
        "Kombes Pol", "AKBP", "Kompol",
        "AKP", "Iptu", "Ipda",
        "Aiptu", "Aipda", "Bripka", "Brigpol", "Briptu", "Bripda",
        "Abrip", "Abriptu", "Abripda",
        "Bharaka", "Bharatu", "Bharada",
        "ASN / PNS"
    ]
    
    # List jabatan utama/umum
    jabatans = [
        "Kapolda", "Wakapolda", 
        "Irwasda", "Karo Ops", "Karo SDM", "Karo Rena", "Karo Log",
        "Dir Reskrimum", "Dir Reskrimsus", "Dir Resnarkoba", 
        "Dir Binmas", "Dir Samapta", "Dir Lantas", "Dir Intelkam", 
        "Dir Polairud", "Dir Pamobvit", "Dir Tahti",
        "Kabid Propam", "Kabid Humas", "Kabid Kum", "Kabid TIK", 
        "Kabid Dokkes", "Kabid Keu", "Kasi / Kaur",
        "Kapolres", "Waka Polres", "Kapolsek",
        "Penyidik", "Penyidik Pembantu", "Bintara", "Tamtama",
        "Staf / Admin"
    ]

    print("Menambahkan Pangkat...")
    for p_name in pangkats:
        exists = db.query(Pangkat).filter(Pangkat.nama == p_name).first()
        if not exists:
            db.add(Pangkat(nama=p_name))
            
    print("Menambahkan Jabatan...")
    for j_name in jabatans:
        exists = db.query(Jabatan).filter(Jabatan.nama == j_name).first()
        if not exists:
            db.add(Jabatan(nama=j_name))
            
    print("Menambahkan/Update Admin Default...")
    admin = db.query(Admin).first()
    if not admin:
        admin = Admin(
            id_admin=str(uuid.uuid4())[:8],
            nama="Administrator",
            email="admin",
            password="1234"
        )
        db.add(admin)
        print("Admin default (admin/1234) berhasil ditambahkan.")
    else:
        admin.email = "admin"
        admin.password = "1234"
        print("Admin default berhasil diperbarui menjadi admin/1234.")

    try:
        db.commit()
        print("Selesai! Berhasil menambahkan semua data master Pangkat dan Jabatan.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
