## Initial tasks
Before running the game, create and acrivate a virtual environment, then install
required packages - [pygame](https://www.pygame.org/) and [pygbag](https://pypi.org/project/pygbag/). 

### Mac
```
/usr/bin/python3 -m venv .venv
source .venv/bin/activate
pip install pygame==2.5.2 
pip install pygbag
```

### Windows
```
py -m venv .venv
.venv\Scripts\activate
pip install pygame==2.5.2 
pip install pygbag
```

## Run game
```python main.py [level]```  
Make sure to activate the virtual environment before run, using one of the commands ```source .venv/bin/activate``` on Mac or ```.venv\Scripts\activate``` on Windows. If ```[level]``` is not provided, level 0 (the first stage) will be loaded. 

## Edit map
```python editor.py [level]```  
If ```[level]``` is not provided, level 0 (the first stage) will be open. 
  
## Copyrights
Developed by [Bailey's Dad](https://github.com/chiho80/bailey)  
Tile images collected from grafxkid.itch.io  
Squirrel sprites based on original artworks of moose-stache.itch.io  
SFXs collected from pixabay.com, mixkit.co  
Music from #uppbeat (Free For Creators!) https://uppbeat.io/t/giulio-fazio/8bit-canon 8bit Canon by Guilio Fazio