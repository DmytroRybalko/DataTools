@echo off
REM Create virtual environment (named venv)
python -m venv logger

REM Activate the virtual environment
call logger\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt

REM Install Playwright browsers
python -m playwright install

echo Build complete. Find your EXE in the dist folder.
pause