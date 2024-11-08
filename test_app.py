# test_app.py
import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        # Sets up a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_world(self):
        # Sends a GET request to the '/' route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')
    
    def test_user(self):
        # Sends a GET request to the '/user' route
        response = self.app.get('/user')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Username')

if __name__ == '__main__':
    unittest.main()
