@echo off
title Spotify Sleep Timer

:input
cls
echo ================================
echo        Spotify Sleep Timer       
echo ================================
echo.
set /p mins=Enter minutes to wait before pausing Spotify: 

:: Validate input
for /f "delims=0123456789" %%a in ("%mins%") do (
    echo Invalid input. Please enter a number.
    pause
    goto input
)

set /a seconds=%mins% * 60
cls
echo ================================
echo   Timer started for %mins% minute(s)
echo ================================
echo.

:countdown
set /a minsLeft=%seconds% / 60
set /a secsLeft=%seconds% %% 60
cls
echo ================================
echo   Spotify Sleep Timer
echo -------------------------------
echo   Time Left: %minsLeft% min %secsLeft% sec
echo ================================
timeout /t 1 >nul
set /a seconds=%seconds% - 1
if %seconds% GEQ 0 goto countdown

:: Pause Spotify using NirCmd
echo Time's up! Pausing Spotify...
powershell -command "(New-Object -ComObject WScript.Shell).SendKeys([char]179)" >nul

echo Done. Spotify paused.
timeout /t 3 >nul
exit
