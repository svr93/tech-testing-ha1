# coding: utf

import mock
from unittest import TestCase
from source import notification_pusher

class TestInstallSignalHandlers(TestCase):
    def test_signals_installed(self):
        with mock.patch('source.notification_pusher.gevent.signal', mock.Mock()) as signal_mock:
            notification_pusher.install_signal_handlers()
        self.assertEqual(4, signal_mock.call_count)
