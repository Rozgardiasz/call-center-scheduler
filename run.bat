@echo off
REM Open the first terminal and run the npm command in PowerShell
start powershell -NoExit -Command "npm run serve"

REM Open the second terminal, activate the virtual environment, and run Uvicorn server in PowerShell
start powershell -NoExit -Command "cd backend/venv/Scripts; .\activate; cd ../..; python.exe -m uvicorn main:app --reload"
