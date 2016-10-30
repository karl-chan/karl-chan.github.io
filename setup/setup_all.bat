@echo off
REM This script sets up the tfl core data required for the server

REM Step 1 Set up environmental variables if not yet
CALL setup_env.bat

REM Step 2 Download core data from tfl
CALL setup_download_tfl_data.bat

REM Step 3 Upload core data to database
CALL setup_upload_csv.bat