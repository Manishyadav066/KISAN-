@echo off
echo Installing Python requirements for Kisan Project
echo ==============================================
echo Make sure you have activated your virtual environment
echo If not, create and activate one with:
echo   python -m venv venv
echo   venv\Scripts\activate
echo ==============================================
timeout /t 3 /nobreak >nul

echo Installing requirements...
pip install -r requirements.txt

if %errorlevel% == 0 (
    echo.
    echo Requirements installed successfully!
) else (
    echo.
    echo Error installing requirements. Please check the error message above.
)

pause