<?php
function toxml($host, $user, $password, $db, $query, $mode, $output) {
  if(!$dbconnect = mysql_connect($host, $user, $password)) {
     echo "Connection failed to the host.";
     exit;
  } 
  if (!mysql_select_db($db)) {
     echo "Cannot connect to database.";
     exit;
  } 

  /*if ($mode == 1) {
    mysql_query('UPDATE MySQLDB SET new="2" WHERE new="1" AND postinfo<(NOW()-12*60*60)');
  }*/

  mysql_query("SET NAMES 'utf8' COLLATE 'utf8_unicode_ci'",$dbconnect);
  $dbresult = mysql_query($query, $dbconnect);
  $doc = new DomDocument('1.0');

  $root = $doc->createElement('Entries');
  $root = $doc->appendChild($root);

  while($row = mysql_fetch_assoc($dbresult)) {
    $entry = $doc->createElement('Entry');
    $entry = $root->appendChild($entry);
    foreach ($row as $fieldname => $fieldvalue) {
      if ($fieldname == "id") {
        $entry->setAttribute($fieldname, $fieldvalue);
      } else {
        if ($mode == 0) {
          $child = $doc->createElement($fieldname);
          $child = $entry->appendChild($child);
          $value = $doc->createTextNode($fieldvalue);
          $value = $child->appendChild($value);
        } else {
          $entry->setAttribute($fieldname, $fieldvalue);
        }
      }
    }   
  } 

  $xml_string = $doc->saveXML();

  //echo $xml_string;

  $Handle = fopen($output, 'w');
  fwrite($Handle, $xml_string);
  fclose($Handle);
  
  if ($mode == 1) {
    mysql_query('UPDATE MySQLDB SET new="0" WHERE new="2"');
  }
}

?>
