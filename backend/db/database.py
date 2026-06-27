import os
import ssl
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

# Load environment variables from .env file (silent jika tidak ada)
load_dotenv()

# Gunakan environment variable untuk deployment (Railway/Vercel/Aiven)
# Default fallback hanya untuk development lokal
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost/presensi_polda")

# Normalize driver: pastikan selalu pakai pymysql
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
elif "mysqlconnector" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("mysql+mysqlconnector://", "mysql+pymysql://", 1)

# SSL configuration for Aiven or general SSL-required hosts
connect_args = {}
if "aivencloud.com" in DATABASE_URL or "ssl" in DATABASE_URL.lower():
    # Hapus parameter query ssl_mode dari string koneksi karena driver tidak menyukainya jika dilewatkan sebagai parameter URL.
    # Parameter ini akan ditangani secara manual via connect_args di bawah ini.
    parsed = urlparse(DATABASE_URL)
    q_params = [(k, v) for k, v in parse_qsl(parsed.query) if k.lower() != 'ssl_mode']
    DATABASE_URL = urlunparse(parsed._replace(query=urlencode(q_params)))

    # Konfigurasi SSL untuk PyMySQL
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connect_args = {"ssl": ctx}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,      # Auto-reconnect jika koneksi putus
    pool_recycle=300,         # Recycle koneksi setiap 5 menit
    pool_size=5,              # Pool size
    max_overflow=10           # Overflow connections
)
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
