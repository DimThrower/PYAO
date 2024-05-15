@echo off
rem Get the current letter of the drive the batch file is located in
cd /d %~d0
echo Current Drive: %~d0

rem Set Python path
set PYTHONPATH=%PYTHONPATH%;D:\PYAO-main\PYAO-main

rem Define the Python script path
set "scrape_har=%~d0\PYAO-main\PYAO-main\AutoOffer\html_manipulation\Property_Data_Sender.py"

rem Activate the virtual environment
call %~d0\PYAO-main\venv\Scripts\activate.bat

rem Run the Python script
python "%scrape_har%"

pause