import unittest
from main import Home, Contact, AboutUs, Login, News, Authenticated, Redirect, authenticated, auth
from mock import Mock

class TestApplication(unittest.TestCase):
    def test_home(self):
        home = Home()
        assert home.http_get() == 'Hello world!'

    def test_contact(self):
        contact = Contact()
        result = contact.http_get()

        assert result.url == '/'

    def test_about_us(self):
        about_us = AboutUs()
        result = about_us.http_get()

        assert result.file == '/about_us.html'
        assert result.data == 'We are the robots'

    def test_login(self):
        users = Mock()
        users.create_login_url.return_value = '/login_url_to_somewhere'
        login = Login(users)
        result = login.http_get()

        assert result.url == '/login_url_to_somewhere'

    def test_news(self):
        news = News()
        assert news.http_get('the bird is the word') == 'the bird is the word'

class TestDecorators(unittest.TestCase):
    def test_Authenticated_no_user(self):
        #Arrange
        f = Mock()
        this = Mock()
        this.users.get_current_user.return_value = None
        this.users.create_login_url.return_value = '/login'

        #Act
        decorator = authenticated(f)
        result = decorator(this)

        #Assert
        assert not f.called
        assert this.users.get_current_user.called
        assert type(result) == Redirect

    def test_Authenticated_logged_in(self):
        #Arrange
        f = Mock()
        this = Mock()
        this.users.get_current_user.return_value = True

        #Act
        decorator = authenticated(f)
        decorator(this)

        #Assert
        assert this.users.get_current_user.called
        assert f.called
