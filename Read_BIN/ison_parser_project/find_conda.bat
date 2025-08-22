@echo off
setlocal
set "CONDA_PATH="

REM Try to find conda via where
for /f "delims=" %%C in ('where conda 2^>nul') do (
    set "CONDA_PATH=%%C"
    goto :found_conda
)

REM Try conda.bat explicitly
for /f "delims=" %%C in ('where conda.bat 2^>nul') do (
    set "CONDA_PATH=%%C"
    goto :found_conda
)

REM Fallback: common install locations
if exist "%USERPROFILE%\miniconda3\condabin\conda.bat" (
    set "CONDA_PATH=%USERPROFILE%\miniconda3\condabin\conda.bat"
    goto :found_conda
)
if exist "%USERPROFILE%\miniconda3\Scripts\conda.exe" (
    set "CONDA_PATH=%USERPROFILE%\miniconda3\Scripts\conda.exe"
    goto :found_conda
)
if exist "C:\ProgramData\Miniconda3\condabin\conda.bat" (
    set "CONDA_PATH=C:\ProgramData\Miniconda3\condabin\conda.bat"
    goto :found_conda
)

echo Miniconda/Anaconda not found!
echo.
echo Run the following in the SAME cmd window and paste the output here:
echo    where conda
echo    echo %%PATH%%
echo.
pause
exit /b

:found_conda
REM Derive root folder from found path
for %%I in ("%CONDA_PATH%") do set "MINICONDA_ROOT=%%~dpI"
if "%MINICONDA_ROOT:~-1%"=="\" set "MINICONDA_ROOT=%MINICONDA_ROOT:~0,-1%"

set "SCRIPTS_PATH=%MINICONDA_ROOT%\Scripts"

echo Found: %CONDA_PATH%
echo Miniconda root: %MINICONDA_ROOT%
echo Scripts folder: %SCRIPTS_PATH%
echo.
REM Example activation (uncomment to use)
REM call "%SCRIPTS_PATH%\activate.bat" ison_parser

pause
endlocal