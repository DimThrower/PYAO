rem "/d" gets the current letter of the drive the batch file is located in
rem "%~d0" holds the actual drive letter
cd /d %~d0

set "check_ghl=AutoOffer\html_manipulation\Asyc_GHL_Checker.py"

start cmd /k "C:\Script\PYAO-main\venv\Scripts\activate.bat && python %check_ghl%"
