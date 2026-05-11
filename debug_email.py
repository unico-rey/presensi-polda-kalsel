import sys
import os
import logging
logging.basicConfig(level=logging.INFO)

# Memastikan app dikenali
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

try:
    from backend.services.email_sender import send_email_notification, SMTP_EMAIL, SMTP_APP_PASSWORD
    print(f"Konfigurasi Email: {SMTP_EMAIL}")
    print(f"Karakter Sandi: {len(SMTP_APP_PASSWORD)} digit")
    if SMTP_EMAIL == "EMAIL_GMAIL_ANDA_DISINI@gmail.com":
        print("GAGAL: EMAIL MASIH DEFAULT BAWAAN KOSONG!")
    else:
        # Kita coba kirim tes email ke alamat yang sama dengan pengirim
        print(f"Mencoba mengirim email percobaan ke diri sendiri ({SMTP_EMAIL})...")
        res = send_email_notification(
            target_email=SMTP_EMAIL,
            subject="TES NOTIFIKASI POLDA KALSEL",
            content="Sukses! Jika Anda melihat ini, berarti konfigurasi SMTP App Password Anda sudah bisa bekerja!"
        )
        if res:
            print("SUKSES: Cek kotak masuk Anda!")
        else:
            print("GAGAL: Fungsi kembalikan nilai False, cek error di atas!")
except Exception as e:
    print(f"EXCEPTION SAAT DEBUG: {e}")
