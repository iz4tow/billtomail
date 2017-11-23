IF EXIST .git GOTO pull
git init
git remote add origin https://github.com/iz4tow/EXEFATTUREONLINE.git
echo "INIZIALIZZATO"
:pull
git pull https://github.com/iz4tow/EXEFATTUREONLINE.git
start FATTUREONLINE.EXE
exit