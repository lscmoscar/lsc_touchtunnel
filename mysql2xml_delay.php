<?php

include('/var/www/test_memorytunnel/prod_assets/mysql2xml.php');

toxml('LOCALHOST', 'MySQL USER', 'MySQL PASSWORD', 'MySQLDB', 'SELECT * FROM MySQLDB WHERE new="2" ORDER BY postinfo', 1, '/var/www/test_memorytunnel/prod_assets/output_new.xml');

exec('/var/www/test_memorytunnel/prod_assets/./update_twitter.py');

?>
