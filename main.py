import unittest

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class Controller( webapp.RequestHandler ):
    def get(self):
        #String
        if type(self._output) == str:
            self.response.out.write(self._output)

        #Redirect
        if type(self._output) == Redirect:
            self.redirect(self._output.url)

        #Template
        if type(self._output) == Template:
            pass #render template

    def __call__(self):
        self._output = self.http_get()
        return self

class Redirect(object):
    def __init__(self, url):
        self.url = url

class Template(object):
    def __init__(self, file, data):
        self.file = file
        self.data = data

#APPLICATION
class Home(Controller):
    def http_get(self):
        return 'Hello world!'

class Contact(Controller):
    def http_get(self):
        return Redirect('/')

class AboutUs(Controller):
    def __init__(self, _users=None):
        if _users:
            self.users = _users
        else:
            self.users = users

    def http_get(self):
        current_user = self.users.get_current_user()
        return Template('/about_us.html', 'We are the robots')

class Login(Controller):
    def __init__(self, _users=None):
        if _users:
            self.users = _users
        else:
            self.users = users

    def http_get(self):
        login_url = self.users.create_login_url('/')
        return Redirect(login_url)

def application():
    return webapp.WSGIApplication([ ( '/', Home() ),
                                    ( '/contact', Contact() ),
                                    ( '/about_us', AboutUs() ),
                                    ( '/login', Login() ),
                                  ], debug=True)

def main():
    run_wsgi_app(application())

if __name__ == '__main__':
    main()
