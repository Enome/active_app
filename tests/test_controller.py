import unittest
from main import Home

class TestController(unittest.TestCase):
    def test_output(self):
        home = Home()
        assert home.http_get() == 'Hello world!'
