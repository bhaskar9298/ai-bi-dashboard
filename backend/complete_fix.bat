@echo off
echo ============================================================
echo COMPLETE FIX PROCEDURE
echo ============================================================
echo.

echo Step 1: Stopping any running Python processes...
taskkill /F /IM python.exe 2>nul
if %errorlevel% == 0 (
    echo    - Killed existing Python processes
    timeout /t 2 /nobreak >nul
) else (
    echo    - No Python processes running
)
echo.

echo Step 2: Cleaning Python cache files...
python force_clean_restart.py
echo.

echo Step 3: Running diagnostic check...
python diagnostic_check.py
echo.

echo Step 4: Ready to start server
echo.
echo ============================================================
echo NEXT STEP: Start the server
echo ============================================================
echo Run: python app.py
echo.
echo Or if you want to start automatically:
choice /C YN /M "Start the server now"
if %errorlevel% == 1 (
    echo Starting server...
    python app.py
)
