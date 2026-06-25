import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from backend.db.database import SessionLocal
from backend.models.models import Anggota

db = SessionLocal()
emails = [
    "budi@example.com", 
    "siti@example.com", 
    "agus@example.com", 
    "dewi@example.com", 
    "rudi@example.com"
]
deleted = db.query(Anggota).filter(Anggota.email.in_(emails)).delete(synchronize_session=False)
db.commit()
db.close()
print(f"Deleted {deleted} sample data")
