<?php
require_once "connect.php";
$inizio=$_POST['inizio'];
$fine=$_POST['fine'];
$forzata='1';
$esecuzione=$_POST['esecuzione'];
$azione=$_POST['azione'];



if ($azione=='MODIFICA' AND $esecuzione==0){
	$sql="TRUNCATE TABLE bandiera"; #ESISTE SEMPRE E SOLO 1 BANDIERA!!!
	mysql_query($sql);
	$sql="INSERT INTO BANDIERA (inizio,fine,forzata,esecuzione) VALUES ('$inizio','$fine','$forzata','0')";
	mysql_query($sql);
	if ( !empty( $error = mysql_error() ) )
	{
		header("Location: bandiera.php?errore=2");
		exit;
	}else{
		header("Location: bandiera.php?errore=0");
		exit;
	}
}else if ($esecuzione!=0){
		header("Location: bandiera.php?errore=1");
		exit;
	}
?>