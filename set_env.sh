# This shell script automates the procedure of creating virtual environment, 
# activating the virtual environment, and installing necessary Python packages
# as described in README.MD

/usr/bin/python3 -m venv .venv
source .venv/bin/activate
pip install pygame==2.5.2 
pip install pyinstaller
pip install Pillow
