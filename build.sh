pyinstaller main.spec
cp -rf scripts dist/Bailey.app/Contents/Frameworks/
cp -rf data dist/Bailey.app/Contents/Frameworks/
cp -rf scripts dist/main/_internal
cp -rf data dist/main/_internal
rm -rf build
