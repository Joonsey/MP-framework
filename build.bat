python -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 goto throw_error
pyinstaller client.py --noconfirm -F
mkdir dist\assets
xcopy /s assets\ dist\assets

exit /b 0

:throw_error
echo "maaad sadge, install python and try again. If this keeps happening try installing the packages manually from the 'requirements.txt' file"
exit /b 1
