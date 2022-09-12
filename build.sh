python -m pip install -r requirements.txt
pyinstaller client.py --noconfirm
mkdir dist/client/assets
cp assets/* dist/client/assets/
