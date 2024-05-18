.venv\Scripts\activate
pyinstaller -y main.spec
copy scripts dist/main/_internal/scripts -Recurse
copy data dist/main/_internal/data -Recurse
rd build -Recurse -Force
