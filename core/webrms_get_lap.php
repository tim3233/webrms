<?php

$car=$_POST['car'];

$fileName = 'data/car.'.$car.'.rnd';

if (file_exists($fileName)) {

$file = new \SplFileObject($fileName);
$file->seek($file->getSize());

$lines = $file->key()-1;

$file->setFlags(\SplFileObject::READ_CSV);

$counter = 0;
$records = 2;
$seek = $lines - $records;

$file->seek($seek);

$lap_data = array();
while ($counter++ < $records) {
    try {
        $line = $file->fgets();
        $lap_data[] = $line;
    } catch (\Exception $e) {
    }
}

$last_round_in_ms=$lap_data[1]-$lap_data[0];

$last_round_in_s=round($last_round_in_ms/1000,4);

if($lap_data>0){

	echo json_encode(array(last_round=>$last_round_in_s,rounds=>$lines));

} else {

    echo json_encode(array(last_round=>0,rounds=>0));


}

} else{
    
    echo json_encode(array(last_round=>0,rounds=>0));

}

?>
