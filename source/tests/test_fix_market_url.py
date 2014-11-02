# coding: utf

from unittest import TestCase
from source import lib

class TestFixMarketUrl(TestCase):
    def test_url_fixed(self):
        url = 'url'
        market_url = "market://"
        web_url = "http://play.google.com/store/apps/"
        self.assertEqual(lib.fix_market_url(market_url+url), web_url+url)
