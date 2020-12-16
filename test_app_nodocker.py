#!/usr/bin/python
import unittest
import os
import app


class FlaskTests(unittest.TestCase):
    def setUp(self):
        os.environ['NO_PROXY'] = '0.0.0.0'
        app.app.testing = True
        self.app = app.app.test_client()
        pass

    def tearDown(self):
        pass

    def test_index(self):
        responce = self.app.get('/')
        self.assertEqual(responce.status_code, 200)

    def test_predict_page(self):
        responce = self.app.get('http://localhost:5000/predict')
        self.assertEqual(responce.status_code, 200)

    def test_get_tweets(self):
        params = {
            'message_user': "This is America",
        }

        responce = self.app.post('http://localhost:5000/predict', data=params)
        self.assertEqual(responce.status_code, 200)


if __name__ == '__main__':
    unittest.main()
