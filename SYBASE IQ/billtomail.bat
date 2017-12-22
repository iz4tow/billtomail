@echo off
echo "CONTROLLI PRELIMINARI" > log.txt
date /T >> log.txt
time /T >> log.txt
net use S: /DELETE /YES
net use S: \\192.168.168.102\d$ /USER:administrator 12mwwbb

rem CONTROLLO FILE PILOTA
dir S:\PDFATTURE\Bill2Mail\pilota*.txt >> log.txt
if exist ERRORE.err  goto inizio
if not exist S:\PDFATTURE\Bill2Mail\pilota_mail.txt goto uscita
if not exist S:\PDFATTURE\Bill2Mail\pilota_artfatt3.txt goto uscita
if not exist S:\PDFATTURE\Bill2Mail\pilota_spool.txt goto uscita


:inizio
echo Y | del ERRORE.err  
echo "INIZIO BILLTOMAIL" > ESECUZIONE.txt
echo Y | del S:\PDFATTURE\Bill2Mail\pilota_mail.txt
echo Y | del S:\PDFATTURE\Bill2Mail\pilota_artfatt3.txt
echo Y | del S:\PDFATTURE\Bill2Mail\pilota_spool.txt
date /T >> ESECUZIONE.txt
time /T >> ESECUZIONE.txt


billtomail.exe >> log.txt
log.exe

echo Y | del ESECUZIONE.txt

:uscita
set data=%date:~6,4%%date:~3,2%%date:~0,2%
set ora=%time:~0,2%%time:~3,2%%time:~6,2%
copy log.txt logs\%data%_%ora%.log
echo Y | del log.txt

rem CANCELLAZIONE LOG VECCHI > 120 GG
Forfiles /p .\LOG\ /s /m *.log /d -120 /c "cmd /c del /q @path"

net use S: /DELETE /YES

exit
