@echo off
echo ========================================
echo NetraAI Backend Server
echo ========================================
echo.

cd backend
echo Starting FastAPI server on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
python api.py

pause
