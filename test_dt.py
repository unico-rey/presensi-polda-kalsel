import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from backend.db.database import SessionLocal
from backend.models.models import Absensi
import pytz

db = SessionLocal()
last_absensi = db.query(Absensi).order_by(Absensi.id.desc()).first()
if last_absensi:
    print(f"waktu_masuk: {last_absensi.waktu_masuk}")
    print(f"tzinfo: {last_absensi.waktu_masuk.tzinfo}")
    
    # Try converting
    wita = pytz.timezone('Asia/Makassar')
    dt = last_absensi.waktu_masuk
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt).astimezone(wita)
    else:
        dt = dt.astimezone(wita)
    print(f"Converted: {dt}")
else:
    print("No absensi data")
