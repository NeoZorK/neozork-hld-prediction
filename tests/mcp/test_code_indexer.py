import unittest
import logging
from mcp_server import CodeIndexer

class DummyLogger(logging.LoggerAdapter):
    def __init__(self):
        super().__init__(logging.getLogger('test'), {})

class TestCodeIndexer(unittest.TestCase):
    def setUp(self):
        self.logger = DummyLogger()
        self.indexer = CodeIndexer(self.logger)

    def test_index_function_and_class(self):
        content = '''
"""
Sample module
"""

def foo():
    """doc foo"""
    pass

class Bar:
    """doc Bar"""
    def baz(self):
        """doc baz"""
        return 1
'''
        self.indexer.index_python_file('test.py', content)
        # functions
        self.assertIn('foo', self.indexer.code_index['functions'])
        # classes
        self.assertIn('Bar', self.indexer.code_index['classes'])
        # method
        self.assertIn('Bar.baz', self.indexer.code_index['functions'])
        # docstrings
        self.assertEqual(self.indexer.code_index['docstrings'][('foo','function')], 'doc foo')
        self.assertEqual(self.indexer.code_index['docstrings'][('Bar','class')], 'doc Bar')
        self.assertEqual(self.indexer.code_index['docstrings'][('Bar.baz','method')], 'doc baz')

if __name__ == '__main__':
    unittest.main()

