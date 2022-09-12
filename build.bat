python -m pip install -r requirements.txt
pyinstaller client.py --noconfirm
mkdir dist/client/assets
xcopy /s/y assets/* dist/client/assets/
