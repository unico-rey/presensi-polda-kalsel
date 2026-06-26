import os
import sys
import traceback

# ============================================================
# PENTING: Set BASE_DIR agar semua path relatif bisa ditemukan
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Set working directory ke folder project
os.chdir(BASE_DIR)

# Load .env dari folder yang benar
from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, ".env"))

try:
    from backend.main import app
    from a2wsgi import ASGIMiddleware

    application = ASGIMiddleware(app)

except Exception as e:
    # Tampilkan error detail jika app gagal startup
    error_detail = traceback.format_exc()

    def application(environ, start_response):
        status = "500 Internal Server Error"
        response_headers = [("Content-Type", "text/plain; charset=utf-8")]
        start_response(status, response_headers)
        error_msg = f"=== APPLICATION STARTUP ERROR ===\n\n{error_detail}"
        return [error_msg.encode("utf-8")]
