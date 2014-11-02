# coding: utf

import mock
from unittest import TestCase
from source import lib
from source.lib import REDIRECT_HTTP

class TestGetUrl(TestCase):
    def test_without_redirect(self):
        url = 'http://url.ru'
        timeout = 10
        content = 'content'
        new_redirect_url = 'http://odnoklassniki.ru/redirect-url/st.redirect'
        with mock.patch('source.lib.make_pycurl_request', mock.Mock(return_value=[content, new_redirect_url])):
            self.assertEquals((None, None, content), lib.get_url(url, timeout))

    def test_redirect(self):
        url = 'http://url.ru'
        timeout = 30
        content = 'content'
        new_redirect_url = 'http://redirect-url.ru'
        with mock.patch('source.lib.make_pycurl_request', mock.Mock(return_value=[content, new_redirect_url])):
            self.assertEquals((new_redirect_url, REDIRECT_HTTP, content), lib.get_url(url, timeout))

    def test_redirect_market(self):
        url = 'http://url.ru'
        timeout = 30
        content = 'content'
        new_redirect_url = 'market://url.ru'
        new_redirect_url_without_market = 'http://play.google.com/store/apps/url.ru'
        with mock.patch('source.lib.make_pycurl_request', mock.Mock(return_value=[content, new_redirect_url])):
            self.assertEquals((new_redirect_url_without_market, REDIRECT_HTTP, content), lib.get_url(url, timeout))

    def test_make_pycurl_request_raised_exception(self):
        url = 'http://url.ru'
        timeout = 30
        with mock.patch('source.lib.make_pycurl_request', mock.Mock(side_effect=ValueError)):
            self.assertEquals((url, 'ERROR', None), lib.get_url(url, timeout))

    def test_without_redirect_url(self):
        url = 'http://url.ru'
        timeout = 30
        content = 'content'
        with mock.patch('source.lib.make_pycurl_request', mock.Mock(return_value=[content, None])):
            with mock.patch('source.lib.check_for_meta', mock.Mock(return_value=None)):
                self.assertEquals((None, None, content), lib.get_url(url, timeout))
