#!--------written by Felix Schueller (FSS)-----------------
# -INPUT:
# -OUTPUT:
#-DESCRIPTION:
#-TODO:
#-Last modified:  Fri Mar 14, 2014  23:29
#@author Felix Schueller
#-----------------------------------------------------------

import web
#import view, config
#from view import render

urls = (
    '/', 'index',
    '/setup', 'setup'
)

class driver:
    next_id = 1
    def __init__(self):
        self.id = driver.next_id
        self.name = "Not Set"
        driver.next_id += 1

class index:
    def GET(self):
        return render.base(listing(),"PyWebRMS")

class setup:
    def GET(self):
        return render.setup()

def listing():
    return render.view()

# FSS---set up 6 driver 
alldrivers = list()
print len(alldrivers)
for i in range(6):
    alldrivers.append(driver())

# FSS---driver setup as global variable 
t_globals = dict(
          driver_setup=alldrivers,
)

render = web.template.render('templates/',globals=t_globals)
render._keywords['globals']['render'] = render

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
