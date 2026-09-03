@echo off
echo Starting installation of required packages.
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
echo.
echo Setup complete. Run start.bat to launch the app.
pause