from fastapi import APIRouter, Request, Form, Depends
# Tambahkan HTMLResponse di bawah ini
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.models.models import Admin, Anggota
from backend.core.templates import templates

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_action(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
): 
    # Hardcoded admin fallback removed; authentication now uses only DB records

    # 2. Cek Login Admin (Berdasarkan Database)
    admin = db.query(Admin).filter(
        Admin.email == email,
        Admin.password == password
    ).first()
    if admin:
        response = RedirectResponse(url="/admin/dashboard", status_code=302)
        response.set_cookie(key="user_email", value=admin.email, httponly=True)
        return response

    # 3. Login Anggota (Berdasarkan Database: Email atau NRP)
    # Coba cari berdasarkan Email atau NRP
    anggota = db.query(Anggota).filter(
        (Anggota.email == email) | (Anggota.NRP == email),
        Anggota.password == password
    ).first()

    if anggota:
        response = RedirectResponse(url="/absensi/", status_code=302)
        response.set_cookie(key="user_email", value=anggota.email, httponly=True)
        return response

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Username atau password salah"}
    )