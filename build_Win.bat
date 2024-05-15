.venv\Scripts\activate
pyinstaller -y main.spec
copy scripts dist/main/_internal
copy data dist/main/_internal
rd build -Recurse -Force
