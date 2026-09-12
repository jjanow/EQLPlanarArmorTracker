@echo off
rem Launcher for Windows. Finds a working Python interpreter and runs the
rem tracker, forwarding any arguments (e.g. run.bat -o report.txt).
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 eq_planar_armor.py %*
    goto :end
)

where python >nul 2>nul
if %errorlevel%==0 (
    python eq_planar_armor.py %*
    goto :end
)

echo error: no Python found on PATH. Install Python 3.9+ from https://python.org and try again.
exit /b 1

:end
pause
