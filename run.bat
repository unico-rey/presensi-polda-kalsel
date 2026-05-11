@echo off
setlocal
set PYTHONUTF8=1

echo ==========================================
echo Starting Sistem Absensi Polda Kalsel...
echo ==========================================

:: 1. Check for Virtual Environment
if not exist venv\Scripts\activate.bat goto NO_VENV

:: 2. Activate Virtual Environment
echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat

:: 3. Run Database Initialization and Migration
echo [2/4] Verifying and migrating database...
python check_db.py
if errorlevel 1 goto DB_ERROR

python migrate_db.py
if errorlevel 1 goto MIGRATE_ERROR

:: 4. Open Browser
echo [3/4] Opening browser...
start http://127.0.0.1:8000/absensi/

:: 5. Run Application
echo [4/4] Starting server...
echo Access application at http://127.0.0.1:8000
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
goto END

:NO_VENV
echo [ERROR] Virtual environment (venv) not found.
pause
exit /b 1

:DB_ERROR
echo [ERROR] Database check failed.
pause
exit /b 1

:MIGRATE_ERROR
echo [ERROR] Database migration failed.
pause
exit /b 1

:END
pause
