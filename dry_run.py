import sys
import os

# Mimic main.py path injection
current_dir = r"c:\project\kuliah\Scantools-Polda\agent"
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    print(f"Parent dir: {parent_dir}")
    print(f"Path contains app: {os.path.exists(os.path.join(parent_dir, 'app'))}")
    from backend.routes import auth, admin, pegawai, scan
    print("✅ Success: All modules imported correctly")
    print(f"auth router: {getattr(auth, 'router', 'Missing')}")
    print(f"admin router: {getattr(admin, 'router', 'Missing')}")
    print(f"pegawai router: {getattr(pegawai, 'router', 'Missing')}")
    print(f"scan router: {getattr(scan, 'router', 'Missing')}")
except Exception as e:
    print(f"❌ Error during import: {e}")
    import traceback
    traceback.print_exc()
