@echo off
call venv\Scripts\activate.bat
set FLASK_APP=app.py
set FLASK_DEBUG=1
flask run
