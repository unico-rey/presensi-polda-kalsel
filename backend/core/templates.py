import os
from fastapi.templating import Jinja2Templates

# Path absolut agar bekerja di Vercel, cPanel, maupun lokal
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(_BASE_DIR, "frontend", "templates"))