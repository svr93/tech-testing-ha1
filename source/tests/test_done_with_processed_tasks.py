# coding: utf

import mock
import tarantool
from unittest import TestCase
from gevent import queue as gevent_queue
from source import notification_pusher

class TestDoneWithProcessedTasks(TestCase):
    def test_task_queue_get_nowait_raised_exception(self):
        task_queue_size = 4
        task_queue = mock.Mock()
        task_queue.qsize = mock.Mock(return_value=task_queue_size)
        task_queue.get_nowait = mock.Mock(side_effect=gevent_queue.Empty)
        with mock.patch('source.notification_pusher.logger', mock.Mock()):
            notification_pusher.done_with_processed_tasks(task_queue)

        self.assertEqual(1, task_queue.get_nowait.call_count)

    def test_task_queue_get_nowait_didnt_raise_exception(self):
        action_name = 'method'
        task = mock.Mock()
        task.method = mock.Mock()
        task_action_name = (task, action_name)
        task_queue_size = 4
        task_queue = mock.Mock()
        task_queue.qsize = mock.Mock(return_value=task_queue_size)
        task_queue.get_nowait = mock.Mock(return_value=task_action_name)
        with mock.patch('source.notification_pusher.logger', mock.Mock()):
            notification_pusher.done_with_processed_tasks(task_queue)
        self.assertEqual(task_queue_size, task_queue.get_nowait.call_count)

    def test_task_has_no_method(self):
        action_name = 'method'
        task = mock.Mock()
        task.method = mock.Mock(side_effect=tarantool.DatabaseError)
        task_action_name = (task, action_name)
        task_queue_size = 1
        task_queue = mock.Mock()
        task_queue.qsize = mock.Mock(return_value=task_queue_size)
        task_queue.get_nowait = mock.Mock(return_value=task_action_name)

        with mock.patch('source.notification_pusher.logger', mock.Mock()):
            with mock.patch('source.notification_pusher.logger.exception', mock.Mock()) as logger_exception_mock:
                notification_pusher.done_with_processed_tasks(task_queue)
        self.assertEqual(task_queue_size, logger_exception_mock.call_count)
