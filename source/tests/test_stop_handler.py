# coding: utf

import mock
from unittest import TestCase
from source import notification_pusher

class TestStopHandler(TestCase):
    def test_run_application_becomes_false(self):
        signim = 4
        temp = notification_pusher.run_application
        notification_pusher.run_application = True
        thread = mock.Mock()
        thread.name = 'thread_name'
        with mock.patch('source.notification_pusher.logger', mock.Mock()):
            with mock.patch('source.notification_pusher.current_thread', mock.Mock(return_value=thread)):
                notification_pusher.stop_handler(signim)

        self.assertFalse(notification_pusher.run_application)
        notification_pusher.run_applcation = temp

    def test_exit_code_is_valid(self):
        signim = 4
        signal_exit_code_offset = 128
        temp = notification_pusher.exit_code
        notification_pusher.run_application = True
        thread = mock.Mock()
        thread.name = 'thread_name'
        with mock.patch('source.notification_pusher.logger', mock.Mock()):
            with mock.patch('source.notification_pusher.current_thread', mock.Mock(return_value=thread)):
                notification_pusher.stop_handler(signim)

        self.assertEqual(signal_exit_code_offset+signim, notification_pusher.exit_code)
        notification_pusher.exit_code = temp
