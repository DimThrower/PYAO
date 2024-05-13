@echo off

rem Activate the venv 
call D:\PYAO-main\venv\Scripts\activate

rem Navigate to the site-package directory
cd D:\PYAO-main\venv\Lib\site-packages

rem Create the .pth file
echo D:\PYAO-main\ > mypath.pth

rem Deactivate venv
Deactivate

echo Python path updated successfully

pause