@echo off
cd /d %~dp0
start chrome http://localhost:8000/index.html
python cgiserver.py