# 🚔 Tutorial & Panduan Lengkap Sistem Presensi Polda Kalsel

Selamat datang di panduan lengkap pengembangan, instalasi, dan penggunaan **Sistem Presensi Polda Kalsel**. Dokumen ini dirancang untuk membantu administrator, pengembang, dan pengguna akhir dalam memahami cara kerja serta cara mengoperasikan sistem presensi cerdas ini.

---

## 📂 1. Struktur Folder Proyek

Untuk memudahkan navigasi, berikut adalah struktur folder utama dari aplikasi ini:

*   **`backend/`** — Berisi logika utama aplikasi Python/FastAPI:
    *   [database.py](file:///c:/project/kuliah/presensi%20polda%20kalsel/backend/db/database.py) — Pengaturan koneksi SQLAlchemy ORM ke database MySQL.
    *   [main.py](file:///c:/project/kuliah/presensi%20polda%20kalsel/backend/main.py) — Titik masuk utama aplikasi (Entrypoint FastAPI).
    *   **`models/`** — Definisi skema database ORM.
    *   **`routes/`** — Endpoint routing (API) yang terbagi menjadi [absensi.py](file:///c:/project/kuliah/presensi%20polda%20kalsel/backend/routes/absensi.py), [admin.py](file:///c:/project/kuliah/presensi%20polda%20kalsel/backend/routes/admin.py), [anggota.py](file:///c:/project/kuliah/presensi%20polda%20kalsel/backend/routes/anggota.py), dan [auth.py](file:///c:/project/kuliah/presensi%20polda%20kalsel/backend/routes/auth.py).
    *   **`services/`** — Logika bisnis tambahan seperti background scheduler dan notifikasi push.
*   **`frontend/`** — Antarmuka pengguna (UI):
    *   **`templates/`** — File HTML (Jinja2) untuk rendering halaman, seperti [absensi.html](file:///c:/project/kuliah/presensi%20polda%20kalsel/frontend/templates/absensi.html) dan [admin_dashboard.html](file:///c:/project/kuliah/presensi%20polda%20kalsel/frontend/templates/admin_dashboard.html).
    *   **`static/`** — Aset statis (CSS, Javascript, Service Worker `sw.js`, PWA Manifest).
*   **Root Folder (Skrip Utilitas)**:
    *   [run.bat](file:///c:/project/kuliah/presensi%20polda%20kalsel/run.bat) — Skrip otomatis untuk setup virtual environment dan menjalankan server.
    *   [check_db.py](file:///c:/project/kuliah/presensi%20polda%20kalsel/check_db.py) — Inisialisasi tabel database berdasarkan skema.
    *   [migrate_db.py](file:///c:/project/kuliah/presensi%20polda%20kalsel/migrate_db.py) — Skrip untuk migrasi kolom database baru (seperti tanda tangan, foto, latitude, dan longitude).
    *   [seed_master.py](file:///c:/project/kuliah/presensi%20polda%20kalsel/seed_master.py) — Inisialisasi data pangkat, jabatan, dan akun admin default.

---

## ⚙️ 2. Langkah Persiapan & Instalasi

### Prasyarat System
*   **Python 3.9+** terinstal dan terdaftar di PATH.
*   **MySQL Server** (bisa menggunakan XAMPP, Laragon, atau instalasi MySQL Server mandiri).

---

### Langkah 2.1: Menyiapkan Database MySQL
1. Buka aplikasi MySQL manager Anda (misalnya phpMyAdmin, DBeaver, atau MySQL CLI).
2. Buat database baru bernama **`presensi_polda`**:
   ```sql
   CREATE DATABASE presensi_polda;
   ```

---

### Langkah 2.2: Konfigurasi Environment File (`.env`)
Salin file `.env.example` menjadi `.env` di direktori utama proyek Anda, lalu sesuaikan isinya dengan kredensial database Anda:

```ini
DATABASE_URL=mysql+mysqlconnector://root:password_mysql_anda@localhost/presensi_polda
SECRET_KEY=ganti_dengan_key_rahasia_anda_yang_aman
```
> **Catatan:** Jika Anda menggunakan XAMPP secara default tanpa password root, gunakan format:
> `DATABASE_URL=mysql+mysqlconnector://root:@localhost/presensi_polda`

---

### Langkah 2.3: Cara Menjalankan Aplikasi

#### Pilihan A: Cara Otomatis (Rekomendasi - Windows)
Cukup jalankan berkas **`run.bat`** di direktori utama.
Skrip ini akan secara otomatis:
1. Membuat virtual environment (`venv`) jika belum ada.
2. Menginstal seluruh pustaka yang dibutuhkan dari `requirements.txt`.
3. Memverifikasi koneksi database serta menerapkan migrasi tabel yang diperlukan.
4. Mengisi data master bawaan (Pangkat, Jabatan, dan Admin Default).
5. Membuka peramban (browser) Anda ke alamat `http://127.0.0.1:8000/absensi/`.
6. Menjalankan server lokal.

#### Pilihan B: Cara Manual (Menggunakan Command Line / Terminal)
Jika ingin menjalankan perintah satu per satu secara manual:

```bash
# 1. Buat dan aktifkan Virtual Environment Python
python -m venv venv
venv\Scripts\activate

# 2. Instal pustaka dependensi
pip install -r requirements.txt

# 3. Jalankan inisialisasi skema database
python check_db.py

# 4. Jalankan migrasi kolom database
python migrate_db.py

# 5. Jalankan seed data master (Pangkat, Jabatan, & Akun Admin Default)
python seed_master.py

# 6. Jalankan Server Uvicorn
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Aplikasi kini dapat diakses melalui browser Anda di **`http://127.0.0.1:8000`**.

---

## 🔒 3. Akses Akun & Kredensial Default

Setelah berhasil dijalankan pertama kali, sistem memiliki akun administrator bawaan untuk masuk ke panel admin:
*   **Halaman Login Admin:** `http://127.0.0.1:8000/admin/`
*   **Username:** `admin`
*   **Password:** `1234`

*Sangat disarankan untuk segera memperbarui password atau menambahkan akun administrator baru melalui panel admin demi alasan keamanan.*

---

## 💡 4. Panduan Penggunaan Fitur

### 📌 4.1. Halaman Presensi Anggota (`http://127.0.0.1:8000/absensi/`)
Halaman ini digunakan oleh anggota Polri untuk melakukan pencatatan kehadiran secara mandiri.

1. **Pilih Nama Anggota:** Anggota memilih nama mereka dari daftar drop-down.
2. **Pilih Tipe Kehadiran:**
   *   **Hadir** (Masuk Kerja)
   *   **Pulang / Pulang Siang** (Selesai Kerja)
   *   **Sakit / Izin / Cuti** (Memerlukan input keterangan tertulis tambahan)
3. **Penyediaan Secure Context (Kamera & GPS):**
   *   Sistem akan meminta izin akses **Lokasi (GPS)** untuk keperluan *Geofencing*.
   *   Sistem akan meminta izin akses **Kamera** untuk berfoto secara langsung saat melakukan absensi.
4. **Tanda Tangan Digital:** Anggota wajib membubuhkan tanda tangan digital pada kanvas interaktif yang disediakan di layar sebelum menekan tombol submit.
5. **Kirim Data (Submit):** Klik tombol "Kirim Presensi". Jika lokasi Anda berada di dalam radius kantor, presensi berhasil disimpan dan detail struk bukti absensi akan ditampilkan.

---

### 📊 4.2. Panel Kontrol & Dashboard Admin (`http://127.0.0.1:8000/admin/`)
Halaman khusus bagi petugas piket / administrator untuk memantau presensi anggota secara real-time.

*   **Live Dashboard:** 
    Menampilkan statistik kehadiran hari ini (Jumlah Hadir, Sakit, Izin, Cuti, Terlambat, dan Belum Absen). Dashboard ini memiliki fitur **Auto-Refresh** setiap 30 detik untuk memberikan informasi terbaru secara otomatis.
*   **Peta Pemantauan Absensi (Map View):**
    Visualisasi posisi geografis terakhir saat anggota melakukan presensi menggunakan Leaflet.js.
*   **Daftar Kehadiran (Event Stream):**
    Menampilkan alur log kronologis aktivitas presensi yang lengkap dengan filter tanggal, cetak/download data, serta tombol edit/hapus rekaman jika diperlukan.
*   **Manajemen Anggota (CRUD & Import/Export):**
    *   Administrator dapat menambah, mengedit, atau menghapus profil anggota.
    *   Tersedia fitur **Import Anggota dari Excel/CSV** untuk mempercepat inisialisasi data dalam jumlah besar dengan menggunakan file template yang telah disediakan.
*   **Manajemen Jabatan & Pangkat:**
    Mengontrol daftar jabatan dan pangkat kepolisian yang tersedia di sistem presensi.

---

## 📍 5. Penjelasan Teknis: Geofencing & Push Notification

### 📏 5.1. Mekanisme Smart Geofencing
Validasi lokasi presensi dilakukan di sisi klien (frontend) dan divalidasi kembali di sisi server (backend) menggunakan rumus matematika **Haversine Formula**:

$$d = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)$$

Dimana:
*   $\phi_1, \phi_2$ adalah latitude lokasi kantor dan koordinat GPS anggota.
*   $\Delta\phi, \Delta\lambda$ adalah perbedaan latitude dan longitude.
*   $R$ adalah jari-jari bumi (6.371.000 meter).
*   $d$ adalah jarak dalam meter.

Jika $d$ melebihi radius batas (misalnya 200 meter) yang dikonfigurasi di menu **Pengaturan Admin**, absensi akan otomatis ditolak oleh server demi mencegah kecurangan (misalnya fake GPS / manipulasi frontend).

### 🔔 5.2. Push Notifications
Aplikasi mendukung pengiriman notifikasi instan langsung ke perangkat anggota/admin setelah presensi berhasil:
*   Menggunakan protokol standar **WebPush (VAPID)**.
*   Beroperasi di latar belakang menggunakan berkas Service Worker [sw.js](file:///c:/project/kuliah/presensi%20polda%20kalsel/frontend/static/sw.js) dan file manifes [manifest.json](file:///c:/project/kuliah/presensi%20polda%20kalsel/frontend/static/manifest.json).
*   Scheduler backend secara periodik memeriksa status absensi harian dan mengirim notifikasi status secara langsung.

---

## 🛠️ 6. Troubleshooting & Pertanyaan Umum (FAQ)

### ❓ A. Mengapa browser tidak mengizinkan akses Kamera & GPS saat mengakses website?
*   **Penyebab:** Peramban modern (Chrome, Edge, Safari) membatasi akses API hardware (kamera & lokasi) hanya pada koneksi aman (**Secure Context**) yaitu `localhost` / `127.0.0.1` atau protokol **HTTPS**.
*   **Solusi:**
    *   Jika menjalankan secara lokal, pastikan Anda mengakses melalui `http://localhost:8000` atau `http://127.0.0.1:8000`.
    *   Jika diakses dari luar jaringan lokal (misalnya di-hosting atau diakses dari HP dalam satu Wi-Fi), Anda harus mengonfigurasi sertifikat SSL (HTTPS) atau menggunakan tunnel secure seperti **Cloudflare Tunnel (cloudflared)** / Ngrok.

### ❓ B. Bagaimana cara mengubah radius lokasi Geofencing kantor?
1. Masuk ke **Panel Admin** (`http://127.0.0.1:8000/admin/`).
2. Pilih menu **Pengaturan** di sidebar sebelah kiri.
3. Ubah nilai **Latitude Kantor**, **Longitude Kantor**, dan **Radius Batas (dalam meter)** sesuai dengan letak titik koordinat Polda/Polres Anda.
4. Klik **Simpan Pengaturan**.

### ❓ C. Bagaimana jika muncul error database "mysqlconnector.errors.ProgrammingError"?
*   **Penyebab:** Database MySQL belum diaktifkan di XAMPP / Laragon, atau nama database belum dibuat, atau kredensial `.env` salah.
*   **Solusi:**
    1. Pastikan modul MySQL di XAMPP/Laragon dalam kondisi **Running**.
    2. Jalankan perintah `mysql -u root` lalu ketik `CREATE DATABASE presensi_polda;` jika database belum dibuat.
    3. Periksa file `.env` Anda dan pastikan username, password, dan port MySQL sesuai.

---

*Dikembangkan dengan dedikasi untuk kemudahan operasional Polda Kalsel. Jika Anda memiliki pertanyaan teknis lebih lanjut, hubungi Administrator Sistem.*
