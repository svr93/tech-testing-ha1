# coding: utf

import mock
from unittest import TestCase
from source import lib

class TestGetRedirectHistory(TestCase):
    def test_redirect_history_url(self):
        url = 'https://www.odnoklassniki.ru/'
        timeout = 10
        with mock.patch('source.lib.prepare_url', mock.Mock(return_value=url)):
            history_types, history_urls, counters = lib.get_redirect_history(url, timeout)

        self.assertEquals([], history_types)
        self.assertEquals([url], history_urls)
        self.assertEquals([], counters)

    def test_get_url_returned_none(self):
        url = 'http://url.ru'
        timeout = 30
        with mock.patch('source.lib.prepare_url', mock.Mock(return_value=url)):
            with mock.patch('source.lib.get_url', mock.Mock(return_value=[None, None, None])):
                history_types, history_urls, counters = lib.get_redirect_history(url, timeout)

        self.assertEquals([], history_types)
        self.assertEquals([url], history_urls)
        self.assertEquals([], counters)

    def test_get_redirect_history(self):
        url = 'http://url.ru'
        timeout = 30
        redirect_url = 'http://redirect-url.ru'
        redirect_type = 'redirect_type'
        counters = 'counters'
        with mock.patch('source.lib.prepare_url', mock.Mock(return_value=url)):
            with mock.patch('source.lib.get_url', mock.Mock(return_value=[redirect_url, redirect_type, 'content'])):
                with mock.patch('source.lib.get_counters', mock.Mock(return_value=counters)):
                    history_types, history_urls, return_counters = lib.get_redirect_history(url, timeout)

        self.assertEquals([redirect_type, redirect_type], history_types)
        self.assertEquals([url, redirect_url, redirect_url], history_urls)
        self.assertEquals(counters, return_counters)

    def test_get_url_returned_error_redirect_type(self):
        url = 'http://url.ru'
        timeout = 30
        redirect_url = 'http://redirect-url.ru'
        redirect_type_error = 'ERROR'
        counters = 'counters'
        with mock.patch('source.lib.prepare_url', mock.Mock(return_value=url)):
            with mock.patch('source.lib.get_url', mock.Mock(return_value=[redirect_url, redirect_type_error, 'content'])):
                with mock.patch('source.lib.get_counters', mock.Mock(return_value=counters)):
                    history_types, history_urls, return_counters = lib.get_redirect_history(url, timeout)

        self.assertEquals([redirect_type_error], history_types)
        self.assertEquals([url, redirect_url], history_urls)
        self.assertEquals(counters, return_counters)

