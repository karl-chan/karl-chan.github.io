@echo off
REM This script uploads csv containing tfl core data to server database

echo Uploading csv to database...
SET upload_script=../python/uploader/csv_upload_to_db.py
SET csv_location=../data/tfl/route_info.csv

python %upload_script% %csv_location%
IF ERRORLEVEL 0 (
    echo Uploaded csv file: %csv_location% to database
) ELSE (
    EXIT /B
)

echo.
timeout /t 2 /nobreak > NUL



