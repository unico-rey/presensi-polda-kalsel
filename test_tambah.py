import sys
import os
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from backend.db.database import SessionLocal
from backend.models.models import Anggota

try:
    db = SessionLocal()
    ag = Anggota(
        id_anggota=str(uuid.uuid4())[:8],
        nama="Test User",
        email="testtambah@example.com",
        password="test",
        jabatan="Waka Polres",
        pangkat="AKBP",
        NRP=None,
        no_wa=""
    )
    db.add(ag)
    db.commit()
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
