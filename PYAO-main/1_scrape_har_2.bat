rem "/d" gets the current letter of the drive the batch file is located in
rem "%~d0" holds the actual drive letter
cd /d %~d0

set "scrape_har=AutoOffer\html_manipulation\Property_Data_Sender_2.py"

start cmd /k "%~d0:\Script\PYAO-main\venv\Scripts\activate.bat && python %scrape_har%"
