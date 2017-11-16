<html>
<?php
require_once "connect.php";
?>

<head>
<title>BILLTOMAIL - CONTROLLO</title>
</head>
<body>

<?php
$errore=$_GET['errore'];


if ($errore=='0') print "<h1><font color=green>BANDIERA MODIFICATA</font></h1>";
if ($errore=='1') print "<h1><font color=red>IMPOSSIBILE MODIFICARE BANDIERA MENTRE BILLTOMAIL VIENE ESEGUITO</font></h1>";
if ($errore=='2') print "<h1><font color=red>ERRORE SQL</font></h1>";
?>


<table border=1>
<tr><td>DATA INIZIO</td><td>DATA FINE</td><td>FORZATA?</td><td>IN ESECUZIONE?</td></tr>
<?php
$query="SELECT * FROM bandiera";
$result=mysql_query($query);
$row=mysql_fetch_array($result);
$inizio=$row['inizio'];
$fine=$row['fine'];
$forzata=$row['forzata'];
$esecuzione=$row['esecuzione'];
print "<form method=POST action=modifica_bandiera.php><tr><td><input type=text name=inizio value=$inizio></td><td><input type=text name=fine value=$fine></td>";
if ($forzata=='0'){
		print "<td>NO</td>";
}else{
		print "<td>SI</td>";
}
print "</td><input type=text name=esecuzione value=$esecuzione hidden=hidden>";
if ($esecuzione=='0'){
		print "<td>NO</td>";
}else{
		print "<td>SI</td>";
}
	print "</td>";
	##
	print "<td><input type=submit name=azione value=MODIFICA><tr></form>";

?>
</table>
<br><br>
<a href=index.php><input type=button value=HOME></a>
</BODY>
</HTML>