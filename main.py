import unittest

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Controller( webapp.RequestHandler ):
    def get(self):
        if type(self._output) == str:
            self.response.out.write(self._output)

    def __call__(self):
        self._output = self.http_get()
        return self


#Application
class Home(Controller):
    def http_get(self):
        return 'Hello world!'

def application():
    return webapp.WSGIApplication([ ( '/home', Home() ) ], debug=True)

def main():
    run_wsgi_app(application())

if __name__ == '__main__':
    main()
