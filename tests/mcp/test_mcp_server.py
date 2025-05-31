import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
import logging
from mcp_server import MCPServer

class DummyLogger(logging.LoggerAdapter):
    def __init__(self):
        super().__init__(logging.getLogger('test_mcp'), {})

class TestMCPServer(unittest.TestCase):
    def setUp(self):
        self.logger = DummyLogger()
        self.server = MCPServer(self.logger, do_scan=False)
        # capture sent messages
        self.server.sent = []
        def fake_send_message(message):
            self.server.sent.append(message)
        self.server.send_message = fake_send_message

    def parse_message(self, raw):
        # raw is dict message in send_message
        return raw

    def test_handle_initialize(self):
        self.server.handle_initialize(1, {})
        sent = self.server.sent[0]
        self.assertIsInstance(sent, dict)
        self.assertEqual(sent.get('jsonrpc'), '2.0')
        self.assertEqual(sent.get('id'), 1)
        result = sent.get('result')
        self.assertIn('serverInfo', result)
        self.assertEqual(result['serverInfo']['name'], 'Neozork MCP Server')

    def test_handle_workspace_files(self):
        # stub project_files
        self.server.project_files = {'a.py': {}, 'b.txt': {}}
        self.server.sent.clear()
        self.server.handle_workspace_files(2, {})
        sent = self.server.sent[0]
        result = sent.get('result')
        self.assertListEqual(sorted(result), ['a.py', 'b.txt'])

    def test_financial_requests(self):
        self.server.available_symbols = {'SYM1', 'SYM2'}
        self.server.available_timeframes = {'T1', 'T2'}
        # symbols
        self.server.sent.clear()
        self.server.handle_financial_symbols(3, {})
        sent_sym = self.server.sent[0]
        self.assertListEqual(sorted(sent_sym.get('result')), ['SYM1', 'SYM2'])
        # timeframes
        self.server.sent.clear()
        self.server.handle_financial_timeframes(4, {})
        sent_tf = self.server.sent[0]
        self.assertListEqual(sorted(sent_tf.get('result')), ['T1', 'T2'])

if __name__ == '__main__':
    unittest.main()

