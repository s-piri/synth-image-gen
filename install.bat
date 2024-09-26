@echo off
SET VENV_DIR=venv

REM Check if the virtual environment directory exists
IF NOT EXIST %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
) ELSE (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
CALL %VENV_DIR%\Scripts\activate

REM Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt

echo Installation complete.
