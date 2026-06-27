import os
from fastapi.templating import Jinja2Templates

# Path absolut agar bekerja di Vercel, cPanel, maupun lokal
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_TEMPLATE_DIR = os.path.join(_BASE_DIR, "frontend", "templates")

# Fallback ke path lain jika folder tidak ditemukan di Vercel
if not os.path.exists(_TEMPLATE_DIR):
    _TEMPLATE_DIR = os.path.join(os.getcwd(), "frontend", "templates")
    
# Coba buat foldernya jika tetap tidak ada agar Jinja2 tidak crash saat startup
if not os.path.exists(_TEMPLATE_DIR):
    try:
        os.makedirs(_TEMPLATE_DIR, exist_ok=True)
    except:
        pass

templates = Jinja2Templates(directory=_TEMPLATE_DIR)