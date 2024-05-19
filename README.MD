## Initial tasks
Before running the game or building executable, create and activate a virtual environment, then install
a required package - [pygame](https://www.pygame.org/). Follow one of the instructions depending on your operating system. 
A package ```pyinstaller``` is optional, and only needed if you want to build the executable. 
If ```pyinstaller``` crashes during building, ```pillow``` may solve the issue.

### On Mac OS
```
/usr/bin/python3 -m venv .venv   
source .venv/bin/activate   
pip install pygame==2.5.2   
pip install pyinstaller   
pip install pillow   
```   
Or simply run the script ```set_env.sh```.

### On MS Windows
```
python -m venv .venv   
.venv\Scripts\activate   
pip install pygame==2.5.2   
pip install pyinstaller   
pip install pillow   
```   

Installing the packages on Mac OS is straightforward while MS Windows brings many hurdles. 
On MS Windows, when facing the error related to the security policies during activating the virtual environment, 
run the Windows PowerShell with administration privilege, then issue ```Set-ExecutionPolicy Unrestricted``` 
on the shell prompt. Select ```Y``` on the questions. You will be able to activate the virtual environment 
to continue.  

## Run the game   
To run the game using Python interpreter under the virtual environment, issue ```python main.py [level]``` 
on the shell prompt. To activate the virtual environment, use one of the commands ```source .venv/bin/activate``` 
on Mac OS or ```.venv\Scripts\activate``` on Windows.  If ```[level]``` is not provided, stage 1 will be loaded.    

### Keyboard controls 
* ```&larr;``` or ```A``` - Move to the left   
* ```&rarr;``` or ```D``` - Move to the right   
* ```&uarr;``` or ```W``` - Jump   
* Left ```shift``` + (```&larr;``` or ```A```) - Run to the left   
* Left ```shift``` + (```&rarr;``` or ```D```) - Run to the right   
* ```X``` or ```L``` - Dash and kill enemy   
* ```esc``` or ```P``` - Pause   
* ```M``` - Mute or unmute   
* ```+``` or ```-``` - Adjust display size   

## Edit maps
You may modiry the maps or create new map using map editor. Issue following command on shell prompt.   
```python editor.py [level]```   
If ```[level]``` is not provided, level 1 will be open.   

### Controls
* ```G``` - Toggle on/offgrid   
* ```A```, ```S```, ```D```, ```W``` - Move viewport   
* ```T``` - Autotile   
* ```C``` or ```V``` or Mouse scroll - Change tile class   
* ```Z``` or ```X``` or ```Shift``` + Mouse scroll - Change variant   
* ```M``` - Toggle start/stop the motion for dynamic tiles   
* ```O``` - Save map   
* ```esc``` - Quit the editor   
* Mouse position: Locate a map element
* Mouse left click: Place a map element
* Mouse right click: Delete a map element 
  
## Build executable
The converter package [pyinstaller](https://pyinstaller.org/en/stable/) is a good option to make executables. 
Install ```pyinstaller``` on the virtual environment using following command. ```pillow``` is optional. 
```
pip install pyinstaller
pip install Pillow
```   
Run ```build.sh``` to create an app for Mac OS ```bailey.app``` under dist folder. 
Run ```win_build.bat``` to create an app for MS Windows ```bailey.exe``` under dist folder. 
The built-in security monitoring tools of MS Windows may block running the pyinstaller. 
If blocked, temporarely disable the real-time monitoring feature of the security tool, try building again, then enable back the real-time monitoring feature after the building is completed. If the ```win_build.bat``` is doing nothing in the shell, manually issue the commands in the ```win_build.bat``` file.

## Copyrights
Freely download, modify, and redistribute the Python codes in this repository. Do not push or PR the changes you made. Other resources, including SFXs, music, tile & entity images, cannot be redistributed without permission of original creators.  
* Code developed by [Bailey's Dad](https://github.com/chiho80/bailey)  
* Ground Tile images collected from grafxkid.itch.io  
* House images from https://twitter.com/Vryell
* Squirrel sprites based on original artworks of moose-stache.itch.io  
* Cat sprites collected from https://craftpix.net/freebies/free-street-animal-pixel-art-asset-pack/
* SFXs collected from pixabay.com, mixkit.co  
* Background music from PlayOnLoop.com Licensed under Creative Commons by Attribution 4.0
