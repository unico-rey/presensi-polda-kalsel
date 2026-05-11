from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from backend.db.database import get_db
from backend.models.models import Absensi, Anggota, Pengaturan, Admin
from backend.services.scheduler import _send_push_to_anggota

router = APIRouter(prefix="/absensi", tags=["Absensi"])
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/", response_class=HTMLResponse)
def absensi_index(request: Request, db: Session = Depends(get_db)):
    semua_anggota = db.query(Anggota).order_by(Anggota.nama.asc()).all()
    settings = {s.kunci: s.nilai for s in db.query(Pengaturan).all()}
    return templates.TemplateResponse("absensi.html", {
        "request": request, 
        "semua_anggota": semua_anggota,
        "settings": settings
    })

@router.post("/submit")
async def absensi_submit(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    id_anggota = form.get("id_anggota")
    tipe_absen = form.get("tipe") # hadir, sakit, ijin, cuti, pulang_siang, pulang
    status_manual = form.get("status_manual") 
    lat = form.get("lat")
    lon = form.get("lon")
    foto = form.get("foto")
    tanda_tangan = form.get("tanda_tangan")
    
    ag = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
    if not ag: 
        return RedirectResponse("/absensi/?error=anggota_tidak_ditemukan", status_code=302)
    
    # --- GEOFENCING BACKEND VALIDATION ---
    settings_db = {s.kunci: s.nilai for s in db.query(Pengaturan).all()}
    is_geofence_active = settings_db.get("geofence_active", "1") == "1"
    
    if is_geofence_active and tipe_absen in ["hadir", "terlambat", "pulang_siang", "pulang"]:
        try:
            import math
            user_lat = float(lat)
            user_lon = float(lon)
            polda_lat = float(settings_db.get("polda_lat", "-3.488661"))
            polda_lon = float(settings_db.get("polda_lon", "114.831166"))
            max_radius = float(settings_db.get("geofence_radius", "200"))
            
            # Haversine
            R = 6371000 # meters
            phi1 = math.radians(polda_lat)
            phi2 = math.radians(user_lat)
            delta_phi = math.radians(user_lat - polda_lat)
            delta_lambda = math.radians(user_lon - polda_lon)
            
            a = math.sin(delta_phi/2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2.0)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = R * c
            
            if distance > max_radius:
                return RedirectResponse(f"/absensi/?error=Lokasi_Anda_berada_di_luar_radius_kantor_({int(distance)}m)", status_code=302)
        except Exception as e:
            return RedirectResponse("/absensi/?error=Gagal_memverifikasi_lokasi_GPS._Pastikan_GPS_menyala", status_code=302)
    # --------------------------------------

    now = datetime.now()
    today = now.date()
    
    rekam = db.query(Absensi).filter(Absensi.id_anggota == id_anggota, func.date(Absensi.tanggal) == today).first()
    
    if tipe_absen in ["pulang", "pulang_siang"]:
        if not rekam:
            return RedirectResponse("/absensi/?error=belum_absen_masuk", status_code=302)
        rekam.waktu_pulang = now
        rekam.foto_pulang = foto
        rekam.tanda_tangan_pulang = tanda_tangan
        if tipe_absen == "pulang_siang":
             rekam.keterangan = "Pulang Siang"
        db.commit()
        record_id = rekam.id

        # --- PUSH NOTIFICATION: Konfirmasi Absen Pulang ---
        try:
            label_pulang = "Pulang Siang" if tipe_absen == "pulang_siang" else "Pulang"
            _send_push_to_anggota(
                db=db,
                id_anggota=id_anggota,
                title=f"✅ Presensi {label_pulang} Berhasil",
                body=f"Yth. {ag.nama}, presensi kepulangan Anda telah tercatat pada pukul {now.strftime('%H:%M')} WITA. Terima kasih!"
            )
        except Exception:
            pass  # Jangan gagalkan absensi jika push notification error
        # ---------------------------------------------------
    else:
        if rekam:
            return RedirectResponse("/absensi/?error=sudah_absen_masuk", status_code=302)
            
        status = "Hadir"
        keterangan = ""
        if tipe_absen in ["sakit", "ijin", "cuti"]:
            status = tipe_absen.capitalize()
            keterangan = status_manual if status_manual else ""
        elif tipe_absen == "hadir":
            # check jam — bedakan Jumat dan hari biasa
            hari_ini = now.weekday()
            if hari_ini == 4:  # Jumat
                key_jam = "jam_masuk_jumat"
            else:
                key_jam = "jam_masuk_normal"
            jam_masuk = db.query(Pengaturan).filter(Pengaturan.kunci == key_jam).first()
            if jam_masuk and jam_masuk.nilai:
                try:
                    batas = datetime.strptime(jam_masuk.nilai, "%H:%M").time()
                    if now.time() > batas:
                        status = "Terlambat"
                except:
                    pass
        elif tipe_absen == "terlambat":
            status = "Terlambat"
                    
        baru = Absensi(
            id_anggota=id_anggota,
            status=status,
            keterangan=keterangan,
            latitude=lat,
            longitude=lon,
            foto=foto,
            tanda_tangan=tanda_tangan
        )
        db.add(baru)
        db.commit()
        db.refresh(baru)
        record_id = baru.id

        # --- PUSH NOTIFICATION: Konfirmasi Absen Masuk ---
        try:
            emoji_map = {"Hadir": "✅", "Terlambat": "⚠️", "Sakit": "🏥", "Ijin": "📋", "Cuti": "🗓️"}
            emoji = emoji_map.get(status, "✅")
            _send_push_to_anggota(
                db=db,
                id_anggota=id_anggota,
                title=f"{emoji} Presensi Masuk Berhasil — {status}",
                body=f"Yth. {ag.nama}, presensi kehadiran Anda ({status}) telah tercatat pada pukul {now.strftime('%H:%M')} WITA. Terima kasih!"
            )
        except Exception:
            pass  # Jangan gagalkan absensi jika push notification error
        # --------------------------------------------------
        
    if tipe_absen in ["pulang", "pulang_siang"]:
        return RedirectResponse(f"/absensi/detail/{record_id}?tipe=pulang", status_code=302)
    return RedirectResponse(f"/absensi/detail/{record_id}", status_code=302)

@router.get("/detail/{absensi_id}", response_class=HTMLResponse)
def absensi_detail_view(absensi_id: int, request: Request, tipe: str = None, db: Session = Depends(get_db)):
    ag = db.query(Absensi).filter(Absensi.id == absensi_id).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Data presensi tidak ditemukan")
        
    anggota_data = db.query(Anggota).filter(Anggota.id_anggota == ag.id_anggota).first()
    ag.anggota = anggota_data
    
    return templates.TemplateResponse("absensi_detail.html", {
        "request": request, 
        "absensi": ag,
        "tipe": tipe or "masuk"
    })
