import os
import ssl
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

# Load environment variables from .env file
load_dotenv()

# Gunakan environment variable untuk deployment (Railway/Vercel/Aiven)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@localhost/presensi_polda")

# Fix untuk database Railway (biasanya menggunakan mysql://... perlu diubah ke mysql+mysqlconnector://)
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+mysqlconnector://", 1)

# SSL configuration for Aiven or general SSL-required hosts
connect_args = {}
if "aivencloud.com" in DATABASE_URL or "ssl" in DATABASE_URL.lower():
    # Hapus parameter query ssl_mode dari string koneksi karena driver tidak menyukainya jika dilewatkan sebagai parameter URL.
    # Parameter ini akan ditangani secara manual via connect_args di bawah ini.
    parsed = urlparse(DATABASE_URL)
    q_params = [(k, v) for k, v in parse_qsl(parsed.query) if k.lower() != 'ssl_mode']
    DATABASE_URL = urlunparse(parsed._replace(query=urlencode(q_params)))

    if "pymysql" in DATABASE_URL:
        # Konfigurasi SSL untuk PyMySQL
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        connect_args = {"ssl": ctx}
    else:
        # Konfigurasi SSL untuk mysql-connector-python
        connect_args = {
            "ssl_verify_cert": False,
            "ssl_disabled": False
        }

try:
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
except Exception as e:
    print(f"DATABASE CONNECTION ERROR: {e}")
    # Fallback to sqlite if connection fails so the app doesn't crash entirely
    engine = create_engine("sqlite:///./presensi.db", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
