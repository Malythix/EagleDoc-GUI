@echo off
call .venv\Scripts\activate.bat
python -m uvicorn main:app
