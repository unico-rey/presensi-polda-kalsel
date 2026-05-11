from fastapi import APIRouter, Request, Depends, Form, HTTPException, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
import uuid
from datetime import datetime
import json

from backend.db.database import get_db
from backend.models.models import Admin, Anggota, Absensi, Jabatan, Pangkat, Pengaturan, Cuti

router = APIRouter(tags=["Admin"])
templates = Jinja2Templates(directory="frontend/templates")

def check_admin(request: Request, db: Session):
    email = request.cookies.get("user_email")
    if not email: return False
    if email == "admin": return True
    return db.query(Admin).filter(Admin.email == email).first() is not None

@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    
    today = datetime.now().date()
    # counts
    absensi_today = db.query(Absensi).filter(func.date(Absensi.tanggal) == today).all()
    hadir = sum(1 for a in absensi_today if a.status.lower() == 'hadir')
    terlambat = sum(1 for a in absensi_today if a.status.lower() == 'terlambat')
    sakit = sum(1 for a in absensi_today if a.status.lower() == 'sakit')
    izin = sum(1 for a in absensi_today if a.status.lower() in ['izin', 'ijin'])
    
    total_anggota = db.query(Anggota).count()
    tidak_hadir = total_anggota - (hadir + terlambat + sakit + izin)
    
    counts = {
        "Hadir": hadir,
        "Terlambat": terlambat,
        "Sakit": sakit,
        "Izin": izin,
        "TidakHadirToday": max(0, tidak_hadir)
    }
    
    # recent 10 absensi
    recent = db.query(Absensi, Anggota.nama).join(Anggota, Absensi.id_anggota == Anggota.id_anggota)\
        .order_by(desc(Absensi.tanggal)).limit(10).all()
        
    recent_absensi = []
    for a, name in recent:
        recent_absensi.append({
            "waktu": a.waktu_masuk.strftime("%H:%M:%S") if a.waktu_masuk else "00:00",
            "tanggal": a.tanggal.strftime("%d-%m-%Y"),
            "foto": a.foto,
            "tanda_tangan": a.tanda_tangan,
            "latitude": a.latitude,
            "longitude": a.longitude,
            "nama": name,
            "id_anggota": a.id_anggota,
            "status": a.status
        })
        
    # recap efficiency dynamically based on current month's workdays up to today
    import calendar
    workdays_up_to_today = 0
    for day in range(1, today.day + 1):
        if datetime(today.year, today.month, day).weekday() < 5: # Monday(0) to Friday(4)
            workdays_up_to_today += 1
    workdays_up_to_today = max(1, workdays_up_to_today) # avoid div by zero

    recap_this = []
    semua_anggota = db.query(Anggota).all()
    for ang in semua_anggota:
        total_hadir_ang = db.query(Absensi).filter(
            Absensi.id_anggota == ang.id_anggota, 
            func.month(Absensi.tanggal) == today.month, 
            func.year(Absensi.tanggal) == today.year,
            Absensi.status.in_(['Hadir', 'Terlambat'])
        ).count()
        pct = min(100, int((total_hadir_ang / workdays_up_to_today) * 100))
        recap_this.append({"nama": ang.nama, "percentage": pct})
    recap_this.sort(key=lambda x: x["percentage"], reverse=True)

    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "counts": counts,
        "recent_absensi": recent_absensi,
        "recap_this": recap_this
    })

@router.get("/anggota", response_class=HTMLResponse)
def admin_anggota_view(request: Request, search: str = None, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    q = db.query(Anggota)
    if search:
        q = q.filter(Anggota.nama.ilike(f"%{search}%"))
    anggota = q.order_by(Anggota.nama.asc()).all()
    jabatans = db.query(Jabatan).all()
    pangkats = db.query(Pangkat).all()
    return templates.TemplateResponse("anggota_list.html", {"request": request, "anggota": anggota, "jabatans": jabatans, "pangkats": pangkats, "search": search or ""})

import uuid
import csv
from io import StringIO
from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse

@router.post("/anggota/tambah")
async def admin_tambah_anggota(request: Request, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    form = await request.form()
    
    nrp_val = form.get("NRP")
    ag = Anggota(
        id_anggota=str(uuid.uuid4())[:8],
        nama=form.get("nama"),
        email=form.get("email"),
        password=form.get("password"),
        jabatan=form.get("jabatan"),
        pangkat=form.get("pangkat"),
        NRP=int(nrp_val.strip()) if (nrp_val and nrp_val.strip().isdigit()) else None,
        no_wa=form.get("no_wa")
    )
    db.add(ag)
    db.commit()
    return RedirectResponse("/admin/anggota?msg=Anggota_berhasil_ditambahkan", status_code=302)

@router.post("/anggota/hapus")
async def admin_hapus_anggota(request: Request, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    form = await request.form()
    id_ag = form.get("id_anggota")
    
    ag = db.query(Anggota).filter(Anggota.id_anggota == id_ag).first()
    if ag:
        # Also delete absensi tied to thisanggota to maintain DB integrity if desired. 
        # But for now just deleting theanggota.
        db.delete(ag)
        db.commit()
    return RedirectResponse("/admin/anggota?msg=Anggota_berhasil_dihapus", status_code=302)

@router.get("/anggota/download-template")
def download_template(request: Request, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    
    csv_content = "Nama Lengkap,Email,Password,Pangkat,Jabatan,NRP,No WhatsApp\n"
    csv_content += "Joko Susilo,joko@polda.go.id,rahasia123,Kombes,Kapolda,1234567,081234567\n"
    
    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=template_anggota.csv"}
    )

@router.post("/anggota/import")
async def import_csv_anggota(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    
    content = await file.read()
    berhasil = 0
    gagal = 0
    error_msg = ""
    
    if file.filename.endswith(".xlsx"):
        import openpyxl
        import io
        try:
            wb = openpyxl.load_workbook(filename=io.BytesIO(content), data_only=True)
            ws = wb.active
            rows = list(ws.iter_rows(values_only=True))
            if len(rows) <= 1:
                return RedirectResponse("/admin/anggota?error=file_kosong", status_code=302)
            
            for index, row in enumerate(rows[1:]): # Skip header
                if not row or len(row) < 3 or not row[0]: # Minimal: nama, email, pass
                    continue
                try:
                    email_val = str(row[1]).strip() if len(row)>1 and row[1] else ""
                    if email_val:
                        existing = db.query(Anggota).filter(Anggota.email == email_val).first()
                        if existing:
                            continue
                            
                    nrp_val = None
                    if len(row) > 5 and row[5] is not None:
                        try:
                            nrp_val = int(float(row[5]))
                        except:
                            pass
                            
                    ag = Anggota(
                        id_anggota=str(uuid.uuid4())[:8],
                        nama=str(row[0]).strip(),
                        email=email_val,
                        password=str(row[2]).strip() if len(row)>2 and row[2] else "",
                        pangkat=str(row[3]).strip() if len(row)>3 and row[3] else "",
                        jabatan=str(row[4]).strip() if len(row)>4 and row[4] else "",
                        NRP=nrp_val,
                        no_wa=str(row[6]).strip() if len(row)>6 and row[6] is not None else ""
                    )
                    db.add(ag)
                    db.commit()
                    berhasil += 1
                except Exception as e:
                    db.rollback()
                    gagal += 1
                    error_msg = str(e)[:100] # Ambil sedikit cuplikan error
                    continue
        except Exception as e:
            return RedirectResponse(f"/admin/anggota?error=format_excel_error", status_code=302)
    else:
        try:
            decoded = content.decode("utf-8")
        except UnicodeDecodeError:
            try:
                decoded = content.decode("cp1252")
            except:
                return RedirectResponse("/admin/anggota?error=format_tidak_dikenali", status_code=302)
                
        # Coba deteksi delimiter (; atau ,)
        delimiter = ';' if ';' in decoded.split('\\n')[0] else ','
        f = StringIO(decoded)
        reader = csv.reader(f, delimiter=delimiter)
        try:
            header = next(reader)
        except:
            return RedirectResponse("/admin/anggota?error=file_kosong", status_code=302)
            
        for index, row in enumerate(reader):
            if len(row) < 3 or not row[0].strip(): # Minimal: nama, email, pass
                continue
            try:
                email_val = row[1].strip() if len(row)>1 else ""
                if email_val:
                    existing = db.query(Anggota).filter(Anggota.email == email_val).first()
                    if existing:
                        continue
                
                nrp_val = None
                if len(row) > 5 and row[5].strip().isdigit():
                    nrp_val = int(row[5].strip())
                        
                ag = Anggota(
                    id_anggota=str(uuid.uuid4())[:8],
                    nama=row[0].strip(),
                    email=email_val,
                    password=row[2].strip() if len(row)>2 else "",
                    pangkat=row[3].strip() if len(row)>3 else "",
                    jabatan=row[4].strip() if len(row)>4 else "",
                    NRP=nrp_val,
                    no_wa=row[6].strip() if len(row)>6 else ""
                )
                db.add(ag)
                db.commit()
                berhasil += 1
            except Exception as e:
                db.rollback()
                gagal += 1
                error_msg = str(e)[:100]
                continue
                
    import urllib.parse
    if berhasil == 0 and gagal > 0:
        return RedirectResponse(f"/admin/anggota?error=Gagal_semua._Contoh_error:_{urllib.parse.quote(error_msg)}", status_code=302)
    elif berhasil == 0:
        return RedirectResponse("/admin/anggota?error=Tidak_ada_data_valid_yang_ditemukan_di_file", status_code=302)
        
    return RedirectResponse(f"/admin/anggota?msg=Import_Selesai._{berhasil}_berhasil,_{gagal}_gagal.", status_code=302)

@router.get("/anggota/edit/{id_anggota}", response_class=HTMLResponse)

def admin_edit_anggota_form(id_anggota: str, request: Request, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    anggota = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
    jabatans = db.query(Jabatan).all()
    pangkats = db.query(Pangkat).all()
    if not anggota: return RedirectResponse("/admin/anggota", status_code=302)
    return templates.TemplateResponse("edit_anggota.html", {"request": request, "anggota": anggota, "jabatans": jabatans, "pangkats": pangkats})

@router.post("/anggota/edit/{id_anggota}")
async def admin_edit_anggota_submit(id_anggota: str, request: Request, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    form = await request.form()
    ag = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
    if ag:
        ag.nama = form.get("nama")
        ag.email = form.get("email")
        if form.get("password") and form.get("password").strip() != "":
            ag.password = form.get("password")
        ag.jabatan = form.get("jabatan")
        ag.pangkat = form.get("pangkat")
        nrp_val = form.get("NRP")
        ag.NRP = int(nrp_val.strip()) if (nrp_val and nrp_val.strip().isdigit()) else None
        ag.no_wa = form.get("no_wa")
        
        try:
            db.commit()
        except BaseException as e:
            db.rollback()
            import urllib.parse
            return RedirectResponse(f"/admin/anggota/edit/{id_anggota}?error={urllib.parse.quote('Gagal menyimpan: Email (atau NRP) sudah terdaftar pada anggota lain!')}", status_code=302)

    return RedirectResponse("/admin/anggota?msg=Perubahan_data_anggota_berhasil_disimpan", status_code=302)

@router.get("/master/jabatan", response_class=HTMLResponse)
def admin_master_jabatan(request: Request, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    jabatans = db.query(Jabatan).all()
    pangkats = db.query(Pangkat).all()
    return templates.TemplateResponse("admin_master_jabatan.html", {"request": request, "jabatans": jabatans, "pangkats": pangkats})

@router.post("/master/jabatan/tambah")
def tambah_jabatan(nama: str = Form(...), db: Session = Depends(get_db)):
    j = Jabatan(nama=nama)
    db.add(j)
    db.commit()
    return RedirectResponse("/admin/master/jabatan?msg=Jabatan_baru_berhasil_ditambahkan", status_code=302)

@router.post("/master/jabatan/hapus")
def hapus_jabatan(id: int = Form(...), db: Session = Depends(get_db)):
    j = db.query(Jabatan).filter(Jabatan.id == id).first()
    if j:
        db.delete(j)
        db.commit()
    return RedirectResponse("/admin/master/jabatan?msg=Jabatan_berhasil_dihapus", status_code=302)

@router.post("/master/pangkat/tambah")
def tambah_pangkat(nama: str = Form(...), db: Session = Depends(get_db)):
    p = Pangkat(nama=nama)
    db.add(p)
    db.commit()
    return RedirectResponse("/admin/master/jabatan?msg=Pangkat_baru_berhasil_ditambahkan", status_code=302)

@router.post("/master/pangkat/hapus")
def hapus_pangkat(id: int = Form(...), db: Session = Depends(get_db)):
    p = db.query(Pangkat).filter(Pangkat.id == id).first()
    if p:
        db.delete(p)
        db.commit()
    return RedirectResponse("/admin/master/jabatan?msg=Pangkat_berhasil_dihapus", status_code=302)

@router.get("/master/pengaturan", response_class=HTMLResponse)
def admin_master_pengaturan(request: Request, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    peng = db.query(Pengaturan).all()
    settings = {p.kunci: p.nilai for p in peng}
    return templates.TemplateResponse("admin_master_pengaturan.html", {"request": request, "settings": settings})

@router.post("/master/pengaturan/update")
async def update_pengaturan(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    for key, val in form.items():
        p = db.query(Pengaturan).filter(Pengaturan.kunci == key).first()
        if p:
            p.nilai = str(val)
        else:
            db.add(Pengaturan(kunci=key, nilai=str(val)))
    db.commit()
    return RedirectResponse("/admin/master/pengaturan?msg=Lokasi_dan_Radius_Kantor_berhasil_diperbarui!", status_code=302)

@router.post("/master/pengaturan/update-admin")
async def update_admin_credentials(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    new_email = form.get("admin_email", "admin")
    new_pass = form.get("admin_password", "1234")
    # Delete all existing admin records to ensure only one admin exists
    db.query(Admin).delete()
    # Create new admin with provided credentials
    admin = Admin(
        id_admin=str(uuid.uuid4())[:8],
        nama="admin",
        email=new_email,
        password=new_pass
    )
    db.add(admin)
    db.commit()
    import urllib.parse
    msg = "Kredensial Admin berhasil diperbarui!"
    return RedirectResponse(f"/admin/master/pengaturan?msg={urllib.parse.quote(msg)}", status_code=302)
    # Delete all existing admin records to ensure only one admin exists
    db.query(Admin).delete()
    # Create or update the admin record with new credentials
    if not admin:
        admin = Admin(
            id_admin=str(uuid.uuid4())[:8],
            nama="Administrator",
            email=new_email,
            password=new_pass or "123"
        )
        db.add(admin)
    else:
        admin.email = new_email
        if new_pass:
            admin.password = new_pass
    # Commit the changes
    db.commit()
    # Redirect with success message
    import urllib.parse
    msg = "Kredensial Admin berhasil diperbarui!"
    return RedirectResponse(f"/admin/master/pengaturan?msg={urllib.parse.quote(msg)}", status_code=302)

from backend.services.scheduler import _send_push_to_anggota, check_masuk_reminder, check_pulang_reminder

@router.get("/master/pengaturan/test-notif")
def test_push_notif(request: Request, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    
    anggota_list = db.query(Anggota).all()
    count = 0
    no_sub = 0
    for ag in anggota_list:
        sent = _send_push_to_anggota(
            db=db, 
            id_anggota=ag.id_anggota, 
            title="🔔 PENGUJIAN SISTEM NOTIFIKASI", 
            body=f"Yth. {ag.nama}, ini adalah pesan uji coba dari sistem Presensi Polda Kalsel. Jika Anda menerima ini, berarti notifikasi Anda aktif!"
        )
        if sent > 0:
            count += sent
        else:
            no_sub += 1
            
    import urllib.parse
    msg = f"Selesai! Notif terkirim ke {count} perangkat aktif. {no_sub} anggota belum subscribe notifikasi."
    return RedirectResponse(f"/admin/master/pengaturan?msg={urllib.parse.quote(msg)}", status_code=302)

@router.get("/master/pengaturan/trigger-reminder-masuk")
def trigger_reminder_masuk(request: Request, db: Session = Depends(get_db)):
    """Kirim reminder masuk SEKARANG ke semua anggota yang belum absen (tanpa cek jam)."""
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    import urllib.parse
    from sqlalchemy import func as sqlfunc
    from datetime import datetime as dt
    settings = {p.kunci: p.nilai for p in db.query(Pengaturan).all()}
    hari = dt.now().weekday()
    jam_masuk = settings.get("jam_masuk_jumat" if hari == 4 else "jam_masuk_normal", "08:00")
    
    today = dt.now().date()
    attended_ids = {a.id_anggota for a in db.query(Absensi).filter(sqlfunc.date(Absensi.tanggal) == today).all()}
    anggota_list = db.query(Anggota).all()
    count = 0
    for ag in anggota_list:
        if ag.id_anggota not in attended_ids:
            sent = _send_push_to_anggota(
                db=db,
                id_anggota=ag.id_anggota,
                title="⚠️ PENGINGAT: Batas Waktu Presensi Masuk",
                body=f"Yth. {ag.nama}, Anda belum melakukan presensi kehadiran hari ini. Batas jam masuk {jam_masuk} WITA. Segera presensi!"
            )
            if sent > 0:
                count += sent

    msg = f"Reminder masuk dikirim ke {count} perangkat. ({len(anggota_list) - len(attended_ids)} anggota belum absen)"
    return RedirectResponse(f"/admin/master/pengaturan?msg={urllib.parse.quote(msg)}", status_code=302)

@router.get("/master/pengaturan/trigger-reminder-pulang")
def trigger_reminder_pulang(request: Request, db: Session = Depends(get_db)):
    """Kirim reminder pulang SEKARANG ke semua yang belum absen pulang (tanpa cek jam)."""
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    import urllib.parse
    from sqlalchemy import func as sqlfunc
    from datetime import datetime as dt
    settings = {p.kunci: p.nilai for p in db.query(Pengaturan).all()}
    hari = dt.now().weekday()
    jam_pulang = settings.get("jam_pulang_jumat" if hari == 4 else "jam_pulang_normal", "15:00")

    today = dt.now().date()
    absensi_today = db.query(Absensi).filter(sqlfunc.date(Absensi.tanggal) == today).all()
    count = 0
    for ab in absensi_today:
        if ab.waktu_pulang is None:
            ag = db.query(Anggota).filter(Anggota.id_anggota == ab.id_anggota).first()
            if not ag: continue
            sent = _send_push_to_anggota(
                db=db,
                id_anggota=ag.id_anggota,
                title="🏠 PENGINGAT: Jangan Lupa Presensi Pulang",
                body=f"Yth. {ag.nama}, Anda belum melakukan presensi kepulangan hari ini. Batas jam pulang {jam_pulang} WITA."
            )
            if sent > 0:
                count += sent

    msg = f"Reminder pulang dikirim ke {count} perangkat."
    return RedirectResponse(f"/admin/master/pengaturan?msg={urllib.parse.quote(msg)}", status_code=302)

@router.get("/absensi", response_class=HTMLResponse)
def admin_absensi_list(request: Request, start_date: str = None, end_date: str = None, month: str = None, search: str = None, order: str = "desc", page: int = 1, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    q = db.query(Absensi, Anggota.nama, Anggota.pangkat, Anggota.no_wa).join(Anggota, Absensi.id_anggota == Anggota.id_anggota)
    if param := search:
        q = q.filter(Anggota.nama.ilike(f"%{param}%"))
    if start_date and end_date:
        q = q.filter(func.date(Absensi.tanggal) >= start_date, func.date(Absensi.tanggal) <= end_date)
    if month:
        m, y = month.split("-")[1], month.split("-")[0]
        q = q.filter(func.month(Absensi.tanggal) == m, func.year(Absensi.tanggal) == y)
    
    if order == "asc":
        q = q.order_by(asc(Absensi.tanggal))
    else:
        q = q.order_by(desc(Absensi.tanggal))
    
    # Pagination
    per_page = 20
    total = q.count()
    total_pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * per_page
    absensi_results = q.offset(offset).limit(per_page).all()
    
    filters = {"start_date": start_date, "end_date": end_date, "month": month, "search": search, "order": order}
    return templates.TemplateResponse("admin_absensi_list.html", {
        "request": request,
        "absensi": absensi_results,
        "filters": filters,
        "page": page,
        "total_pages": total_pages,
        "total": total,
        "per_page": per_page,
    })

@router.post("/absensi/bulk-delete")
async def bulk_delete_absensi(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    ids = form.getlist("absensi_ids")
    db.query(Absensi).filter(Absensi.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return RedirectResponse("/admin/absensi?msg=Data_absensi_berhasil_dihapus", status_code=302)

@router.get("/cuti", response_class=HTMLResponse)
def admin_cuti(request: Request, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    cuti_req = db.query(Cuti, Anggota.nama).join(Anggota, Cuti.id_anggota == Anggota.id_anggota).order_by(desc(Cuti.created_at)).all()
    anggota = db.query(Anggota).all()
    return templates.TemplateResponse("admin_cuti.html", {"request": request, "requests": cuti_req, "anggota": anggota})

@router.post("/cuti/tambah")
async def tambah_cuti(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    c = Cuti(
        id_anggota=form.get("id_anggota"),
        tanggal_mulai=form.get("tanggal_mulai"),
        tanggal_selesai=form.get("tanggal_selesai"),
        jenis_cuti=form.get("jenis_cuti"),
        keterangan=form.get("keterangan"),
        status="Disetujui"
    )
    db.add(c)
    db.commit()
    return RedirectResponse("/admin/cuti?msg=Pengajuan_cuti_berhasil_ditambahkan", status_code=302)

@router.post("/cuti/update-status")
def update_cuti_status(id_cuti: int = Form(...), status: str = Form(...), db: Session = Depends(get_db)):
    c = db.query(Cuti).filter(Cuti.id == id_cuti).first()
    if c:
        c.status = status
        db.commit()
    return RedirectResponse("/admin/cuti?msg=Status_cuti_berhasil_diperbarui", status_code=302)

@router.post("/cuti/hapus")
def hapus_cuti(id: int = Form(...), db: Session = Depends(get_db)):
    c = db.query(Cuti).filter(Cuti.id == id).first()
    if c:
        db.delete(c)
        db.commit()
    return RedirectResponse("/admin/cuti?msg=Data_cuti_berhasil_dihapus", status_code=302)

@router.get("/peta-absensi", response_class=HTMLResponse)
def admin_peta_absensi(request: Request, db: Session = Depends(get_db)):
    if not check_admin(request, db): return RedirectResponse("/auth/login")
    peng = {p.kunci: p.nilai for p in db.query(Pengaturan).all()}
    return templates.TemplateResponse("admin_map_view.html", {"request": request, "settings": peng})

@router.get("/api/live-locations")
def live_locations(db: Session = Depends(get_db)):
    # Tampilkan rekapan keseluruhan presensi, tidak per hari (dibatasi 1000 data terbaru agar tidak membebani peta)
    absensi_all = db.query(Absensi, Anggota.nama).join(Anggota, Absensi.id_anggota == Anggota.id_anggota)\
        .filter(Absensi.latitude != None, Absensi.longitude != None)\
        .order_by(desc(Absensi.tanggal)).limit(1000).all()
        
    markers = []
    for a, name in absensi_all:
        markers.append({
            "lat": float(a.latitude),
            "lon": float(a.longitude),
            "nama": name,
            "waktu": a.waktu_masuk.strftime("%H:%M:%S") if a.waktu_masuk else "00:00:00",
            "status": a.status,
            "foto": a.foto
        })
    return {"markers": markers}




