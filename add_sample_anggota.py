# add_sample_anggota.py
"""Utility script to add sample Anggota entries to the database.
Run with: `python add_sample_anggota.py`
"""
import sys
import os
import uuid

# Ensure project root is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.db.database import SessionLocal
from backend.models.models import Anggota

sample_anggota = [
    {"nama": "Budi Santoso", "email": "budi@example.com", "password": "budi123", "jabatan": "Kapolsek", "pangkat": "Kompol", "NRP": 123456, "no_wa": "081234567890"},
    {"nama": "Siti Aminah", "email": "siti@example.com", "password": "siti123", "jabatan": "Kapolres", "pangkat": "Irjen Pol", "NRP": 234567, "no_wa": "081234567891"},
    {"nama": "Agus Prasetyo", "email": "agus@example.com", "password": "agus123", "jabatan": "Waka Polres", "pangkat": "Brigjen Pol", "NRP": 345678, "no_wa": "081234567892"},
    {"nama": "Dewi Lestari", "email": "dewi@example.com", "password": "dewi123", "jabatan": "Kabid Humas", "pangkat": "AKBP", "NRP": 456789, "no_wa": "081234567893"},
    {"nama": "Rudi Hartono", "email": "rudi@example.com", "password": "rudi123", "jabatan": "Staf / Admin", "pangkat": "Aipda", "NRP": 567890, "no_wa": "081234567894"},
]

def add_samples():
    db = SessionLocal()
    added = 0
    for ag in sample_anggota:
        exists = db.query(Anggota).filter(Anggota.email == ag["email"]).first()
        if not exists:
            new_ag = Anggota(
                id_anggota=str(uuid.uuid4())[:8],
                nama=ag["nama"],
                email=ag["email"],
                password=ag["password"],
                jabatan=ag["jabatan"],
                pangkat=ag["pangkat"],
                NRP=ag["NRP"],
                no_wa=ag["no_wa"],
            )
            db.add(new_ag)
            added += 1
    db.commit()
    db.close()
    print(f"Added {added} sample anggota entries.")

if __name__ == "__main__":
    add_samples()
