#!--------written by Felix Schueller (FSS)-----------------
# -INPUT:
# -OUTPUT:
#-DESCRIPTION:
#-TODO:
#-Last modified:  Thu Mar 13, 2014  23:36
#@author Felix Schueller
#-----------------------------------------------------------

import web
#import view, config
#from view import render

class driver:
    next_id = 0
    def __init__(self):
        self.id = driver.next_id
        self.name = "Not Set"
        driver.next_id += 1

class index:
    def GET(self):

        alldrivers = list()
        for i in range(6):
            alldrivers.append(driver())
        #return render.base(view.listing())
        return render.base(alldrivers,"PyWebRMS")

render = web.template.render('templates/')

urls = (
    '/', 'index'
)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
