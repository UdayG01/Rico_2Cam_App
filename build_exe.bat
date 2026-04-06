call .venv\Scripts\activate.bat
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed --icon=favicon.png --add-data "favicon.png;." --add-data "logo-Renata-IoT_1_new2-768x256.png;." --add-data "logo-Renata-IoT_1_new2_darkmode.png;." main.py
echo Build complete! You can find your app in the "dist\main" folder.
