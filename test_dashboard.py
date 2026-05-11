from backend.db.database import SessionLocal
from backend.models.models import Pegawai, Absensi
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import traceback

def test_dashboard_logic():
    db = SessionLocal()
    try:
        now = datetime.now()
        limit_date = now - timedelta(days=30)
        
        print("Testing delete query...")
        # db.query(Absensi).filter(Absensi.tanggal < limit_date).delete() # Jangan delete data beneran dulu
        
        print("Testing count queries...")
        jumlah_pegawai = db.query(Pegawai).count()
        jumlah_absensi = db.query(Absensi).count()
        print(f"Pegawai: {jumlah_pegawai}, Absensi: {jumlah_absensi}")

        print("Testing recent query join...")
        recent_query = db.query(Absensi, Pegawai.nama).join(
            Pegawai, Absensi.id_pegawai == Pegawai.id_pegawai
        ).order_by(Absensi.tanggal.desc()).limit(10).all()
        
        for absensi, nama in recent_query:
            print(f"Found: {nama}, Foto: {len(absensi.foto) if absensi.foto else 0}, TT: {len(absensi.tanda_tangan) if absensi.tanda_tangan else 0}")
            
        print("✅ Dashboard logic tests passed!")
    except Exception as e:
        print("❌ Dashboard logic test failed!")
        with open("error_log.txt", "w") as f:
            traceback.print_exc(file=f)
        print("Traceback written to error_log.txt")
    finally:
        db.close()

if __name__ == "__main__":
    test_dashboard_logic()
