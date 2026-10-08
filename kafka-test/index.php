<?php
    $writefile = fopen("data.txt", "a+") or die("Unable to open file!");

    $content = isset($GLOBALS["HTTP_RAW_POST_DATA"]) ? $GLOBALS["HTTP_RAW_POST_DATA"] : '';
    fwrite($writefile, $content);
    $content = isset($GLOBALS["HTTP_RAW_GET_DATA"]) ? $GLOBALS["HTTP_RAW_GET_DATA"] : '';
    fwrite($writefile, $content);
    echo $content;
    echo '</br>';

    $xmlstr= file_get_contents("php://input");
    echo $xmlstr;
    echo '</br>';
    fwrite($writefile, $xmlstr);

    fwrite($writefile, "POST: \r\n");
    foreach ($_POST as $v){
        fwrite($writefile, $v);
        echo $v;
        echo '</br>';
    }
    fwrite($writefile, "GET: \r\n");
    foreach ($_GET as $v){
        fwrite($writefile, $v);
        fwrite($writefile, "\r\n");
        echo $v;
        echo '</br>';
    }
    fwrite($writefile, "HEADERS: \r\n");
    foreach (getallheaders() as $name => $value) {
        fwrite($writefile, $value);
        fwrite($writefile, "\r\n");
        echo "$name: $value";
        echo '</br>';
    }
    fclose($writefile);

    $myfile = fopen("webdictionary.txt", "r") or die("Unable to open file!");
    echo fread($myfile, filesize("webdictionary.txt"));
    fclose($myfile);
    echo '</br>';
?>