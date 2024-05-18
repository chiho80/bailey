.venv\Scripts\activate
pyinstaller -y main.spec
xcopy scripts dist/main/_internal/scripts
xcopy data dist/main/_internal/data
rd build -Recurse -Force
