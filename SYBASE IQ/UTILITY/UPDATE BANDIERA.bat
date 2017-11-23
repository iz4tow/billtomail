IF EXIST .git GOTO pull
git init
echo "INIZIALIZZATO"
:pull
git pull https://github.com/iz4tow/EXEBILLTOMAIL.git
start GUIBANDIERA.EXE
exit