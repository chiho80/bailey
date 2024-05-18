## Initial tasks
Before running the game or building executable, create and acrivate a virtual environment, then install
a required package - [pygame](https://www.pygame.org/). Follow one of the instructions depending on your operating system.

### On Mac OS
```
/usr/bin/python3 -m venv .venv
source .venv/bin/activate
pip install pygame==2.5.2 
```

### On MS Windows
```
python -m venv .venv
.venv\Scripts\activate
pip install pygame==2.5.2 
```   
When facing the error related to the security policies during activating the virtual environment, 
run the Windows PowerShell with administration privilege, then issue ```Set-ExecutionPolicy Unrestricted``` 
on the shell prompt. Select Y on the question. Now you will be able to activate the virtual environment.

## Run the game   
To run the game using Python interpreter under the virtual environment, issue ```python main.py [level]``` 
on the shell prompt. To activate the virtual environment, use one of the commands ```source .venv/bin/activate``` 
on Mac OS or ```.venv\Scripts\activate``` on Windows.  If ```[level]``` is not provided, stage 1 will be loaded.    

## Keyboard controls 
* Left or A - Move to the left   
* Right or D - Move to the right   
* Up or W - Jump   
* Lshift + (Left or A) - Run to the left   
* Lshift + (Right or D) - Run to the right   
* X or L - Dash and kill enemy   
* ESC or P - Pause   
* M - Mute or unmute   
* Plus (+) or Minus (-) - Adjust display size   

## Edit maps
You may modiry the maps or create new map using map editor. Issue following command on shell prompt.   
```python editor.py [level]```   
If ```[level]``` is not provided, level 1 will be open.   

### Keys used   
* ```G```: toggle on/offgrid   
* ```A```, ```S```, ```D```, ```W```: move viewport   
* ```T```: autotile   
* ```Z``` or ```X```: change variant   
* ```C``` or ```V```: change tile class   
* ```M```: toggle start/stop the motion for dynamic tiles   
* ```O```: save map   
* ```ESC```: quit the editor   
  
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