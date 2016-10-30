@echo off
REM This script downloads tfl core data as a csv

echo Downloading bus route information from tfl... (It may take up to 5 minutes)
SET download_script=../python/downloader/tfl_download.py
SET save_csv_location=../data/tfl/route_info.csv

python %download_script% csv %save_csv_location%
IF ERRORLEVEL 0 (
    echo Saved route information csv file to: %save_csv_location%
) ELSE (
    EXIT /B
)

echo.
timeout /t 2 /nobreak > NUL



