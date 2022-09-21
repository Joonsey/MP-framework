python -m pip install -r requirements.txt
python -m pyinstaller client.py --noconfirm -F --noconsole
mkdir dist/assets
cp assets/* dist/assets/
