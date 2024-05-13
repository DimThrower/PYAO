@echo off
rem Get the current letter of the drive the batch file is located in
cd /d %~d0
echo Current Drive: %~d0

rem Set Python path
set PYTHONPATH=%PYTHONPATH%;D:\PYAO-main\PYAO-main

rem Define the Python script path
set "make_offer=%~d0\PYAO-main\PYAO-main\AutoOffer\Offer_Generator\Offer_Maker.py"

rem Activate the virtual environment
call %~d0\PYAO-main\venv\Scripts\activate.bat

rem Run the Python script
python "%make_offer%"

pause
