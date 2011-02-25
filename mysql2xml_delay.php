<?php

include('PATH/mysql2xml.php');

toxml('LOCALHOST', 'MYSQL USER', 'MYSQL PASSWORD', 'MYSQLDB', 'SELECT * FROM MYSQLTABLE WHERE new="2" ORDER BY postinfo', 1, 'PATH/output_new.xml');

exec('PATH/./update_twitter.py');

?>
