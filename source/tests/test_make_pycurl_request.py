# coding: utf

import mock
from unittest import TestCase
from source import lib

class TestMakePycurlRequest(TestCase):
    def test_redirect_url_is_none(self):
        url = 'http://url.ru'
        timeout = 30
        content = 'content'
        buff = mock.Mock()
        buff.getvalue = mock.Mock(return_value=content)
        curl = mock.Mock()
        curl.setopt = mock.Mock()
        curl.perform = mock.Mock()
        curl.getinfo = mock.Mock(return_value=None)
        with mock.patch('source.lib.StringIO', mock.Mock(return_value=buff)):
            with mock.patch('pycurl.Curl', mock.Mock(return_value=curl)):
                self.assertEquals((content, None), lib.make_pycurl_request(url, timeout))

    def test_with_useragent(self):
        url = 'http://url.ru'
        timeout = 30
        content = 'content'
        redirect_url = 'http://redirect-url.ru'
        useragent = 'useragent'
        buff = mock.MagicMock()
        buff.getvalue = mock.Mock(return_value=content)
        curl = mock.MagicMock()
        curl.setopt = mock.Mock()
        curl.perform = mock.Mock()
        curl.getinfo = mock.Mock(return_value=redirect_url)
        with mock.patch('source.lib.StringIO', mock.Mock(return_value=buff)):
            with mock.patch('pycurl.Curl', mock.Mock(return_value=curl)):
                self.assertEquals((content, redirect_url), lib.make_pycurl_request(url, timeout, useragent))
