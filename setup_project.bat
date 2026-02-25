@echo off
echo ========================================
echo NetraAI Project Setup
echo ========================================
echo.

echo [1/4] Installing Python dependencies...
pip install -r requirements.txt
echo.

echo [2/4] Generating synthetic dataset...
python dataset_generator.py
echo.

echo [3/4] Verifying dataset...
python verify_dataset.py
echo.

echo [4/4] Installing frontend dependencies...
cd frontend
call npm install
cd ..
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the platform:
echo   1. Run start_backend.bat (Terminal 1)
echo   2. Run start_frontend.bat (Terminal 2)
echo   3. Open http://localhost:3000
echo.

pause
