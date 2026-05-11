from backend.db.database import SessionLocal
from backend.models.models import PushSubscription

db = SessionLocal()
subs = db.query(PushSubscription).all()
print("Total Subscriptions:", len(subs))
for s in subs:
    print(f"- ID Anggota: {s.id_anggota}, Endpoint: {s.endpoint[:30]}...")
