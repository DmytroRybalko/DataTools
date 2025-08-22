@echo off
REM === Change to the folder where this BAT file is located ===
cd /d %~dp0

REM === Step 1: Create venv if not exists ===
if not exist env (
    echo Creating virtual environment in .\env ...
    python -m venv env
)

REM === Step 2: Activate venv ===
call env\Scripts\activate.bat

REM === Step 3: Upgrade pip ===
echo Upgrading pip...
python -m pip install --upgrade pip

REM === Step 4: Install requirements ===
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo No requirements.txt found, installing core packages...
    pip install tkinter selenium playwright
)

REM === Step 5: Fix Tcl/Tk paths ===
for /f "delims=" %%i in ('python -c "import sys; print(sys.base_prefix)"') do set PYBASE=%%i
set TCL_LIBRARY=%PYBASE%\tcl\tcl8.6
set TK_LIBRARY=%PYBASE%\tcl\tk8.6

pause
echo.