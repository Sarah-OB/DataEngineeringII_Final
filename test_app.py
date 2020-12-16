#!/usr/bin/python
import unittest
import os
import requests


class FlaskTests(unittest.TestCase):
    def setUp(self):
        os.environ['NO_PROXY'] = '0.0.0.0'
        pass

    def tearDown(self):
        pass

    def test_index(self):
        responce = requests.get('http://localhost:5000')
        self.assertEqual(responce.status_code, 200)

    def test_predict_page(self):
        responce = requests.get('http://localhost:5000/predict')
        self.assertEqual(responce.status_code, 200)

    def test_get_tweets(self):
        params = {
            'message_user': "This is America",
        }

        responce = requests.post('http://localhost:5000/predict', data=params)
        self.assertEqual(responce.status_code, 200)


if __name__ == '__main__':
    unittest.main()
