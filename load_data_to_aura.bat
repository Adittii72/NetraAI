@echo off
echo ========================================
echo NetraAI - Loading Data to Neo4j Aura
echo ========================================
echo.
echo Instance: netraai-db
echo URI: neo4j+s://ce4768b6.databases.neo4j.io
echo.
echo This will load:
echo - 500 Companies
echo - 200 Directors
echo - 150 Tenders
echo - 2,503 Relationships
echo.
echo Please wait...
echo.

cd backend
python neo4j_connector.py

echo.
echo ========================================
echo Data Loading Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start backend: start_backend.bat
echo 2. Start frontend: start_frontend.bat
echo 3. Open browser: http://localhost:3000
echo.
pause
