from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.sql import func
from backend.db.database import Base

class Admin(Base):
    __tablename__ = "admin"
    id_admin = Column(String(30), primary_key=True)
    nama = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

class Anggota(Base):
    __tablename__ = "anggota"
    id_anggota = Column(String(30), primary_key=True)
    nama = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    jabatan = Column(String(50))
    pangkat = Column(String(50))
    NRP = Column(Integer)
    no_wa = Column(String(20), nullable=True)

class Absensi(Base):
    __tablename__ = "absensi"

    id = Column(Integer, primary_key=True, index=True)
    id_anggota = Column(String(30), nullable=False)
    tanggal = Column(DateTime(timezone=True), server_default=func.now())
    waktu_masuk = Column(DateTime(timezone=True), server_default=func.now())
    waktu_pulang = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), nullable=False) # Hadir, Terlambat, Sakit, Ijin
    keterangan = Column(Text, nullable=True)
    foto = Column(Text(length=4294967295), nullable=True) # Base64 image data
    tanda_tangan = Column(Text(length=4294967295), nullable=True) # Base64 signature data
    foto_pulang = Column(Text(length=4294967295), nullable=True) # Base64 foto saat pulang
    tanda_tangan_pulang = Column(Text(length=4294967295), nullable=True) # Base64 TTD saat pulang
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)

class Jabatan(Base):
    __tablename__ = "jabatan"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100), unique=True, nullable=False)

class Pangkat(Base):
    __tablename__ = "pangkat"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100), unique=True, nullable=False)

class Pengaturan(Base):
    __tablename__ = "pengaturan"
    kunci = Column(String(50), primary_key=True)
    nilai = Column(Text, nullable=False)

class Cuti(Base):
    __tablename__ = "cuti"
    id = Column(Integer, primary_key=True, index=True)
    id_anggota = Column(String(30), nullable=False)
    tanggal_mulai = Column(DateTime, nullable=False)
    tanggal_selesai = Column(DateTime, nullable=False)
    jenis_cuti = Column(String(50), nullable=False) # Cuti Tahunan, Alasan Penting, dll
    keterangan = Column(Text, nullable=True)
    status = Column(String(20), default="Pending") # Pending, Disetujui, Ditolak
    created_at = Column(DateTime, server_default=func.now())

class PushSubscription(Base):
    __tablename__ = "push_subscription"
    id = Column(Integer, primary_key=True, index=True)
    id_anggota = Column(String(30), nullable=False)
    endpoint = Column(Text, nullable=False)
    p256dh = Column(String(100), nullable=False)
    auth = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
