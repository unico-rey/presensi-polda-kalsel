from backend.db.database import SessionLocal
from backend.models.models import Absensi, Anggota
from datetime import datetime

def test_pulang():
    db = SessionLocal()
    try:
        anggota = db.query(Anggota).first()
        if anggota:
            print(f"Testing with anggota: {anggota.nama}")
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Check if Hadir exists
            existing = db.query(Absensi).filter(Absensi.id_anggota == anggota.id_anggota, Absensi.tanggal >= today_start).first()
            if not existing:
                print("Creating Hadir record first (simulating morning check-in)...")
                new_ab = Absensi(id_anggota=anggota.id_anggota, status="Hadir", waktu_masuk=datetime.now())
                db.add(new_ab)
                db.commit()
            else:
                print("Hadir record already exists.")
                
            # Simulate Pulang
            existing = db.query(Absensi).filter(Absensi.id_anggota == anggota.id_anggota, Absensi.tanggal >= today_start).order_by(Absensi.id.desc()).first()
            if existing:
                existing.waktu_pulang = datetime.now()
                db.commit()
                print(f"Set waktu_pulang to {existing.waktu_pulang}")
                
            # Query again to verify
            final = db.query(Absensi).filter(Absensi.id_anggota == anggota.id_anggota, Absensi.tanggal >= today_start).order_by(Absensi.id.desc()).first()
            print(f"Verification DB Record: status={final.status}, masuk={final.waktu_masuk}, pulang={final.waktu_pulang}")
        else:
            print("No anggota records found in database to test with.")
    finally:
        db.close()

if __name__ == "__main__":
    test_pulang()
