@echo off
echo ========================================
echo NetraAI Neo4j Setup
echo ========================================
echo.

echo This script will help you set up Neo4j for NetraAI
echo.

echo Step 1: Install Neo4j Python Driver
pip install neo4j --quiet
echo.

echo Step 2: Check if Neo4j is running
echo.
echo Please ensure Neo4j is running before continuing.
echo.
echo Options to run Neo4j:
echo   1. Neo4j Desktop - Download from https://neo4j.com/download/
echo   2. Docker - Run: docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j
echo   3. Neo4j Aura - Free cloud instance at https://neo4j.com/cloud/aura/
echo.

pause

echo.
echo Step 3: Loading data into Neo4j
echo.
cd backend
python neo4j_connector.py
cd ..
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the Neo4j-powered API:
echo   cd backend
echo   python api_neo4j.py
echo.
echo To view data in Neo4j Browser:
echo   Open http://localhost:7474
echo.

pause
