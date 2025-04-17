# tests/utils/test_utils.py

import unittest
from unittest.mock import patch #, MagicMock

# Import the function to test
from src.utils.utils import determine_point_size

# Dummy logger
class MockLogger:
    def print_info(self, msg): pass
    def print_warning(self, msg): pass
    def print_error(self, msg): pass
    def print_debug(self, msg): pass

# Mock yfinance Ticker class and its info attribute/method
class MockYFinanceTicker:
    def __init__(self, ticker_info=None, raise_exception=False):
        self._ticker_info = ticker_info if ticker_info is not None else {}
        self._raise_exception = raise_exception

    @property
    def info(self):
        if self._raise_exception:
            raise Exception("Simulated yfinance error")
        # Return a copy to prevent modification if info is called multiple times
        return self._ticker_info.copy()

# Unit tests for general utility functions
class TestUtils(unittest.TestCase):

    # Patch the logger and yfinance.Ticker in the utils module
    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_currency_non_jpy(self, mock_yf_ticker, _):
        ticker_info = {'quoteType': 'CURRENCY', 'currency': 'USD'}
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info)
        point = determine_point_size("EURUSD=X")
        self.assertEqual(point, 0.00001)
        mock_yf_ticker.assert_called_once_with("EURUSD=X")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_currency_jpy_in_ticker(self, mock_yf_ticker, _):
        ticker_info = {'quoteType': 'CURRENCY', 'currency': 'JPY'} # Currency might be USD, but ticker implies JPY
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info)
        point = determine_point_size("USDJPY=X")
        self.assertEqual(point, 0.001)
        mock_yf_ticker.assert_called_once_with("USDJPY=X")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_currency_jpy_in_currency(self, mock_yf_ticker, _):
        ticker_info = {'quoteType': 'CURRENCY', 'currency': 'JPY'}
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info)
        point = determine_point_size("AUDCAD=X") # Ticker doesn't contain JPY
        self.assertEqual(point, 0.001) # But currency is JPY
        mock_yf_ticker.assert_called_once_with("AUDCAD=X")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_equity(self, mock_yf_ticker, _):
        ticker_info = {'quoteType': 'EQUITY', 'currency': 'USD'}
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info)
        point = determine_point_size("AAPL")
        self.assertEqual(point, 0.01)
        mock_yf_ticker.assert_called_once_with("AAPL")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_index(self, mock_yf_ticker, _):
        ticker_info = {'quoteType': 'INDEX', 'currency': 'USD'}
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info)
        point = determine_point_size("^GSPC")
        self.assertEqual(point, 0.01)
        mock_yf_ticker.assert_called_once_with("^GSPC")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_crypto_high_value(self, mock_yf_ticker, _):
        # Using regularMarketPrice
        ticker_info = {'quoteType': 'CRYPTOCURRENCY', 'regularMarketPrice': 60000, 'currency': 'USD'}
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info)
        point = determine_point_size("BTC-USD")
        self.assertEqual(point, 0.1) # High value crypto guess
        mock_yf_ticker.assert_called_once_with("BTC-USD")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_crypto_low_value(self, mock_yf_ticker, _):
         # Using currentPrice as fallback
        ticker_info = {'quoteType': 'CRYPTOCURRENCY', 'currentPrice': 0.5, 'currency': 'USD'}
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info)
        point = determine_point_size("XRP-USD")
        self.assertEqual(point, 0.001) # Price < 10
        mock_yf_ticker.assert_called_once_with("XRP-USD")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_crypto_very_low_value(self, mock_yf_ticker, _):
         # Using ask as fallback
        ticker_info = {'quoteType': 'CRYPTOCURRENCY', 'ask': 0.0005, 'currency': 'USD'}
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info)
        point = determine_point_size("SHIB-USD")
        self.assertEqual(point, 0.000001) # Price < 0.001
        mock_yf_ticker.assert_called_once_with("SHIB-USD")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_crypto_mid_value(self, mock_yf_ticker, _):
        ticker_info = {'quoteType': 'CRYPTOCURRENCY', 'bid': 150, 'currency': 'USD'}
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info)
        point = determine_point_size("ETH-USD")
        self.assertEqual(point, 0.01) # Price < 1000
        mock_yf_ticker.assert_called_once_with("ETH-USD")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_crypto_no_price(self, mock_yf_ticker, _):
        ticker_info = {'quoteType': 'CRYPTOCURRENCY', 'currency': 'USD'} # No price fields
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info)
        point = determine_point_size("NOCOIN-USD")
        self.assertEqual(point, 0.01) # Default guess
        mock_yf_ticker.assert_called_once_with("NOCOIN-USD")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_future(self, mock_yf_ticker, _):
        ticker_info = {'quoteType': 'FUTURE', 'currency': 'USD'}
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info)
        point = determine_point_size("ES=F")
        self.assertIsNone(point) # Should fail for FUTURE
        mock_yf_ticker.assert_called_once_with("ES=F")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_unknown_type(self, mock_yf_ticker, _):
        ticker_info = {'quoteType': 'UNKNOWN', 'currency': 'XXX'}
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info)
        point = determine_point_size("UNKNOWNTICKER")
        self.assertIsNone(point) # Should fail for unknown type
        mock_yf_ticker.assert_called_once_with("UNKNOWNTICKER")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_yfinance_exception(self, mock_yf_ticker, _):
        # Configure the mock Ticker to raise an exception when .info is accessed
        mock_yf_ticker.return_value = MockYFinanceTicker(raise_exception=True)
        point = determine_point_size("ERRORTICKER")
        self.assertIsNone(point) # Should fail gracefully
        mock_yf_ticker.assert_called_once_with("ERRORTICKER")

    @patch('src.utils.utils.logger', new_callable=MockLogger)
    @patch('src.utils.utils.yf.Ticker')
    def test_determine_point_size_no_info(self, mock_yf_ticker, _):
        # Simulate yf.Ticker().info returning an empty dict or None (less likely)
        mock_yf_ticker.return_value = MockYFinanceTicker(ticker_info={})
        point = determine_point_size("NOINFO")
        self.assertIsNone(point) # Should fail if quoteType is missing
        mock_yf_ticker.assert_called_once_with("NOINFO")

# Allow running the tests directly
if __name__ == '__main__':
    unittest.main()