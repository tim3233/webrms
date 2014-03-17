# !---------written by Felix Schueller (FSS)-----------------
# ! -INPUT:
# ! -OUTPUT:
# -DESCRIPTION: based on webrms by tim
# -TODO:
# -Last modified:  Mon Mar 17, 2014  16:44
# @author Felix Schueller
# -----------------------------------------------------------
import serial
import time
import random
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line

class controller_data(dict):
    next_id = 1
    def __init__(self):
        self['id']=controller_data.next_id
        self['fastest']= 0.0
        self['time']= 0.0
        self['fuel']= 0.0
        self['laps']= 0
        self['prev']= 0.0
        controller_data.next_id += 1


def logger(ws):
    
    # FSS---set up 6 driver 
    c_data = dict()
    for i in range(3):
        # c_data.append(controller_data())
        c_data[i+1]= controller_data()
    print c_data
    
    i = 0
    while True:
        i = i+1
        print("Try # ",i)
        try:
    #         # ser = serial.Serial('/dev/cu.NoZAP-PL2303-000013FA', 19200, timeout=0.05)
            # ser = open('raw_data/car1_no_fuel_min.txt')
            ser = open('raw_data/car1_no_fuel.txt')
            # ser = open('raw_data/car2_fuel_on_over_pitlane.txt')
            # ser = open('raw_data/car4_fuel_real.txt')

            line_saved=0
            fuel_saved_1=0
            fuel_at_start=0

            while 1<2:
    #             # ser.write("\"?")
                line = ser.readline()
                print "raw line", line
                # if line == '': # debug with file
                #     break


                if line!=line_saved:

                    ascii_string = line
                    # print line

                    first_bit = ascii_string[1:2]
                    cc=first_bit
                    # print "First bit: ",first_bit
                    # 1234567891011121314
                    # :TTTTTTVVS M B B A P$
                    # T = Tank Autos 1-6
                    # V immer 0
                    # S = 0 = rennen 
                    # M = Tankmodus 0: aus, 1: normal, 2: real
                    #   mit Pitlane +4
                    if first_bit == ":":
                        ascii_string2 = ascii_string[5:6]
                        hex_string=ascii_string2[0:1].encode('hex')[1:2]
                        print hex_string
                        decimal = int(hex_string,16)
                        print decimal
                        
                        ascii_string2 = ascii_string[11:12]
                        hex_string=ascii_string2[0:1].encode('hex')[1:2]
                        print hex_string
                        decimal = int(hex_string,16) - 4
                        print decimal
                        

                    
                    if first_bit!=":":
                        ascii_string = ascii_string[4:10]

                        hex_string=ascii_string[1:2].encode("hex")[1:2]+ascii_string[0:1].encode("hex")[1:2]
                        hex_string+=ascii_string[3:4].encode("hex")[1:2]+ascii_string[2:3].encode("hex")[1:2]
                        hex_string+=ascii_string[5:6].encode("hex")[1:2]+ascii_string[4:5].encode("hex")[1:2]

                        decimal=int(hex_string, 16)
                        cci = int(cc)
                        timer=str(decimal);

                        t_in_s =  (decimal - c_data[cci]['prev'])/1000.0
                        if t_in_s > 10 :
                            t_in_s = 5
                        
                        print t_in_s

                        c_data[cci]['time'] = t_in_s 
                        c_data[cci]['laps'] += 1 
                        if c_data[cci]['laps'] == 1 :
                            c_data[cci]['fastest'] = t_in_s 
                        elif t_in_s < c_data[cci]['fastest']:
                            c_data[cci]['fastest'] = t_in_s 
                        
                        c_data[cci]['fuel'] = random.randint(0,10) * 10
                        c_data[cci]['prev'] = decimal  
                        # ws.write_message(c_data[cci])

    #                     # print("Car:" + car_controller)
    #                     # print("Timestamp:" + timer +"ms")

    #                     # datafile = open("./data/car."+car_controller+".rnd", "a")
    #                     # print >> datafile, timer
    #                     # datafile.close()
                        line_saved=line
                        time.sleep(.02)
                        time.sleep(t_in_s)
        except:
            time.sleep(.02)
            # continue
            break
        break


    # ser.close()


if __name__ == '__main__':
    logger('test')

