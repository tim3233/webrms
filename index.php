<?php

    for($i=1;$i<=6;$i++){
    $fileName = 'core/data/car.'.$i.'.rnd';
    $fuelName = 'core/data/car.'.$i.'.fuel';
    $startName = 'core/data/start.log';
    
    if (!file_exists($fileName)) {
	fopen($fileName,"x+");
	chmod($fileName, 0777);
    }
    if (!file_exists($fuelName)) {
	fopen($fuelName,"x+");
	chmod($fuelName, 0777);
    }
    
    }
    
     if (!file_exists($startName)) {
	fopen($startName,"x+");
	chmod($startName, 0777);
    }


?>
<!DOCTYPE html>
<html>
    <head>
	<title>webrms 0.1</title>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
	<link href="css/style.css" rel="stylesheet" media="screen">
	<link href='http://fonts.googleapis.com/css?family=Oswald:400,700,300' rel='stylesheet' type='text/css'>
	<script src="js/jquery-2.0.3.min.js"></script>
	<script src="js/bootstrap.min.js"></script>
    </head>
    <body>
	<script>
	    function getLaps(car) {
		
		    var car_id=car;
		  	    
		    var request = $.ajax({
			    url: 	"core/webrms_get_lap.php",
			    type: 	"POST",
			    data: 	{car: car_id},
			    dataType: "html"
			});
			request.done(function(msg) {
				var lapData = jQuery.parseJSON(msg);
							
				if(lapData.last_round>0){
				    $("#driver_laptime_"+car_id).html(lapData.last_round + ' s');
				    $("#driver_laprounds_"+car_id).html(lapData.rounds);
				}
		    });
			
		    setTimeout(function () {
				    getLaps(car_id)
				}, 500);
		}
		
	    $( document ).ready(function() {
		
		//Rundenzähler starten
		getLaps(1);
		getLaps(2);
		getLaps(3);
		getLaps(4);
		getLaps(5);
		getLaps(6);
		
		//Start-Server-Function
		
		$("#start").click(function(){
		
		});
		
		//Reset-Function
		
		$("#reset").click(function(){
		var request = $.ajax({
			    url: 	"core/webrms_reset.php",
			    type: 	"POST",
			    data: 	{reset: 'true'},
			    dataType: "html"
			});
		});
	    
	    });
	</script>
	<div class="top-menu">
	    <div class="container">
		<div class="row">
		    <div class="span4">
			    <div class="btn-group">
				<a class="btn dropdown-toggle  btn-inverse" data-toggle="dropdown" href="#">
				    Rennen
				    <span class="caret"></span>
				</a>
				<ul class="dropdown-menu">
				    <li><a href="#" id="reset">Zur&uuml;cksetzen</a></li>
				</ul>
			    </div>
		    </div>
		</div>
	    </div>
	</div>
	<div class="container rennergebnisse"> 
	    <div class="row">
		<div class="span12 header">
		    <div class="span3">
			Fahrer
		    </div>
		    <div class="span2">
			letzte Runde
		    </div>
		    <div class="span2">
			Runden
		    </div>
		     <div class="span2">
			beste Runde
		    </div>
		</div>
	    </div>
	    <div class="row">
		<div class="span12">
		    <div class="span3">
			Fahrer 1
		    </div>
		    <div class="span2 lap-time" id="driver_laptime_1">
			0.0000 s
		    </div>
		     <div class="span2" id="driver_laprounds_1">
			0
		    </div>
		     <div class="span2 lap-time" id="driver_besttime_1">
		     0.0000s
		    </div>
		</div>
	    </div>
	    <div class="row">
		<div class="span12">
		    <div class="span3">
			Fahrer 2
		    </div>
		    <div class="span2 lap-time" id="driver_laptime_2">
			0.0000 s
		    </div>
		    <div class="span2" id="driver_laprounds_2">
			0
		    </div>
		      <div class="span2 lap-time" id="driver_besttime_2">
		     0.0000s
		    </div>
		</div>
	    </div>
	    <div class="row">
		<div class="span12">
		    <div class="span3">
			Fahrer 3
		    </div>
		    <div class="span2 lap-time" id="driver_laptime_3">
			0.0000 s
		    </div>
		     <div class="span2" id="driver_laprounds_3">
			0
		    </div>
		      <div class="span2 lap-time" id="driver_besttime_3">
		     0.0000s
		    </div>
		</div>
	    </div>
	    <div class="row">
		<div class="span12">
		    <div class="span3">
			Fahrer 4
		    </div>
		    <div class="span2 lap-time" id="driver_laptime_4">
			0.0000 s
		    </div>
		     <div class="span2" id="driver_laprounds_4">
			0
		    </div>
		      <div class="span2 lap-time" id="driver_besttime_4">
		     0.0000s
		    </div>
		</div>
	    </div>
	     <div class="row">
		<div class="span12">
		    <div class="span3">
			Fahrer 5
		    </div>
		    <div class="span2 lap-time" id="driver_laptime_5">
			0.0000 s
		    </div>
		     <div class="span2" id="driver_laprounds_5">
			0
		    </div>
		      <div class="span2 lap-time" id="driver_besttime_5">
		     0.0000s
		    </div>
		</div>
	    </div>
	      <div class="row">
		<div class="span12">
		    <div class="span3">
			Fahrer 6
		    </div>
		    <div class="span2 lap-time" id="driver_laptime_6">
			0.0000 s
		    </div>
		     <div class="span2" id="driver_laprounds_6">
			0
		    </div>
		      <div class="span2 lap-time" id="driver_besttime_6">
		     0.0000s
		    </div>
		</div>
	    </div>
	</div>
    </body>
</html>