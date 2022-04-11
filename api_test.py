from doctest import testfile
import unittest
from itsdangerous import json
import requests

class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"
    data1= {
        "poolId":223,
        "poolValues":[3, 6, 7, 8, 8, 10, 13, 15, 16, 20]
    }

    data2= {
        "poolId":223,
        "percentile":50
    }

    data3= {
        "poolId":22333,
        "percentile":50
    }

    expect_result = {
    "quantile": 9,
    "total": 10
    }

    def test_1_point_1(self):
        resp = requests.post(self.URL+'/post-1', json = self.data1)
        self.assertEqual(resp.status_code, 200)
        print("test 1 point 1 complete")

    def test_1_point_2(self):
        resp = requests.post(self.URL + '/post-2', json = self.data2)
        self.assertEqual(resp.status_code, 200)
        print("test 1 point 2 complete")
    
    def test_2_point_2(self):
        resp = requests.post(self.URL + 'post-2', json = self.data3)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), self.expect_result)
        print("test 2 point 2 complete")

if __name__ == "__main__":       
    unittest.main()