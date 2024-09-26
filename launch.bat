@echo off
SET VENV_DIR=venv

REM Check if the virtual environment directory exists
IF NOT EXIST %VENV_DIR% (
    echo Virtual environment does not exist. Please run install.bat first.
    exit /b
)

REM Activate the virtual environment
CALL %VENV_DIR%\Scripts\activate

REM Run the main Python script
python main.py  REM Replace 'main.py' with the name of your main script

echo Press any key to exit...
pause > nul
