import requests
import unittest
from sqlalchemy import create_engine

class DockerComposeTestCase(unittest.TestCase):

    def test_post(self):
        expression = {'expression': "3+2"}
        result = requests.post('http://localhost:5000/add', data=expression)
        self.assertEqual(result.status_code, 200)
        
    def test_bad_post(self):
        incorrect = {"expression": "Hello xDD"}
        result = requests.post('http://localhost:5000/add', data=incorrect)
        self.assertNotEqual(result.status_code, 200)

    def test_db(self):
        expression = {'expression': "3+2"}
        result = requests.post('http://localhost:5000/add', data=expression)
        engine = create_engine('postgresql://cs162_user:cs162_password@localhost:5432/cs162', echo = True)

        connection = engine.connect()
        results = connection.execute("SELECT * FROM Expression WHERE text='3+2'").fetchall()

        self.assertNotEqual(len(results), 0)

    def test_correct_result(self):
        expression = {'expression': "3+2"}
        result = requests.post('http://localhost:5000/add', data=expression)
        engine = create_engine('postgresql://cs162_user:cs162_password@localhost:5432/cs162', echo = True)

        connection = engine.connect()
        results = connection.execute("SELECT value FROM Expression WHERE text='3+2'").first()

        self.assertEqual(results, 5)

    def test_error_db(self):
        incorrect = {"expression": "Hello xDD"}
        result = requests.post('http://localhost:5000/add', data=incorrect)
        engine = create_engine('postgresql://cs162_user:cs162_password@localhost:5432/cs162', echo = True)

        connection = engine.connect()
        results = connection.execute("SELECT * FROM Expression WHERE text='Hello xDD'").fetchall()

        self.assertNotEqual(len(results), 0)



if __name__ == '__main__':
    unittest.main()