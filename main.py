import unittest

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class Controller( webapp.RequestHandler ):
    def get(self, *args):
        self.exe_get(self.http_get, *args)

    def exe_get(self, t, *args):
        get_response = t(*args)

        #String
        if type(get_response) == str:
            self.response.out.write(get_response)

        #Redirect
        if type(get_response) == Redirect:
            self.redirect(get_response.url)

        #Template
        if type(get_response) == Template:
            pass #render template

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
    def http_get(self):
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

class News(Controller):
    def http_get(self, word):
        return word


def application():
    return webapp.WSGIApplication([ ( '/', Home ),
                                    ( '/contact', Contact ),
                                    ( '/about_us', AboutUs ),
                                    ( '/login', Login ),
                                    ( '/news/([-\w]+)', News ),
                                  ], debug=True)

def main():
    run_wsgi_app(application())

if __name__ == '__main__':
    main()
