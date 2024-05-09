## Initial tasks
To run the game, create and acrivate a virtual environment, then install
required packages (pygame and pygbag). 

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
```python main.py```
Remember activate the virtual environment before run, using one of the commands ```source .venv/bin/activate``` on Mac or ```.venv\Scripts\activate``` on Windows



## Edit map
If [level] is not provided, level 0 (the first stage) will be open.
```python editor.py [level]```