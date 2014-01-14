import serial
import time

while True:
        try:
                ser = serial.Serial('/dev/cu.NoZAP-PL2303-000013FA', 19200, timeout=0.05)

                line_saved=0
                fuel_saved_1=0
                fuel_at_start=0

                while 1<2:
                        ser.write("\"?")
                        line = ser.readline()
                        
        
                        if line!=line_saved:
                        
                                ascii_string = line

                                first_bit = ascii_string[1:2]
                                car_controller=first_bit

                                if first_bit!=":":
                                        ascii_string = ascii_string[4:10]

                                        hex_string=ascii_string[1:2].encode("hex")[1:2]+ascii_string[0:1].encode("hex")[1:2]
                                        hex_string+=ascii_string[3:4].encode("hex")[1:2]+ascii_string[2:3].encode("hex")[1:2]
                                        hex_string+=ascii_string[5:6].encode("hex")[1:2]+ascii_string[4:5].encode("hex")[1:2]
                
                                        decimal=int(hex_string, 16)
                                        timer=str(decimal);
        
                                        print("Car:" + car_controller)
                                        print("Timestamp:" + timer +"ms")
                
                                        datafile = open("/Applications/XAMPP/xamppfiles/htdocs/webrms/core/data/car."+car_controller+".rnd", "a")
                                        print >> datafile, timer
                                        datafile.close()
                                        line_saved=line
                                        time.sleep(.02)
        except:
                time.sleep(.02)
                continue
        break


ser.close()
