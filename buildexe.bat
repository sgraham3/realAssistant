pyinstaller --name "realAssistant" --onefile --windowed --add-data "metadata.ini;." --icon "icon.ico" main.py
rem pyinstaller --clean realAssistant.spec