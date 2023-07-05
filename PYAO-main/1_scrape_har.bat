rem "/d" gets the current letter of the drive the batch file is located in
rem "%~d0" holds the actual drive letter
cd /d %~d0

set "scrape_har=AutoOffer\html_manipulation\Property_Data_Sender.py"

start cmd /k "C:\Script\PYAO-main\venv\Scripts\activate.bat && python %scrape_har%"
