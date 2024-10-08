@echo off
set dir_path=%cd%
echo %dir_path%
@echo on
python "%dir_path%\get.py" %*
pause