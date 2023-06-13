@echo off

rem Activate the venv 
call C:\Script\PYAO-main\venv\Scripts\activate

rem Navigate to the site-package directory
cd C:\Script\PYAO-main\venv\Lib\site-packages

rem Create the .pth file
echo C:\Script\PYAO-main\ > mypath.pth

rem Deactivate venv
Deactivate

echo Python path updated successfully