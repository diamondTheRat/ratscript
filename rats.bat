@echo off
REM Check if there is an argument passed
if "%~1"=="" (
    echo No input file provided.
    exit /b 1
)

REM Call Python script with the input file
python ./run_file.py %1