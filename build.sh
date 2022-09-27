source venv/bin/activate
pip install -r requirements.txt
pyinstaller client.py --noconfirm -F --noconsole
mkdir -p dist/assets
cp assets/* dist/assets/
