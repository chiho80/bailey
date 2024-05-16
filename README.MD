## Initial tasks
Before running the game, create and acrivate a virtual environment, then install
a required package - [pygame](https://www.pygame.org/). 

### Mac
```
/usr/bin/python3 -m venv .venv
source .venv/bin/activate
pip install pygame==2.5.2 
```

### Windows
```
python -m venv .venv
.venv\Scripts\activate
pip install pygame==2.5.2 
```   
When facing the error related the security policy during activating the virtual environment, 
run the Windows PowerShell with administration privilege, then execute this ```Set-ExecutionPolicy Unrestricted``` 
on the shell, then select Y on the question. Now you will be able to activate the virtual environment.

## Distribute the game
The converter package [pyinstaller](https://pyinstaller.org/en/stable/) is a good option to make executables.   
```
pip install pyinstaller
pip install Pillow
```   
Run ```build_Mac.sh``` to create an app for MacOS ```bailey.app``` under dist folder. 
Run ```build_Win.bat``` to create an app for MS Windows ```bailey.exe``` under dist folder. 
The built-in security monitoring tools of MS Windows may block running the pyinstaller during building. 
If that is happening, temporarely disable the real-time monitoring them enable after the building is finished.
If the ```build_Win.bat``` is not running without clear reason, execute the commands in the bat file, one by one.

## Run game
```python main.py [level]```  
Make sure to activate the virtual environment before run, using one of the commands ```source .venv/bin/activate``` on Mac or ```.venv\Scripts\activate``` on Windows. If ```[level]``` is not provided, level 0 (the first stage) will be loaded.

## Keys
* Left or A - Move to the left   
* Right or D - Move to the right   
* Up or W - Jump   
* Lshift + (Left or A) - Run to the left   
* Lshift + (Right or D) - Run to the right   
* X or L - Dash and kill enemy   
* ESC or P - Pause   
* M - Mute or unmute   
* Plus (+) or Minus (-) - Adjust display size   


## Edit map
```python editor.py [level]```  
If ```[level]``` is not provided, level 0 (the first stage) will be open. 
  
## Copyrights
Freely download and update Python codes. Do not push the changes you made. Other resources, including SFXs, music, tile & entity images, cannot be redistributed without permission of original creators.  
* Code developed by [Bailey's Dad](https://github.com/chiho80/bailey)  
* Ground Tile images collected from grafxkid.itch.io  
* Squirrel sprites based on original artworks of moose-stache.itch.io  
* Cat sprites collected from https://craftpix.net/freebies/free-street-animal-pixel-art-asset-pack/
* SFXs collected from pixabay.com, mixkit.co  
* Background music from PlayOnLoop.com Licensed under Creative Commons by Attribution 4.0