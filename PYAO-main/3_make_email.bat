rem "/d" gets the current letter of the drive the batch file is located in
rem "%~d0" holds the actual drive letter
cd /d %~d0

set "make_email=AutoOffer\Email_Generator\Open_AI.py"

start cmd /k "C:\Script\PYAO-main\venv\Scripts\activate.bat && python %make_email%"
