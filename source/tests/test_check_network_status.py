# coding: utf

import socket
from unittest import TestCase
import urllib2
import mock
from source.lib import utils

class TestCheckNetworkStatus(TestCase):
    def test_valid_url(self):
        testurl = '/test/url'
        timeout = 5
        with mock.patch('urllib2.urlopen', mock.Mock()):
            self.assertTrue(utils.check_network_status(testurl, timeout))
            
    def test_value_error(self):
        testurl = '/test/url'
        timeout = 5
        with mock.patch('urllib2.urlopen', mock.Mock(side_effect=ValueError)):
            self.assertFalse(utils.check_network_status(testurl, timeout))

    def test_socket_error(self):
        testurl = '/test/url'
        timeout = 5
        with mock.patch('urllib2.urlopen', mock.Mock(side_effect=socket.error)):
            self.assertFalse(utils.check_network_status(testurl, timeout))
