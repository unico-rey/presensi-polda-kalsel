import sys
import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# MEMAKSA Python melihat folder utama SCANTOOLS-POLDA
current_dir = os.path.dirname(os.path.abspath(__file__)) # folder app
parent_dir = os.path.dirname(current_dir) # folder utama
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.routes import admin, anggota, auth, absensi

# ===============================
# DATABASE
# ===============================
from backend.db.database import Base, engine

from backend.services.scheduler import start_scheduler

# ===============================
# INIT FASTAPI
# ===============================
app = FastAPI(
    title="Sistem Absensi Polda Kalsel",
    description="Aplikasi Presensi Anggota Polri Polda Kalimantan Selatan",
    version="1.0"
)

@app.on_event("startup")
async def startup_event():
    start_scheduler()

# ===============================
# CREATE TABLES (AUTO)
# ===============================
Base.metadata.create_all(bind=engine)

# ===============================
# SERVICE WORKER (harus di root agar scope "/" bisa dikontrol)
# ===============================
@app.get("/sw.js", include_in_schema=False)
async def service_worker():
    sw_path = os.path.join(parent_dir, "frontend", "static", "sw.js")
    return FileResponse(
        sw_path,
        media_type="application/javascript",
        headers={"Service-Worker-Allowed": "/"}
    )

# ===============================
# STATIC FILES
# ===============================
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# ===============================
# REGISTER ROUTERS
# ===============================

# Auth
app.include_router(
    auth.router,
    tags=["Auth"]
)

# Admin
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"]
)

# Anggota
app.include_router(
    anggota.router,
    prefix="/anggota",
    tags=["Anggota"]
)

# Absensi
app.include_router(
    absensi.router,
    tags=["Absensi"]
)

# End of routers

# ===============================
# ROOT REDIRECT
# ===============================
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/absensi/")

# ===============================
# LOGOUT
# ===============================
@app.get("/logout", include_in_schema=False)
async def logout():
    response = RedirectResponse(url="/absensi/", status_code=302)
    response.delete_cookie("user_email")
    return response

