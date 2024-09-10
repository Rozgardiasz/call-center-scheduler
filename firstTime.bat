@echo off
:: Step 1: Run npm install
echo Running npm install...
call npm install

:: Step 2: Check if PostgreSQL server is running
echo Checking if PostgreSQL is running...
for /f "tokens=*" %%A in ('netstat -aon ^| find "5432"') do (
    echo PostgreSQL server is running
    goto create_venv
)
echo PostgreSQL server is not running, please start PostgreSQL.
exit /b 1

:create_venv
:: Step 3: Create a Python virtual environment
echo Creating Python virtual environment...
python -m venv backend\venv

:: Step 4: Activate the virtual environment
echo Activating virtual environment...
call backend\venv\Scripts\activate

:: Step 5: Install Python requirements
echo Installing Python requirements from requirements.txt...
pip install -r backend/requirements.txt

echo Setup completed successfully.
