@echo off
echo Starting Kisan Project Server...
echo ========================================
echo Make sure you have activated your virtual environment
echo If not, run: venv\Scripts\activate
echo ========================================
timeout /t 2 /nobreak >nul
python manage.py runserver
pause