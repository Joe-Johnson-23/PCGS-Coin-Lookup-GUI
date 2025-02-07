# PCGS Coin Lookup GUI

A graphical user interface for looking up PCGS (Professional Coin Grading Service) coin information.

## Features
- Search coins by PCGS number
- Search coins by date
- Dynamic filtering of results
- Detailed coin information display

## Requirements
- Python 3.8 or higher
- Tkinter (system installation required on some platforms)

### Installing Tkinter (if needed):
- **macOS**: `brew install python-tk@3.11`
- **Linux**: `sudo apt-get install python3-tk`
- **Windows**: Included with Python installation

### Option 1: Run Standalone Executable (macOS)
1. Download the latest release
2. Open `PCGSLookup.app`
3. If you get a security warning, go to System Preferences → Security & Privacy and allow the app

### Option 2: Run from Source (All Platforms)
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pcgs-lookup-gui.git
   cd pcgs-lookup-gui
   ```
2. Create and activate virtual environment:
   ```bash
   python -m venv pcgs_env
   source pcgs_env/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python guiPCGS.py
   ```

## Usage
1. Enter a PCGS number or date to search
2. Click on items in the date list to see details
3. Use the clear button to reset all fields
4. Results will display in the main text area

## Building from Source
To create your own standalone executable:

Install PyInstaller
pip install pyinstaller

Create executable
pyinstaller --onefile \
--windowed \
--name "PCGSLookup" \
--icon=icons/app_icon.icns \
--add-data "pcgs_registry_cache.pkl:." \
--add-data "pcgsLookupFunction.py:." \
guiPCGS.py