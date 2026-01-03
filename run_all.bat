@echo off
echo ===================================================
echo   QRS: Quantum Refractometer Simulation
echo   The Effective Field Theory of 5D Optics
echo   (c) 2026 Antigravity Research
echo ===================================================
echo.
echo [1/5] Checking Environment...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.9+.
    pause
    exit /b
)
echo.

echo [2/5] Running Simulations (Phase 1: Geometry)...
python modules/generate_prism_image.py
python modules/generate_fiber_image.py
echo.

echo [3/5] Running Simulations (Phase 2: Cosmology & CGI)...
python modules/galactic_curve.py
python modules/raytracer_5d.py
echo.

echo [4/6] Running Simulations (Phase 3: Metamaterials - Slow)...
python modules/field_explorer.py
python modules/5d_wave_simulation.py
echo.

echo [5/6] Running Experiments (Phase 4: Validation)...
python modules/experiments/conoscopy_simulation.py
python modules/experiments/grid_locking.py
python modules/experiments/kagra_validation.py
python modules/experiments/kagra_noise_simulation.py
echo.

echo [6/6] Generating Scientific Atlas (Final Report)...
python generate_report.py
if %errorlevel% neq 0 (
    echo [ERROR] Report generation failed.
    pause
    exit /b
)

echo.
echo ===================================================
echo [SUCCESS] QRS_Final_Report.html generated!
echo It is ready to be opened in your browser.
echo ===================================================
pause
