from pydantic import BaseModel

# ======= ADMIN =======

class AdminBase(BaseModel):
    id_admin: str
    nama: str
    email: str
    password: str

class AdminOut(AdminBase):
    class Config:
        from_attributes = True


# ======= ANGGOTA =======

class AnggotaBase(BaseModel):
    id_anggota: str
    nama: str
    email: str
    password: str
    jabatan: str | None = None
    pangkat: str | None = None
    NRP: int | None = None

class AnggotaCreate(AnggotaBase):
    pass

class AnggotaOut(AnggotaBase):
    class Config:
        from_attributes = True

# ======= ABSENSI =======

class AbsensiBase(BaseModel):
    id_anggota: str
    status: str
    keterangan: str | None = None

class AbsensiCreate(AbsensiBase):
    pass

class AbsensiOut(AbsensiBase):
    id: int
    tanggal: str
    waktu_masuk: str
    waktu_pulang: str | None = None

    class Config:
        from_attributes = True
