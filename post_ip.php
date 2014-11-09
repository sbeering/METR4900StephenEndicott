<?php

if( $_POST["ip_pub"] && $_POST["ip_int"] && $_POST["secretstring"] == "I am so awesome" && $_POST["name"]){

	$file = 'tmp/'.$_POST["name"].'_ip.txt';

	

	// Write the contents of IP address to file

	file_put_contents($file, $_POST["ip_pub"].'\t'.$_POST["ip_int"], LOCK_EX);

	echo 'Success';



}

else{

	echo 'Nope';

}

?>