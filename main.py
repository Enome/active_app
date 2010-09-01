import unittest

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class Controller( webapp.RequestHandler ):
    def __init__(self, _users=None):
        """constructor injection or something that looks
        like it"""
        self.users = _users or users

    def get(self, *args):
        self.exe_get(self.http_get, *args)

    def exe_get(self, http_get, *args):
        """Based on the return type of http_get a
        response is created"""
        get_response = http_get(*args)

        #String
        if type(get_response) == str:
            self.response.out.write(get_response)

        #Redirect
        if type(get_response) == Redirect:
            self.redirect(get_response.url)

        #Template
        if type(get_response) == Template:
            pass #render template

        #Error
        if type(get_response) == Error:
            self.error(get_response.code)

#Response result type
class Redirect(object):
    def __init__(self, url):
        self.url = url

class Template(object):
    def __init__(self, file, data):
        self.file = file
        self.data = data

class Error(object):
    def __init__(self, code):
        self.code = code

#Decorators
def authenticated(f):

    def wrapper(self, *args, **kwargs):
        user = self.users.get_current_user()

        if not user:
            #no user found, redirect to login
            return Redirect(self.users.create_login_url(self.request.uri))

        return f(self, *args, **kwargs)

    return wrapper

def administrator(f):

    def wrapper(self, *args, **kargs):
        user = self.users.get_current_user()

        if not user:
            #no user found, redirect to login
            return Redirect(self.create_login_url(self.request.uri))

        if not self.users.is_current_user_admin():
            #user is logged in but not an admin
            return Error(403)

        return f(self, *args, **kargs)

    return wrapper

#RequestHandlers
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

    def http_get(self):
        login_url = self.users.create_login_url('/')
        return Redirect(login_url)

class News(Controller):
    def http_get(self, word):
        return word

class UserZone(Controller):
    @authenticated
    def http_get(self):
        return self.users.get_current_user().nickname()

#URLS
def application():
    return webapp.WSGIApplication([ ( '/', Home ),
                                    ( '/contact', Contact ),
                                    ( '/about_us', AboutUs ),
                                    ( '/login', Login ),
                                    ( '/news/([-\w]+)', News ),
                                    ( '/userzone', UserZone ),
                                  ], debug=True)

def main():
    run_wsgi_app(application())

if __name__ == '__main__':
    main()
