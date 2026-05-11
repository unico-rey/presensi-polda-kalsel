<div align="center">
  <img src="https://raw.githubusercontent.com/unico-rey/presensi-polda-kalsel/master/frontend/static/assets/img/logo-polda.png" alt="Logo Polda Kalsel" width="120" onerror="this.onerror=null; this.src='https://upload.wikimedia.org/wikipedia/commons/4/46/Logo_Polri.png'">

  # 🚔 Sistem Presensi Polda Kalsel
  
  **Aplikasi Presensi Cerdas dengan Geofencing & Real-Time Notifikasi**

  [![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
  [![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
  [![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
</div>

<br />

## 📖 Tentang Proyek
**Sistem Presensi Polda Kalsel** adalah aplikasi absensi modern yang dibangun khusus untuk memudahkan monitoring data presensi anggota Kepolisian Daerah Kalimantan Selatan. Aplikasi ini memanfaatkan teknologi Geofencing untuk validasi lokasi absen dan sistem Push Notification (VAPID) untuk notifikasi realtime.

Dilengkapi dengan Dashboard Admin yang intuitif untuk manajemen data anggota, pemantauan kehadiran, dan pengaturan radius absensi.

## ✨ Fitur Utama
- 📍 **Geofencing Location:** Validasi jarak absensi berdasarkan titik koordinat yang ditentukan (Haversine formula).
- 🔔 **Push Notifications:** Pemberitahuan real-time langsung ke perangkat saat ada yang melakukan absensi.
- 📱 **Responsive Design:** Tampilan antarmuka yang optimal diakses dari smartphone maupun desktop.
- 👥 **Manajemen Anggota:** Fitur lengkap (CRUD) untuk mengelola data personel.
- 📊 **Dashboard Monitoring:** Ringkasan statistik kehadiran harian secara visual.
- 📥 **Export/Import Data:** Dukungan pengolahan data anggota melalui file CSV/Excel.
- 🚀 **Performa Cepat:** Backend dibangun menggunakan FastAPI untuk respons yang asinkron dan sangat cepat.

## 🛠️ Teknologi yang Digunakan
* **Backend:** Python, FastAPI, Uvicorn
* **Database:** SQLite (SQLAlchemy ORM)
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Jinja2 Templates, Bootstrap
* **Lainnya:** Vapid (Web Push), Geolocation API

---

## 💻 Cara Instalasi & Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan project ini di komputer lokal Anda.

### Prasyarat
- Python 3.9 atau lebih baru
- Git

### Langkah Instalasi

1. **Clone Repository**
   ```bash
   git clone https://github.com/unico-rey/presensi-polda-kalsel.git
   cd presensi-polda-kalsel
   ```

2. **Jalankan Aplikasi (Windows)**
   Cukup klik ganda atau jalankan file batch yang telah disediakan:
   ```bash
   run.bat
   ```
   *Script ini secara otomatis akan:*
   - Mengaktifkan/membuat Virtual Environment.
   - Melakukan pengecekan dan migrasi Database.
   - Membuka browser ke halaman aplikasi.
   - Menjalankan server Uvicorn.

   *Alternatif Manual (jika tanpa `run.bat`):*
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python check_db.py
   python migrate_db.py
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```

3. **Akses Aplikasi**
   - Halaman Presensi: `http://127.0.0.1:8000/absensi/`
   - Halaman Admin Dashboard: `http://127.0.0.1:8000/admin/`

## 🔐 Akun Default Admin
Untuk login ke halaman admin, gunakan kredensial berikut:
- **Username:** `admin`
- **Password:** `1234`

## 📸 Tampilan Layar (Screenshots)

<div align="center">
  <table style="width:100%">
    <tr>
      <td align="center"><strong>Halaman Presensi (Geofencing)</strong></td>
      <td align="center"><strong>Admin Dashboard</strong></td>
    </tr>
    <tr>
      <td align="center">
        <!-- Placeholder untuk Screenshot Absensi -->
        <img src="https://via.placeholder.com/400x250/f0f2f5/005571?text=Halaman+Absensi" alt="Halaman Absensi">
      </td>
      <td align="center">
        <!-- Placeholder untuk Screenshot Admin -->
        <img src="https://via.placeholder.com/400x250/f0f2f5/005571?text=Dashboard+Admin" alt="Dashboard Admin">
      </td>
    </tr>
  </table>
</div>

---
<div align="center">
  <i>Dibuat untuk mempermudah sistem manajemen absensi Polda Kalsel.</i>
</div>
