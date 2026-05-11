from backend.db.database import SessionLocal, engine, Base
from backend.models.models import Absensi
from datetime import datetime

# Double check table creation
Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    print("Attempting to insert test record...")
    new_absensi = Absensi(
        id_pegawai="P001",
        status="Hadir",
        tanggal=datetime.now(),
        waktu_masuk=datetime.now(),
        keterangan="Test insertion"
    )
    db.add(new_absensi)
    db.commit()
    print("✅ Insertion successful!")
except Exception as e:
    print(f"❌ Insertion failed: {e}")
finally:
    db.close()
