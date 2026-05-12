<div align="center">
  <img src="https://raw.githubusercontent.com/unico-rey/presensi-polda-kalsel/master/frontend/static/assets/img/logo-polda.png" alt="Logo Polda Kalsel" width="120" onerror="this.onerror=null; this.src='https://upload.wikimedia.org/wikipedia/commons/4/46/Logo_Polri.png'">

  # 🚔 Sistem Presensi Polda Kalsel
  
  **Aplikasi Manajemen Kehadiran Cerdas dengan Geofencing & Real-Time Monitoring**

  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
  [![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
  [![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
  [![UI/UX](https://img.shields.io/badge/UI/UX-Modern_Glassmorphism-FF69B4?style=for-the-badge)](https://github.com/unico-rey/presensi-polda-kalsel)
</div>

<br />

## 📖 Tentang Proyek
**Sistem Presensi Polda Kalsel** adalah solusi digital modern yang dirancang khusus untuk mengelola dan memantau kehadiran anggota Kepolisian Daerah Kalimantan Selatan secara akurat dan transparan. 

Dengan fokus pada keamanan dan kemudahan penggunaan, sistem ini mengintegrasikan validasi lokasi berbasis **Geofencing** dan sistem **Push Notification** otomatis untuk memberikan pengalaman presensi yang handal baik bagi anggota maupun administrator.

## ✨ Fitur Unggulan

- 📍 **Smart Geofencing:** Validasi lokasi presensi menggunakan formula *Haversine* tingkat tinggi untuk memastikan anggota berada dalam radius yang ditentukan dari kantor.
- 🔔 **Real-Time Push Notifications:** Notifikasi otomatis langsung ke perangkat anggota melalui standar VAPID setelah presensi berhasil dilakukan (Masuk/Pulang).
- 📊 **Dynamic Live Dashboard:** Pemantauan aktivitas presensi secara *real-time* dengan sistem auto-refresh data setiap 30 detik.
- 📈 **Chronological Event Stream:** Pencatatan kehadiran berbasis alur kronologis yang memudahkan pelacakan aktivitas harian anggota secara berurutan.
- 💎 **Premium UI/UX:** Antarmuka modern dengan estetika *Glassmorphism*, transisi halus, dan sistem modal detail yang informatif.
- 👥 **Advanced Management:** Manajemen data anggota lengkap (CRUD) dengan fitur import/export file CSV/Excel untuk efisiensi data.
- ⚙️ **Admin Control:** Panel pengaturan terpusat untuk mengontrol status Geofencing, radius lokasi, dan jadwal jam kerja.

## 🛠️ Arsitektur Teknologi

### Backend (The Engine)
- **FastAPI:** Framework Python asinkron berperforma tinggi untuk API yang responsif.
- **SQLAlchemy:** ORM modern untuk manajemen database yang aman dan terstruktur.
- **Uvicorn:** ASGI server untuk skalabilitas tinggi.

### Frontend (The Interface)
- **Vanilla JavaScript:** Logika frontend yang ringan dan cepat tanpa overhead framework besar.
- **Jinja2 Templates:** Rendering sisi server yang dinamis dan efisien.
- **Modern CSS:** Desain responsif dengan kombinasi utilitas modern untuk visual premium.
- **Leaflet.js:** Integrasi peta interaktif untuk pemetaan lokasi presensi anggota.

---

## 💻 Panduan Instalasi

### Prasyarat
- Python 3.9 atau versi terbaru
- Git installed (opsional)

### Cara Menjalankan (Rekomendasi)

Cukup gunakan file executable yang telah disediakan untuk setup otomatis:

1. **Clone/Download** repository ini.
2. Jalankan file **`run.bat`** (Windows).
3. Script akan otomatis:
   - Membuat Virtual Environment (`venv`).
   - Menginstal semua dependensi dari `requirements.txt`.
   - Menginisialisasi dan memigrasi Database.
   - Menjalankan server dan membuka browser secara otomatis.

### Jalur Manual
```bash
# Aktifkan virtual environment
python -m venv venv
venv\Scripts\activate

# Instal dependensi
pip install -r requirements.txt

# Inisialisasi Database
python check_db.py
python migrate_db.py

# Jalankan Server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🔐 Akses Administrator
Gunakan akun default berikut untuk mengelola sistem:
- **Halaman Admin:** `http://127.0.0.1:8000/admin/`
- **Username:** `admin`
- **Password:** `1234`

## 📸 Dokumentasi Antarmuka

<div align="center">
  <table style="width:100%">
    <tr>
      <td align="center" width="50%"><strong>Antarmuka Presensi (Mobile Ready)</strong></td>
      <td align="center" width="50%"><strong>Dashboard Monitoring Admin</strong></td>
    </tr>
    <tr>
      <td align="center">
        <img src="https://via.placeholder.com/400x250/0a192f/ffffff?text=Antarmuka+Presensi+Anggota" alt="Antarmuka Presensi">
        <br/><i>Validasi Geofencing & Foto Selfie</i>
      </td>
      <td align="center">
        <img src="https://via.placeholder.com/400x250/0a192f/ffffff?text=Dashboard+Live+Monitoring" alt="Dashboard Admin">
        <br/><i>Statistik & Alur Kronologis Real-time</i>
      </td>
    </tr>
  </table>
</div>

---

<div align="center">
  <p><i>Dikembangkan dengan ❤️ untuk kemajuan institusi Polda Kalsel.</i></p>
  <sub>© 2026 Presensi Polda Kalsel - Modern Attendance Solution</sub>
</div>
