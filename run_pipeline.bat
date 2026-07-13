@echo off
echo ===================================================
echo RUNNING AUTONOMOUS DATA HARVESTING PIPELINES
echo ===================================================

cd /d "C:\Users\Ember\Documents\automated-scraper-pipeline"

:: Activate the single virtual environment shared by both files
call venv\Scripts\activate

echo [1/2] Launching Flat-File CSV Pipeline...
python scraper.py

echo [2/2] Launching Relational SQL Database Pipeline...
python scraper_to_sql.py

echo ===================================================
echo ALL DATA PIPELINES COMPLETED SUCCESSFULLY
echo ===================================================
pause
