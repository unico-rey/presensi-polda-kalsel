import os
import sys

# Memasukkan path aplikasi agar Python dapat menemukan modul backend
sys.path.insert(0, os.path.dirname(__file__))

# Mengimpor aplikasi FastAPI dari backend.main
from backend.main import app

# Mengonversi ASGI FastAPI ke WSGI menggunakan a2wsgi agar kompatibel dengan cPanel Passenger
from a2wsgi import ASGIMiddleware

application = ASGIMiddleware(app)
