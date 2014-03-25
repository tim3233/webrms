#!---------written by Felix Schueller (FSS)-----------------
#! -INPUT:
#! -OUTPUT:
#-DESCRIPTION:
#-TODO:
#-Last modified:  Tue Mar 25, 2014  13:47
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

clients = []
dt = []
simulation = True


class driver:
    next_id = 1

    def __init__(self, name="Driver"):
        self.id = driver.next_id
        self.name = name
        driver.next_id += 1


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html",
                    drivers=alldrivers)



class DriverSetupHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        try:
            slot = int(self.get_argument("pk"))
            name = self.get_argument("value")
            if not slot or not name:
                self.write({"success": False})
            elif not len(name):
                self.write({"success": False})
            elif not 1 <= slot <= 6:
                self.write({"success": False})
            else:
                alldrivers[slot - 1].name = name
                self.write({"success": True})
        except:
            self.write({"success": False})

        self.flush()
        self.finish()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    last_msg = 'none'

    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients.append(self)
        print "WebSocket" + str(self.id) + " opened"
        # global dt # so data thread is checkable by other functions

    def on_message(self, message):
        """
        when we receive some message we want some message handler..
        """
        print "Received ", self.id, message
        self.last_msg = message
        if message == 'status':
            try:
                if dt[0].is_alive():
                    self.write_message("alive")
                else:
                    self.write_message("dead")
            except:
                self.write_message("dead")

        if message == 'start':
            try:
                if dt[0].is_alive():  #dt is alive, do nothing
                    self.write_message("alive")
                else:
                    del (dt[0])
                    # Last option set simulation (True) or real carerra cu (False)
                    dt.append(threading.Thread(target=webrms_logger.logger, args=[self, simulation]))
                    dt[0].start()
                    self.write_message("alive")
            except:  #dt is undefined, so logger is started for first time
                dt.append(threading.Thread(target=webrms_logger.logger, args=[self, simulation]))
                dt[0].start()
                self.write_message("alive")

    def on_close_wrapper(self):
        """ 
        Wrapper to make sure  on_close is also called if server cuts connection
        """
        self.close()
        self.on_close()

    def on_close(self):
        self.last_msg = 'stop'
        if self in clients:
            clients.remove(self)
        print 'Websocket closed', self.id


def wsSend(message):
    for ws in clients:
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
                                  (r'/driversetup', DriverSetupHandler),
                                  (r'/static/(.*)', tornado.web.StaticFileHandler),
                              ], **settings)

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
