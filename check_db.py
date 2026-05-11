from backend.db.database import engine, Base
from backend.models.models import Absensi
import sys

try:
    print("Checking database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables initialized successfully (created if missing).")
except Exception as e:
    print(f"Error initializing tables: {e}")
    sys.exit(1)
