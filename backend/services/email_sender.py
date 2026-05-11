import smtplib
import logging
from email.message import EmailMessage

# ==========================================
# KONFIGURASI EMAIL PENGIRIM (SMTP GMAIL)
# ==========================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# Masukkan alamat email admin pengirim
SMTP_EMAIL = "email_anda@gmail.com"
# Masukkan App Password (16 digit) dari Google Account Anda, BUKAN password login biasa
SMTP_APP_PASSWORD = "xxxxxxxxxxxxxxxx"

def send_email_notification(target_email: str, subject: str, content: str) -> bool:
    if not target_email or target_email.strip() == "":
        return False
        
    # Validasi setup awal
    if len(SMTP_APP_PASSWORD.replace(" ", "")) < 16:
        logging.warning("App Password Gmail belum diisi (masih bawaan) atau salah format! Pengiriman dibatalkan.")
        return False

    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = f"Sistem Presensi Polda Kalsel <{SMTP_EMAIL}>"
    msg['To'] = target_email

    try:
        # Koneksi ke Server SMTP Google
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() # Enkripsi keamanan TLS
        server.login(SMTP_EMAIL, SMTP_APP_PASSWORD.replace(" ", ""))
        
        # Kirim Pesan
        server.send_message(msg)
        server.quit()
        
        logging.info(f"Email pengingat berhasil dikirim ke {target_email}")
        return True
    except Exception as e:
        logging.error(f"Gagal mengirim email ke {target_email}: {e}")
        return False
