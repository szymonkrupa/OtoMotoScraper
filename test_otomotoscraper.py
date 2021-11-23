import requests
import random
from bs4 import BeautifulSoup
import unittest

from otomotoscraper import max_page, urls, price, equipment

class Test(unittest.TestCase):
    bs = None
    def setUpClass():
        car_brand_list = ['Audi', 'BMW', 'Renault', 'Toyota', 'Ford', 'Volvo']
        url = f'https://www.otomoto.pl/osobowe/uzywane/{random.choice(car_brand_list)}'
        Test.req = requests.get(url)
        Test.bs = BeautifulSoup(Test.req.content, 'html.parser')
    def test_response(self):
        # Respone status_code check
        self.assertEqual(Test.req.status_code, 200, "Status code different than 200")
    def test_pagemax(self):
        # max_page function test
        pageMax = max_page(Test.bs)
        self.assertTrue(type(pageMax) == int, "Not integer")
    def test_urls(self):
        # urls function test
        links = urls(Test.bs)
        self.assertIsNotNone(links, "Links not found")
    def test_offers(self):
        # price and equipment function test
        links = urls(Test.bs)
        offer_req = requests.get(links[-2])
        soup = BeautifulSoup(offer_req.content, 'html.parser')
        priceDict = price(soup)
        eqDict = equipment(soup)
        self.assertTrue(type(priceDict['price']) == float, "Not float")
        self.assertTrue(len(priceDict['currency']) == 3, "Different than 3 letters")
        self.assertTrue(type(eqDict['equipment']) == list, "It's None")
    

if __name__ == '__main__':
   unittest.main()