# coding: utf

from unittest import TestCase
import mock
import os
from source import redirect_checker, notification_pusher
from source.lib.utils import Config

class TestMainLoop(TestCase):
    def test_active_children_terminated_if_network_status_is_false(self):
        parent_pid = 1
        network_status = False

        config = mock.MagicMock()
        config.WORKER_POOL_SIZE = 10
        config.SLEEP = 1

        active_children_count = 6
        active_child = mock.MagicMock()
        active_child.terminate = mock.Mock()
        active_children = [active_child] * active_children_count

        def break_run(*args, **kwargs):
            redirect_checker.is_running = False

        with mock.patch('source.redirect_checker.active_children', mock.Mock(return_value=active_children)):
            with mock.patch('source.redirect_checker.check_network_status', mock.Mock(return_value=network_status)):
                with mock.patch('os.getpid', mock.Mock(return_value=parent_pid)):
                    with mock.patch('source.redirect_checker.sleep', mock.Mock(side_effect=break_run)):
                        redirect_checker.main_loop(config)
        for c in active_children:
            c.terminate.assert_call_once()
        redirect_checker.is_running = True

    def test_spawn_worker_called_if_network_status_is_true(self):
        parent_pid = 1
        network_status = True
        active_children_count = 6
        active_child = mock.MagicMock()
        active_child.terminate = mock.Mock()
        active_children = [active_child] * active_children_count
        config = mock.MagicMock()
        config.WORKER_POOL_SIZE = 10
        config.SLEEP = 1
        # spawn_workers_mock = mock.Mock()

        def break_run(*args, **kwargs):
            redirect_checker.is_running = False

        with mock.patch('source.redirect_checker.check_network_status', mock.Mock(return_value=network_status)):
            with mock.patch('os.getpid', mock.Mock(return_value=parent_pid)):
                with mock.patch('source.redirect_checker.active_children', mock.Mock(return_value=active_children)):
                    with mock.patch('source.redirect_checker.spawn_workers', mock.Mock()) as spawn_workers_mock:
                        with mock.patch('source.redirect_checker.sleep', mock.Mock(side_effect=break_run)):
                            redirect_checker.main_loop(config)
        spawn_workers_mock.assert_called_once_with(num=config.WORKER_POOL_SIZE - active_children_count, target=mock.ANY,
                                                   args=mock.ANY, parent_pid=parent_pid)
        redirect_checker.is_running = True

    def test_spawn_worker_called_if_network_status_is_true_and_active_children_count_greater_than_worker_pool_size(
            self):
        parent_pid = 1
        network_status = True
        active_children_count = 16
        active_child = mock.MagicMock()
        active_child.terminate = mock.Mock()
        active_children = [active_child] * active_children_count
        config = mock.MagicMock()
        config.WORKER_POOL_SIZE = 10
        config.SLEEP = 1
        # spawn_workers_mock = mock.Mock()

        def break_run(*args, **kwargs):
            redirect_checker.is_running = False

        with mock.patch('source.redirect_checker.check_network_status', mock.Mock(return_value=network_status)):
            with mock.patch('os.getpid', mock.Mock(return_value=parent_pid)):
                with mock.patch('source.redirect_checker.active_children', mock.Mock(return_value=active_children)):
                    with mock.patch('source.redirect_checker.spawn_workers', mock.Mock()) as spawn_workers_mock:
                        with mock.patch('source.redirect_checker.sleep', mock.Mock(side_effect=break_run)):
                            redirect_checker.main_loop(config)
        self.assertEqual(0, spawn_workers_mock.call_count)
        redirect_checker.is_running = True


    def test_task_is_none(self):
        temp = notification_pusher.run_application
        notification_pusher.run_application = True

        queue = mock.Mock()
        tube = mock.Mock()
        task = None
        tube.take = mock.Mock(return_value=task)
        queue.tube = mock.Mock(return_value=tube)
        free_workers_count = 4
        worker_pool = mock.Mock()
        worker_pool.free_count = mock.Mock(return_value=free_workers_count)
        processed_task_queue = mock.Mock()

        def _break_notification_pusher(*args, **kwargs):
            notification_pusher.run_application = False

        with mock.patch('source.notification_pusher.logger', mock.Mock()):
            with mock.patch('source.notification_pusher.tarantool_queue.Queue.__new__', mock.Mock(return_value=queue)):
                with mock.patch('source.notification_pusher.Pool.__new__', mock.Mock(return_value=worker_pool)):
                    with mock.patch('source.notification_pusher.gevent_queue.Queue.__new__',
                                    mock.Mock(return_value=processed_task_queue)):
                        with mock.patch('source.notification_pusher.done_with_processed_tasks', mock.Mock()):
                            with mock.patch('source.notification_pusher.sleep',
                                            mock.Mock(side_effect=_break_notification_pusher)):
                                with mock.patch('source.notification_pusher.Greenlet.__new__',
                                                mock.Mock()) as new_greenlet_mock:
                                    notification_pusher.main_loop(mock.Mock())
        self.assertEqual(0, new_greenlet_mock.call_count)
        notification_pusher.run_application = temp

    def test_task_is_not_none(self):
        temp = notification_pusher.run_application
        notification_pusher.run_application = True

        queue = mock.Mock()
        tube = mock.Mock()
        task = mock.Mock()
        tube.take = mock.Mock(return_value=task)
        queue.tube = mock.Mock(return_value=tube)
        free_workers_count = 1
        worker_pool = mock.Mock()
        worker_pool.free_count = mock.Mock(return_value=free_workers_count)
        worker_pool.add = mock.Mock()

        worker = mock.Mock()
        worker.start = mock.Mock()

        processed_task_queue = mock.Mock()


        def _break_notification_pusher(*args, **kwargs):
            notification_pusher.run_application = False

        with mock.patch('source.notification_pusher.logger', mock.Mock()):
            with mock.patch('source.notification_pusher.tarantool_queue.Queue.__new__', mock.Mock(return_value=queue)):
                with mock.patch('source.notification_pusher.Pool.__new__', mock.Mock(return_value=worker_pool)):
                    with mock.patch('source.notification_pusher.gevent_queue.Queue.__new__',
                                    mock.Mock(return_value=processed_task_queue)):
                        with mock.patch('source.notification_pusher.done_with_processed_tasks', mock.Mock()):
                            with mock.patch('source.notification_pusher.sleep',
                                            mock.Mock(side_effect=_break_notification_pusher)):
                                with mock.patch('source.notification_pusher.Greenlet.__new__',
                                                mock.Mock(return_value=worker)) as new_greenlet_mock:
                                    notification_pusher.main_loop(mock.Mock())
        self.assertEqual(1, new_greenlet_mock.call_count)
        worker_pool.add.assert_called_once_with(worker)
        worker.start.assert_called_once_with()
        notification_pusher.run_application = temp

