# coding: utf

from unittest import TestCase
import mock
from source.lib import worker

class TestGetRedirectHistoryFromTask(TestCase):
    def test_get_redirect_history_returned_error_and_recheck_is_false(self):
        url = '/test/url'
        url_id = 1
        suspicious = 'suspicious'
        recheck = False
        timeout = 10
        redirect_history = [['ERROR'], [], []]
        task = mock.Mock()
        task.data = {
            'url': url,
            'recheck': recheck,
            'url_id': url_id,
            'suspicious': suspicious
        }
        excepted_data = {
            'url': url,
            'recheck': True,
            'url_id': url_id,
            'suspicious': suspicious
        }
        with mock.patch('source.lib.worker.get_redirect_history', mock.Mock(return_value=redirect_history)):
            result = worker.get_redirect_history_from_task(task, timeout)
        self.assertEqual((True, excepted_data), result)

    def test_get_redirect_history_return_valid_value_without_suspicious(self):
        url = '/test/url'
        url_id = 1
        recheck = True
        timeout = 10
        redirect_history = [['ERROR'], [], []]
        task = mock.Mock()
        task.data = {
            'url': url,
            'recheck': recheck,
            'url_id': url_id,
        }
        excepted_data = {
            'url_id': url_id,
            'result': redirect_history,
            'check_type': 'normal',
        }

        with mock.patch('source.lib.worker.get_redirect_history', mock.Mock(return_value=redirect_history)):
            result = worker.get_redirect_history_from_task(task, timeout)
        self.assertEqual((False, excepted_data), result)

    def test_get_redirect_history_return_valid_value_with_suspicious(self):
        url = '/test/url'
        url_id = 1
        suspicious = 'suspicious'
        recheck = True
        timeout = 10
        redirect_history = [['ERROR'], [], []]
        task = mock.Mock()
        task.data = {
            'url': url,
            'recheck': recheck,
            'url_id': url_id,
            'suspicious': suspicious,
        }
        excepted_data = {
            'url_id': url_id,
            'result': redirect_history,
            'suspicious': suspicious,
            'check_type': 'normal',
        }
        with mock.patch('source.lib.worker.get_redirect_history', mock.Mock(return_value=redirect_history)):
            result = worker.get_redirect_history_from_task(task, timeout)
        self.assertEqual((False, excepted_data), result)
