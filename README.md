PyWebrms is a python based slotcar race management system with a browser frontend.  
Orignial code was forked from https://github.com/tim3233/webrms.

Features:

- Displays last lap, number of laps and fastest lap
- Fuel display
- Configurable driver names
- Reset all or individual drivers
- Simulation mode so no racetrack is required to develop on this code


Requirements:

pip install tornado

pip install pyserial

frontend and server done with tornado (no apache/... needed)

set your serial address in webpy_logger

set simulation flag to true or false in webpy_tornado

to start webserver: python webrms_tornado.py

then point your browser to the given address
(usually localhost:8888)

