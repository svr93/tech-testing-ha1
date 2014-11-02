# coding: utf

from unittest import TestCase
from source import lib

class TestCheckMeta(TestCase):
    def test_check_meta(self):
        meta_url = 'test.url'
        url = 'http://test/'
        content = """
				<!DOCTYPE html>
                <html>
                <head>
                    <meta http-equiv="refresh" content="5; url=%s">
                </head>
            </html>""" % meta_url
        self.assertEqual(lib.check_for_meta(content, url), url+meta_url)
