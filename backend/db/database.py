import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Gunakan environment variable untuk deployment (Railway/Vercel)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@localhost/presensi_polda")

# Fix untuk database Railway (biasanya menggunakan mysql://... perlu diubah ke mysql+mysqlconnector://)
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+mysqlconnector://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
