from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import func
from datetime import datetime, timedelta
import logging
import json

from backend.db.database import SessionLocal
from backend.models.models import Anggota, Absensi, Pengaturan, PushSubscription
from backend.core.vapid import send_push_notification

scheduler = BackgroundScheduler(timezone="Asia/Makassar")

def _get_settings(db):
    """Ambil semua pengaturan dari DB sebagai dict."""
    peng = db.query(Pengaturan).all()
    return {p.kunci: p.nilai for p in peng}

def _get_jam_kerja(settings, hari_ini):
    """Ambil jam masuk & pulang berdasarkan hari (Senin-Kamis vs Jumat)."""
    if hari_ini == 4:  # Friday (0=Mon, 4=Fri)
        masuk_key = "jam_masuk_jumat"
        pulang_key = "jam_pulang_jumat"
        masuk_default = "07:00"
        pulang_default = "15:30"
    else:
        masuk_key = "jam_masuk_normal"
        pulang_key = "jam_pulang_normal"
        masuk_default = "08:00"
        pulang_default = "15:00"

    jam_masuk = settings.get(masuk_key, "") or settings.get("jam_masuk", "") or masuk_default
    jam_pulang = settings.get(pulang_key, "") or pulang_default

    return jam_masuk.strip(), jam_pulang.strip()


def _send_push_to_anggota(db, id_anggota, title, body):
    """Kirim Web Push notification ke semua device milik anggota tertentu."""
    subscriptions = db.query(PushSubscription).filter(
        PushSubscription.id_anggota == id_anggota
    ).all()

    payload = json.dumps({"title": title, "body": body})
    sent_count = 0

    for sub in subscriptions:
        subscription_info = {
            "endpoint": sub.endpoint,
            "keys": {
                "p256dh": sub.p256dh,
                "auth": sub.auth
            }
        }
        try:
            send_push_notification(subscription_info, payload, db)
            logging.info(f"Push notification berhasil dikirim ke {id_anggota}")
            sent_count += 1
        except Exception as e:
            logging.error(f"Gagal kirim push ke {id_anggota}: {e}")
            # Hapus subscription yang sudah expired/invalid (410 Gone)
            if "410" in str(e) or "404" in str(e):
                db.delete(sub)
                db.commit()
                logging.info(f"Subscription expired dihapus untuk {id_anggota}")

    return sent_count


def check_masuk_reminder():
    """Cek dan kirim notifikasi sebelum JAM MASUK."""
    db = SessionLocal()
    try:
        now = datetime.now()
        hari_ini = now.weekday()

        # Skip weekend (Sabtu=5, Minggu=6)
        if hari_ini >= 5:
            return

        settings = _get_settings(db)
        jam_masuk, _ = _get_jam_kerja(settings, hari_ini)

        # Cek apakah notifikasi aktif
        push_active = settings.get("notif_push_active", "1") == "1"
        if not push_active:
            logging.info("[MASUK] Notifikasi dimatikan, skip.")
            return

        # Ambil menit pengingat (default 30)
        try:
            menit_sebelum = int(settings.get("notif_menit_sebelum", "30"))
        except (ValueError, TypeError):
            menit_sebelum = 30

        try:
            jm_time = datetime.strptime(jam_masuk, "%H:%M").time()
        except Exception:
            logging.error(f"[MASUK] Format jam masuk tidak valid: {jam_masuk}")
            return

        target_time = now.replace(hour=jm_time.hour, minute=jm_time.minute, second=0, microsecond=0)
        reminder_time = target_time - timedelta(minutes=menit_sebelum)

        # Window ±2 menit agar tidak mudah terlewat
        delta_menit = abs((now - reminder_time).total_seconds() / 60)
        logging.info(f"[MASUK] now={now.strftime('%H:%M')}, reminder={reminder_time.strftime('%H:%M')}, delta={delta_menit:.1f} menit")

        if delta_menit <= 2:
            today = now.date()

            # Cari siapa yang belum absen masuk hari ini
            absensi_today = db.query(Absensi).filter(func.date(Absensi.tanggal) == today).all()
            attended_ids = {a.id_anggota for a in absensi_today}

            anggota_list = db.query(Anggota).all()
            notified = 0
            for ag in anggota_list:
                if ag.id_anggota not in attended_ids:
                    title = "⚠️ PEMBERITAHUAN: Batas Waktu Presensi Masuk"
                    body = f"Yth. {ag.nama}, waktu tersisa {menit_sebelum} menit sebelum batas jam masuk ({jam_masuk} WITA). Mohon segera melakukan presensi kehadiran Anda melalui sistem."
                    sent = _send_push_to_anggota(db, ag.id_anggota, title, body)
                    if sent > 0:
                        notified += 1
                        logging.info(f"[MASUK] Notif terkirim ke {ag.nama} ({sent} device)")
                    else:
                        logging.warning(f"[MASUK] {ag.nama} belum subscribe push notification")

            logging.info(f"[MASUK] Reminder selesai: {notified} anggota berhasil dikirim dari {len(anggota_list)} total.")
        else:
            logging.debug(f"[MASUK] Belum waktunya trigger (delta {delta_menit:.1f} menit).")

    except Exception as e:
        logging.error(f"Error di check_masuk_reminder: {e}")
    finally:
        db.close()


def check_pulang_reminder():
    """Cek dan kirim notifikasi sebelum JAM PULANG."""
    db = SessionLocal()
    try:
        now = datetime.now()
        hari_ini = now.weekday()

        # Skip weekend
        if hari_ini >= 5:
            return

        settings = _get_settings(db)
        _, jam_pulang = _get_jam_kerja(settings, hari_ini)

        # Cek apakah notifikasi aktif
        push_active = settings.get("notif_push_active", "1") == "1"
        if not push_active:
            return

        # Ambil menit pengingat (default 30)
        try:
            menit_sebelum = int(settings.get("notif_menit_sebelum", "30"))
        except (ValueError, TypeError):
            menit_sebelum = 30

        try:
            jp_time = datetime.strptime(jam_pulang, "%H:%M").time()
        except Exception:
            logging.error(f"[PULANG] Format jam pulang tidak valid: {jam_pulang}")
            return

        target_time = now.replace(hour=jp_time.hour, minute=jp_time.minute, second=0, microsecond=0)
        reminder_time = target_time - timedelta(minutes=menit_sebelum)

        # Window ±2 menit agar tidak mudah terlewat
        delta_menit = abs((now - reminder_time).total_seconds() / 60)
        logging.info(f"[PULANG] now={now.strftime('%H:%M')}, reminder={reminder_time.strftime('%H:%M')}, delta={delta_menit:.1f} menit")

        if delta_menit <= 2:
            today = now.date()

            # Cari siapa yang sudah absen masuk tapi BELUM absen pulang
            absensi_today = db.query(Absensi).filter(func.date(Absensi.tanggal) == today).all()
            notified = 0

            for ab in absensi_today:
                if ab.waktu_pulang is None:
                    ag = db.query(Anggota).filter(Anggota.id_anggota == ab.id_anggota).first()
                    if not ag:
                        continue

                    title = "🏠 PEMBERITAHUAN: Waktu Presensi Pulang"
                    body = f"Yth. {ag.nama}, waktu tersisa {menit_sebelum} menit sebelum batas jam pulang ({jam_pulang} WITA). Mohon segera melakukan presensi kepulangan Anda melalui sistem."

                    sent = _send_push_to_anggota(db, ag.id_anggota, title, body)
                    if sent > 0:
                        notified += 1
                        logging.info(f"[PULANG] Notif terkirim ke {ag.nama} ({sent} device)")
                    else:
                        logging.warning(f"[PULANG] {ag.nama} belum subscribe push notification")

            logging.info(f"[PULANG] Reminder selesai: {notified} anggota berhasil dikirim.")
        else:
            logging.debug(f"[PULANG] Belum waktunya trigger (delta {delta_menit:.1f} menit).")

    except Exception as e:
        logging.error(f"Error di check_pulang_reminder: {e}")
    finally:
        db.close()


def start_scheduler():
    # Job 1: Cek reminder masuk setiap menit (pagi)
    scheduler.add_job(
        func=check_masuk_reminder,
        trigger=CronTrigger(minute="*"),
        id="attendance_masuk_reminder",
        name="Reminder sebelum masuk",
        replace_existing=True
    )

    # Job 2: Cek reminder pulang setiap menit (siang/sore)
    scheduler.add_job(
        func=check_pulang_reminder,
        trigger=CronTrigger(minute="*"),
        id="attendance_pulang_reminder",
        name="Reminder sebelum pulang",
        replace_existing=True
    )

    scheduler.start()
    logging.info("✅ Scheduler notifikasi presensi started (masuk + pulang)")
