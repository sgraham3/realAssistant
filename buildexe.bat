pyinstaller --name "realAssistant" --onefile --windowed --add-data "metadata.ini;." --icon "icon.ico" realAssistant.py
rem pyinstaller --clean realAssistant.spec