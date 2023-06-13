rem "/d" gets the current letter of the drive the batch file is located in
rem "%~d0" holds the actual drive letter
cd /d %~d0

set "get_prop=AutoOffer\html_manipulation\Property_Data_Sender.py"
set "check_ghl=AutoOffer\html_manipulation\Asyc_GHL_Checker.py"
set "make_offer=AutoOffer\Offer_Generator\Offer_Maker.py"
set "make_email=AutoOffer\Email_Generator\Open_AI.py"
set "send_email=AutoOffer\email_sender\Email_Sender.py"
set "switch_ghl=AutoOffer\html_manipulation\GHL_Switcher.py"

@REM start cmd /k "C:\Users\charl\Desktop\AutoOffer\Scripts\activate.bat && python %get_prop%"
@REM start cmd /k "C:\Users\charl\Desktop\AutoOffer\Scripts\activate.bat && python %check_ghl%"
@REM start cmd /k "C:\Users\charl\Desktop\AutoOffer\Scripts\activate.bat && python %make_offer%"
@REM start cmd /k "C:\Users\charl\Desktop\AutoOffer\Scripts\activate.bat && python %make_email%"
@REM start cmd /k "C:\Users\charl\Desktop\AutoOffer\Scripts\activate.bat && python %send_email%"
@REM start cmd /k "C:\Users\charl\Desktop\AutoOffer\Scripts\activate.bat && python %switch_ghl%"



start cmd /k "C:\Script\PYAO-main\venv\Scripts\activate.bat && python %get_prop%"
rem timeout /t 7 >nul
rem start cmd /k "C:\Script\PYAO-main\venv\Scripts\activate.bat && python %check_ghl%"
rem timeout /t 7 >nul
rem  cmd /k "C:\Script\PYAO-main\venv\Scripts\activate.bat && python %make_offer%"
rem timeout /t 7 >nul
rem start cmd /k "C:\Script\PYAO-main\venv\Scripts\activate.bat && python %make_email%"
rem timeout /t 7 >nul
rem start cmd /k "C:\Script\PYAO-main\venv\Scripts\activate.bat && python %send_email%"
rem timeout /t 7 >nul
rem start cmd /k "C:\Script\PYAO-main\venv\Scripts\activate.bat && python %switch_ghl%"