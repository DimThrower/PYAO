
rem path to mysql server bin folder
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"

rem credentials to connect to mysql server
set mysql_user=root
set mysql_password=input

rem backup file name generation
set backup_path=C:\Script
set backup_name=auto_offer_backup.sql

rem backup creation
mysqldump --user=%mysql_user% --password=%mysql_password% -p auto_offer --result-file="%backup_path%\%backup_name%"
if %ERRORLEVEL% NEQ 0 (
    (echo Backup failed: error during dump creation) >> "%backup_path%\mysql_backup_log.txt"
) else (echo Backup successful) >> "%backup_path%\mysql_backup_log.txt"
