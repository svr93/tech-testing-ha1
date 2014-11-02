# coding: utf

import argparse
from unittest import TestCase
import mock
from source import redirect_checker, notification_pusher

class TestMain(TestCase):
    def test_daemonize_called_if_daemon_flag_set(self):
        argv = ['description', '--daemon', '--config', '']
        with mock.patch('source.redirect_checker.daemonize', mock.Mock()) as daemonize_mock:
            with mock.patch('source.redirect_checker.create_pidfile', mock.Mock()):
                with mock.patch('source.redirect_checker._load_config', mock.Mock(return_value=mock.Mock())):
                    with mock.patch('source.redirect_checker.dictConfig', mock.Mock()):
                        with mock.patch('source.redirect_checker.main_loop', mock.Mock()):
                            redirect_checker.main(argv)
        daemonize_mock.assert_called_once_with()

    def test_pidfile_created_if_pid_flag_set(self):
        pid = 1
        argv = ['description', '--pid', str(pid), '--config', '']
        with mock.patch('source.redirect_checker.daemonize', mock.Mock()):
            with mock.patch('source.redirect_checker.create_pidfile', mock.Mock()) as create_pidfile_mock:
                with mock.patch('source.redirect_checker._load_config', mock.Mock(return_value=mock.Mock())):
                    with mock.patch('source.redirect_checker.dictConfig', mock.Mock()):
                        with mock.patch('source.redirect_checker.main_loop', mock.Mock()):
                            redirect_checker.main(argv)
        create_pidfile_mock.assert_called_once_with(str(pid))

    def test_returned_valid_exit_code(self):
        config = mock.Mock()
        config.EXIT_CODE = 2
        argv = ['description', '--config', '']
        with mock.patch('source.redirect_checker.daemonize', mock.Mock()):
            with mock.patch('source.redirect_checker.create_pidfile', mock.Mock()):
                with mock.patch('source.redirect_checker._load_config', mock.Mock(return_value=config)):
                    with mock.patch('source.redirect_checker.dictConfig', mock.Mock()):
                        with mock.patch('source.redirect_checker.main_loop', mock.Mock()):
                            EXIT_CODE = redirect_checker.main(argv)
        self.assertEqual(EXIT_CODE, config.EXIT_CODE)


    def test_notification_pusher_daemonize_called_if_daemon_flag_set(self):
        temp = notification_pusher.run_application
        notification_pusher.run_application = False
        argv = ['description', '--daemon', '--config', '']
        thread = mock.Mock()
        thread.name = mock.Mock()

        def _break_notification_pusher(*args, **kwargs):
            notification_pusher.run_application = False

        with mock.patch('source.notification_pusher.daemonize', mock.Mock()) as daemonize_mock:
            with mock.patch('source.notification_pusher.create_pidfile', mock.Mock()):
                with mock.patch('source.notification_pusher._load_config', mock.Mock(return_value=mock.Mock())):
                    with mock.patch('source.notification_pusher.patch_all', mock.Mock()):
                        with mock.patch('source.notification_pusher.dictConfig', mock.Mock()):
                            with mock.patch('source.notification_pusher.install_signal_handlers', mock.Mock()):
                                with mock.patch('source.notification_pusher.current_thread', mock.Mock(return_value=thread)):
                                    notification_pusher.main(argv)
        daemonize_mock.assert_called_once_with()
        notification_pusher.run_application = temp

    def test_notification_pusher_pidfile_created_if_pid_flag_set(self):
        temp = notification_pusher.run_application
        notification_pusher.run_application = False
        pid = 1
        argv = ['description', '--pid', str(pid), '--config', '']
        thread = mock.Mock()
        thread.name = mock.Mock()

        def _break_notification_pusher(*args, **kwargs):
            notification_pusher.run_application = False

        with mock.patch('source.notification_pusher.daemonize', mock.Mock()):
            with mock.patch('source.notification_pusher.create_pidfile', mock.Mock()) as pidfile_created_mock:
                with mock.patch('source.notification_pusher._load_config', mock.Mock(return_value=mock.Mock())):
                    with mock.patch('source.notification_pusher.patch_all', mock.Mock()):
                        with mock.patch('source.notification_pusher.dictConfig', mock.Mock()):
                            with mock.patch('source.notification_pusher.install_signal_handlers', mock.Mock()):
                                with mock.patch('source.notification_pusher.current_thread', mock.Mock(return_value=thread)):
                                    notification_pusher.main(argv)
        pidfile_created_mock.assert_called_once_with(str(pid))
        notification_pusher.run_application = temp

    def test_main_loop_raised_exception(self):
        temp = notification_pusher.run_application
        notification_pusher.run_application = True
        argv = ['description', '--config', '']
        thread = mock.Mock()
        thread.name = mock.Mock()

        def _break_notification_pusher(*args, **kwargs):
            notification_pusher.run_application = False

        with mock.patch('source.notification_pusher.daemonize', mock.Mock()):
            with mock.patch('source.notification_pusher.create_pidfile', mock.Mock()):
                with mock.patch('source.notification_pusher._load_config', mock.Mock(return_value=mock.Mock())):
                    with mock.patch('source.notification_pusher.patch_all', mock.Mock()):
                        with mock.patch('source.notification_pusher.dictConfig', mock.Mock()):
                            with mock.patch('source.notification_pusher.install_signal_handlers', mock.Mock()):
                                with mock.patch('source.notification_pusher.current_thread', mock.Mock(return_value=thread)):
                                    with mock.patch('source.notification_pusher.main_loop', mock.Mock(side_effect=Exception)):
                                        with mock.patch('source.notification_pusher.sleep', mock.Mock(side_effect=_break_notification_pusher)) as sleep_mock:
                                            notification_pusher.main(argv)
        sleep_mock.assert_called_once_with(mock.ANY)
        notification_pusher.run_application = temp

    def test_main_loop(self):
        temp = notification_pusher.run_application
        notification_pusher.run_application = True
        argv = ['description', '--config', '']
        thread = mock.Mock()
        thread.name = mock.Mock()

        def _break_notification_pusher(*args, **kwargs):
            notification_pusher.run_application = False

        with mock.patch('source.notification_pusher.daemonize', mock.Mock()):
            with mock.patch('source.notification_pusher.create_pidfile', mock.Mock()):
                with mock.patch('source.notification_pusher._load_config', mock.Mock(return_value=mock.Mock())):
                    with mock.patch('source.notification_pusher.patch_all', mock.Mock()):
                        with mock.patch('source.notification_pusher.dictConfig', mock.Mock()):
                            with mock.patch('source.notification_pusher.install_signal_handlers', mock.Mock()):
                                with mock.patch('source.notification_pusher.current_thread', mock.Mock(return_value=thread)):
                                    with mock.patch('source.notification_pusher.main_loop', mock.Mock(side_effect=_break_notification_pusher)) as main_loop_mock:
                                        with mock.patch('source.notification_pusher.sleep', mock.Mock(side_effect=_break_notification_pusher)):
                                            notification_pusher.main(argv)
        main_loop_mock.assert_called_once_with(mock.ANY)
        notification_pusher.run_application = temp
