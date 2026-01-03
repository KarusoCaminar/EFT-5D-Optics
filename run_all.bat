@echo off
echo ===================================================
echo   QRS: Quantum Refractometer Simulation
echo   The Effective Field Theory of 5D Optics
echo   (c) 2026 Antigravity Research
echo ===================================================
echo.
echo [1/2] Checking Environment...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.9+.
    pause
    exit /b
)
echo.

echo [2/2] Launching Dashboard (Batch Mode)...
python dashboard.py --batch

if %errorlevel% neq 0 (
    echo [ERROR] Dashboard execution failed.
    pause
    exit /b
)

echo.
echo ===================================================
echo [SUCCESS] Run complete.
echo ===================================================
pause
