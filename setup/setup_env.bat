@echo off
REM This script set up the necessary System Environmental Variables for the project

echo Checking if environmental variables are up to date for the project...
echo.
python %~dp0python\common\path_manager.py --test > NUL 2>&1
IF %ERRORLEVEL% EQU -1 (
    SETX /M LiveLondonBusMapPath %~dp0 > NUL
    SETX /M PYTHONPATH %PYTHONPATH%;%~dp0python > NUL

    echo Added environmental variables for all users:
    echo   LiveLondonBusMapPath: %~dp0
    echo   PYTHONPATH: %PYTHONPATH%
) ELSE (
    echo No changes needed. Project already properly configured.
    echo.
)

timeout /t 2 /nobreak > NUL