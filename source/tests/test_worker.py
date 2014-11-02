# coding: utf

from unittest import TestCase
import mock
from source.lib import worker

class TestWorker(TestCase):
    def test_parent_proc_path_doesnt_exist(self):
        tube = mock.MagicMock()
        parent_pid = 1

        with mock.patch('source.lib.worker.get_tube', mock.Mock(return_value=tube)):
            with mock.patch('os.path.exists', mock.Mock(return_value=False)):
                with mock.patch('source.lib.worker.logger', mock.Mock()):
                    worker.worker(mock.Mock(), parent_pid)
        self.assertEqual(0, tube.take.call_count)

    def test_input_tube_take_returned_none(self):
        tube = mock.MagicMock()
        tube.take = mock.Mock(return_value=None)
        parent_pid = 1

        with mock.patch('source.lib.worker.get_tube', mock.Mock(return_value=tube)):
            with mock.patch('os.path.exists', mock.Mock(side_effect=[True, False])):
                with mock.patch('source.lib.worker.get_redirect_history_from_task', mock.Mock()) as get_history_mock:
                    worker.worker(mock.Mock(), parent_pid)
        self.assertEqual(0, get_history_mock.call_count)

    def test_get_history_returned_none(self):
        task = mock.MagicMock()
        tube = mock.MagicMock()
        tube.take = mock.Mock(return_value=task)
        tube.put = mock.Mock()
        parent_pid = 1
        with mock.patch('source.lib.worker.get_tube', mock.Mock(return_value=tube)):
            with mock.patch('os.path.exists', mock.Mock(side_effect=[True, False])):
                with mock.patch('source.lib.worker.get_redirect_history_from_task', mock.Mock(return_value=None)):
                    worker.worker(mock.Mock(), parent_pid)
        self.assertEqual(0, tube.put.call_count)

    def test_get_history_returned_is_input(self):
        task = mock.MagicMock()
        tube = mock.MagicMock()
        tube.take = mock.Mock(return_value=task)
        tube.put = mock.Mock()
        parent_pid = 1
        result = (True, mock.Mock())
        with mock.patch('source.lib.worker.get_tube', mock.Mock(return_value=tube)):
            with mock.patch('os.path.exists', mock.Mock(side_effect=[True, False])):
                with mock.patch('source.lib.worker.get_redirect_history_from_task', mock.Mock(return_value=result)):
                    worker.worker(mock.Mock(), parent_pid)
        self.assertEqual(1, tube.put.call_count)

    def test_get_history_returned_is_output(self):
        task = mock.MagicMock()
        tube = mock.MagicMock()
        tube.take = mock.Mock(return_value=task)
        tube.put = mock.Mock()
        parent_pid = 1
        result = (False, mock.Mock())
        with mock.patch('source.lib.worker.get_tube', mock.Mock(return_value=tube)):
            with mock.patch('os.path.exists', mock.Mock(side_effect=[True, False])):
                with mock.patch('source.lib.worker.get_redirect_history_from_task', mock.Mock(return_value=result)):
                    worker.worker(mock.Mock(), parent_pid)
        self.assertEqual(1, tube.put.call_count)

    def test_task_ack_raised_exception(self):
        task = mock.MagicMock()
        task.ack = mock.Mock()
        tube = mock.MagicMock()
        tube.take = mock.Mock(return_value=task)
        tube.put = mock.Mock()
        parent_pid = 1
        result = (False, mock.Mock())
        with mock.patch('source.lib.worker.get_tube', mock.Mock(return_value=tube)):
            with mock.patch('os.path.exists', mock.Mock(side_effect=[True, False])):
                with mock.patch('source.lib.worker.get_redirect_history_from_task', mock.Mock(return_value=result)):
                    with mock.patch('source.lib.worker.logger', mock.Mock()) as logger_mock:
                        worker.worker(mock.Mock(), parent_pid)
        self.assertEqual(0, logger_mock.exception.call_count)
