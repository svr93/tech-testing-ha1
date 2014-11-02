# coding: utf

from unittest import TestCase
import mock
from source.lib import utils

class TestLoadConfigFromPyfile(TestCase):
    def test_simple_configuration_file_with_one_key_loaded(self):
        path = '/test/file'
        configuration = {
            'KEY1': 'VAL1',
        }

        with mock.patch('source.lib.utils._execfile', mock.Mock(return_value=configuration)):
            result_config = utils.load_config_from_pyfile(path)

        configuration_config = utils.Config()
        configuration_config.KEY1 = configuration['KEY1']

        self.assertEqual(result_config.KEY1, result_config.KEY1)

    def test_complex_configuration_file_with_one_key_loaded(self):
        path = '/test/file'
        configuration = {
            'KEY1': {
                'KEY11': 'VAL11',
                'KEY12': 'VAL12',
            }
        }

        with mock.patch('source.lib.utils._execfile', mock.Mock(return_value=configuration)):
            result_config = utils.load_config_from_pyfile(path)

        configuration_config = utils.Config()
        configuration_config.KEY1 = configuration['KEY1']

        self.assertEqual(result_config.KEY1, result_config.KEY1)

    def test_valid_configuration_file_with_some_keys_loaded(self):
        path = '/test/file'
        configuration = {
            'KEY1': {
                'KEY11': 'VAL11',
                'KEY12': 'VAL12',
            },
            'KEY2': 'VAL2',
        }

        with mock.patch('source.lib.utils._execfile', mock.Mock(return_value=configuration)):
            result_config = utils.load_config_from_pyfile(path)

        configuration_config = utils.Config()
        configuration_config.KEY1 = configuration['KEY1']
        configuration_config.KEY2 = configuration['KEY2']

        self.assertEqual(result_config.KEY1, result_config.KEY1)
        self.assertEqual(result_config.KEY2, result_config.KEY2)

    def test_invalid_configuration_file_raises_exception(self):
        path = '/test/file'
        configuration = 'invalid configuration'

        with mock.patch('source.lib.utils._execfile', mock.Mock(return_value=configuration)):
            self.assertRaises(AttributeError, utils.load_config_from_pyfile, path)
