from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.models.models import Anggota
from backend.schemas.schemas import AnggotaCreate, AnggotaOut

router = APIRouter(tags=["Anggota"])

templates = Jinja2Templates(directory="frontend/templates")


# ==========================================================
# ROUTE HALAMAN (HARUS DI ATAS ROUTE DINAMIS)
# ==========================================================

# Dashboard Anggota
@router.get("/dashboard/{id_anggota}", response_class=HTMLResponse)
def anggota_dashboard(id_anggota: str, request: Request, db: Session = Depends(get_db)):
    anggota = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
    if not anggota:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")

    return templates.TemplateResponse(
        "anggota_dashboard.html",
        {"request": request, "anggota": anggota}
    )


# Halaman Profil
@router.get("/profil/{id_anggota}", response_class=HTMLResponse)
def profil_anggota(id_anggota: str, request: Request, db: Session = Depends(get_db)):
    anggota = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
    if not anggota:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")

    return templates.TemplateResponse(
        "anggota_profil.html",
        {"request": request, "anggota": anggota}
    )


# Form Edit Anggota
@router.get("/edit/{id_anggota}", response_class=HTMLResponse)
def edit_anggota_form(id_anggota: str, request: Request, db: Session = Depends(get_db)):
    anggota = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
    if not anggota:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")

    return templates.TemplateResponse(
        "edit_anggota.html",
        {"request": request, "anggota": anggota}
    )


# Submit Edit Anggota
@router.post("/edit/{id_anggota}")
async def edit_anggota_submit(id_anggota: str, request: Request, db: Session = Depends(get_db)):
    form = await request.form()

    anggota = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
    if not anggota:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")

    anggota.nama = form.get("nama")
    anggota.email = form.get("email")
    anggota.jabatan = form.get("jabatan")
    anggota.pangkat = form.get("pangkat")

    db.commit()
    db.refresh(anggota)

    return RedirectResponse(
        url=f"/anggota/dashboard/{id_anggota}",
        status_code=302
    )


# Logout
@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie("user_email")
    return response


# Halaman Home Anggota
@router.get("/home", response_class=HTMLResponse)
def anggota_home():
    html = """
    <html>
        <head>
            <title>Halaman Anggota</title>
        </head>
        <body>
            <h1>Selamat Datang di Halaman Anggota 👨‍💼</h1>
            <p>Anda berhasil login sebagai Anggota.</p>
            <a href="/">Kembali</a>
        </body>
    </html>
    """
    return HTMLResponse(html)


# ==========================================================
# API CRUD ANGGOTA (JSON)
# ==========================================================

@router.post("/", response_model=AnggotaOut)
def create_anggota(data: AnggotaCreate, db: Session = Depends(get_db)):
    existing = db.query(Anggota).filter(Anggota.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email sudah digunakan")

    new_ag = Anggota(**data.dict())
    db.add(new_ag)
    db.commit()
    db.refresh(new_ag)
    return new_ag


@router.get("/", response_model=list[AnggotaOut])
def get_all_anggota(db: Session = Depends(get_db)):
    return db.query(Anggota).all()


# ==========================================================
# ROUTE DINAMIS (PALING BAWAH)
# ==========================================================

@router.get("/detail/{id_anggota}", response_model=AnggotaOut)
def get_anggota_by_id(id_anggota: str, db: Session = Depends(get_db)):
    ag = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")
    return ag


@router.put("/{id_anggota}", response_model=AnggotaOut)
def update_anggota(id_anggota: str, data: AnggotaCreate, db: Session = Depends(get_db)):
    ag = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")

    for key, value in data.dict().items():
        setattr(ag, key, value)

    db.commit()
    db.refresh(ag)
    return ag


@router.delete("/{id_anggota}")
def delete_anggota(id_anggota: str, db: Session = Depends(get_db)):
    ag = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")

    db.delete(ag)
    db.commit()
    return {"message": "Anggota berhasil dihapus"}

# ===============================
# PUSH NOTIFICATION WEB PUSH
# ===============================
from pydantic import BaseModel
from backend.models.models import PushSubscription
from backend.core.vapid import get_or_create_vapid_keys

class SubscribeData(BaseModel):
    endpoint: str
    keys: dict

@router.get("/push/vapid-public-key")
async def get_vapid_public_key(db: Session = Depends(get_db)):
    keys = get_or_create_vapid_keys(db)
    return {"public_key": keys["public"]}

@router.post("/push/subscribe-public")
async def subscribe_push_public(sub: SubscribeData, id_anggota: str, db: Session = Depends(get_db)):
    """Mendaftar push notification tanpa perlu login (hanya butuh id_anggota)."""
    anggota = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
    if not anggota:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")
        
    p256dh = sub.keys.get("p256dh")
    auth = sub.keys.get("auth")
    
    # Simpan atau update subscription
    existing = db.query(PushSubscription).filter(PushSubscription.endpoint == sub.endpoint).first()
    if existing:
        existing.id_anggota = anggota.id_anggota
        existing.p256dh = p256dh
        existing.auth = auth
    else:
        baru = PushSubscription(
            id_anggota=anggota.id_anggota,
            endpoint=sub.endpoint,
            p256dh=p256dh,
            auth=auth
        )
        db.add(baru)
    
    db.commit()
    return {"status": "success", "nama": anggota.nama}

