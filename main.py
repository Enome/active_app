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

class Redirect(object):
    def __init__(self, url):
        self.url = url

class Template(object):
    def __init__(self, file, data):
        self.file = file
        self.data = data

#Decorators
def authenticated(f):

    def wrapper(self, *args, **kwargs):
        user = self.users.get_current_user()

        if not user:
            return Redirect(self.users.create_login_url(self.request.uri))

        return f(self, *args, **kwargs)

    return wrapper

#def authenticated(_users=None, _request=None):
#    def wrap(f):
#        def wrapped_f(*args):
#            users = _users or self.users
#            request = _request or self.request
#
#            user = users.users.get_current_user()
#            if not user:
#                return Redirect(self.users.create_login_url(self.request.uri))
#
#            f(*args)
#        return wrapped_f
#    return wrap
#
class Authenticated(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, _users=None, _request=None, *args):
        self.users = _users or self.f.users
        self.request = _request or self.f.request

        user = self.users.get_current_user()
        if not user:
            return Redirect(self.users.create_login_url(self.request.uri))

        self.f()

import functools
def auth(method, _users=None, _request=None):
    @functools.wraps(method) 
    def wrapper(self, *args, **kwargs):
        if _users:
            self.users = _users

        if _request:
            self.request = _request

        user = self.users.get_current_user()
        if not user:
            return Redirect(self.users.create_login_url(self.request.uri))

        return method(self, *args, **kwargs)
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
