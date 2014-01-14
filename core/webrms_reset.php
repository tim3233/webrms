<?php

for($i=1;$i<=6;$i++){
$fileName = 'data/car.'.$i.'.rnd';

if (file_exists($fileName)) {
    unlink($fileName);
    fopen($fileName,"x+");
    chmod($fileName, 0777);
}

}


?>