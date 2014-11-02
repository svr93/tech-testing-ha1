# coding: utf

from unittest import TestCase
import mock
from source.lib import utils

class TestDaemonize(TestCase):
    def test_daemonize_raised_exception_when_os_fork_raised_exception_first_time(self):
        exception = OSError("")
        with mock.patch('os.fork', mock.Mock(side_effect=exception)):
            self.assertRaises(Exception, utils.daemonize)

    def test_os_fork_called_two_times_when_os_fork_returned_zero_first_time(self):
        pid = 0
        with mock.patch('os.fork', mock.Mock(return_value=pid)) as os_fork_mock:
            with mock.patch('os.setsid'):
                utils.daemonize()
        self.assertEqual(2, os_fork_mock.call_count)

    def test_os_fork_called_once_when_os_fork_return_valid_pid_first_time(self):
        pid = 1
        with mock.patch('os.fork', mock.Mock(return_value=pid)) as os_fork_mock:
            with mock.patch('os._exit'):
                utils.daemonize()
        os_fork_mock.assert_calls_once_with()

    def test_os_setsid_called_when_os_fork_returned_zero_first_time(self):
        pid = 0
        with mock.patch('os.fork', mock.Mock(return_value=pid)):
            with mock.patch('os.setsid') as os_setsid_mock:
                utils.daemonize()
        os_setsid_mock.assert_calls_once_with()
        
    def test_os_exit_called_once_when_os_fork_returned_valid_pid_first_time(self):
        pid = 1
        with mock.patch('os.fork', mock.Mock(return_value=pid)):
            with mock.patch('os._exit') as os_exit_mock:
                utils.daemonize()
        os_exit_mock.assert_called_once_with(0)

    def test_os_exit_didnt_call_when_os_fork_returned_zero_both_times(self):
        pid = 0
        with mock.patch('os.fork', mock.Mock(return_value=pid)):
            with mock.patch('os.setsid'):
                with mock.patch('os._exit') as os_exit_mock:
                    utils.daemonize()
        self.assertEqual(0, os_exit_mock.call_count)

    def test_os_exit_called_once_when_os_fork_returned_zero_first_time_and_os_fork_return_valid_pid_second_time(self):
        invalid_pid = 0
        valid_pid = 1
        with mock.patch('os.fork', mock.Mock(side_effect=[invalid_pid, valid_pid])):
            with mock.patch('os.setsid'):
                with mock.patch('os._exit') as os_exit_mock:
                    utils.daemonize()
        os_exit_mock.assert_called_once_with(0)
