#!---------written by Felix Schueller (FSS)-----------------
#! -INPUT:
#! -OUTPUT:
#-DESCRIPTION:
#-TODO:
#-Last modified:  Mon Mar 17, 2014  22:50
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

# we gonna store clients in dictionary..
#clients = dict()
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
        #clients[self.id] = {"id": self.id, "object": self}
        clients.append(self)
        print "WebSocket" +str(self.id) + " opened"
        if self.id == '1': # This is the data socket
            #self.write_message("Client %s received a message : %s" % (self.id, message))
            global dt # so data thread is checkable by other functions
            dt = threading.Thread(target=webrms_logger.logger,args=[self,clients[0],True])
            # dt = threading.Thread(target=handletest,args=[self])
            # rt = webrms_logger.logger(self)
            # print rt
            # handletest(self)
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
        #if self.id in clients:
            #del clients[self.id]
        #if self in wss:
            #wss.remove(self)

def wsSend(message):
    for ws in wss:
        ws.write_message(message)

def handletest(client):
    i =0
    go = True
    while go: 
        d_data= dict()
        d_data['id'] = random.randint(0,5) 
        d_data['time'] = 0.22 +i
        d_data['fastest'] = 0.11 +i
        d_data['laps'] = i +1
        # d_data['fuel'] = max(100 - i *10,0) 
        d_data['fuel'] = random.randint(0,100) 
        client.write_message(d_data)
        i = i+1
        time.sleep(2)
        if i > 15:
            go = False

        #wsSend(" ")

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
