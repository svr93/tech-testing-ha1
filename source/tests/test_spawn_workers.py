# coding: utf

import multiprocessing
from unittest import TestCase
import mock
from source.lib import utils

class TestSpawnWorkers(TestCase):
    def test_processes_created(self):
        num = 10
        with mock.patch('multiprocessing.Process.__new__', mock.Mock()) as multiprocessing_Process_mock:
            utils.spawn_workers(num, mock.Mock(), mock.Mock(), mock.Mock())
        self.assertEqual(num, multiprocessing_Process_mock.call_count)
