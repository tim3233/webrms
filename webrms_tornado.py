#!---------written by Felix Schueller (FSS)-----------------
#! -INPUT:
#! -OUTPUT:
#-DESCRIPTION:
#-TODO:
#-Last modified:  Mon Mar 17, 2014  23:21
#@author Felix Schueller
#-----------------------------------------------------------
import os
import time
import threading
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line
import webrms_logger
import random

define("port", default=8888, help="run on the given port", type=int)

clients =[]

class driver:
    next_id = 1
    def __init__(self,name="Driver"):
        self.id = driver.next_id
        self.name = name 
        driver.next_id += 1

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html", 
                    drivers=alldrivers)   

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients.append(self)
        print "WebSocket" +str(self.id) + " opened"
        if self.id == '1': # This is the data socket
            global dt # so data thread is checkable by other functions
            # Last option set simulation (True) or real carerra cu (False)
            dt = threading.Thread(target=webrms_logger.logger,args=[self,clients[0],True])
            dt.start()
    
    def on_message(self, message):        
        """
        when we receive some message we want some message handler..
        """
        if self.id == '2': # this is the control socket
            if message == 'status':
                if dt.is_alive():
                    self.write_message("alive")
                else:
                    self.write_message("dead")
            #if message == 'fuel1':
               #self.on_close_wrapper() 

    def on_close_wrapper (self):
        """ 
        Wrapper to make sure  on_close is also called if server cuts connection
        """
        self.close()
        self.on_close()
        
    def on_close(self):
        print 'Websocket closed', self.id
        if self in clients:
            clients.remove(self)

def wsSend(message):
    for ws in wss:
        ws.write_message(message)

settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
)   

# FSS---set up 6 driver 
alldrivers = list()
print len(alldrivers)
for i in range(6):
    alldrivers.append(driver())



app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws', WebSocketHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler),
],**settings)


if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
