"""
Test module for debug_yfinance.py script.
Tests functionality without making real API requests to avoid rate limiting in Docker.
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from datetime import datetime

# Add the scripts directory to the path
project_root = Path(__file__).parent.parent
scripts_dir = project_root / "scripts"
sys.path.insert(0, str(scripts_dir))

# Import the module to test
from debug.debug_yfinance import (
    YFinanceDownloader, 
    DEFAULT_TICKERS, 
    get_tickers_for_docker,
    prompt_for_tickers
)


class TestYFinanceDownloader:
    """Test class for YFinanceDownloader functionality."""

    def test_initialization(self):
        """Test that YFinanceDownloader initializes correctly."""
        downloader = YFinanceDownloader(single_attempt=True)
        
        assert downloader.cache_dir == ".yf_cache"
        assert downloader.max_retries == 1
        assert downloader.request_delay == 1.0
        assert downloader.retry_delay_base == 2.0
        assert downloader.backoff_factor == 1.5
        assert downloader.jitter == 0.2
        assert downloader.successful_downloads == []
        assert downloader.failed_downloads == []

    def test_create_session(self):
        """Test session creation with proper headers."""
        downloader = YFinanceDownloader()
        session = downloader._create_session()
        
        assert session is not None
        assert 'User-Agent' in session.headers
        assert 'Accept' in session.headers
        assert 'Accept-Language' in session.headers

    def test_rotate_user_agent(self):
        """Test user agent rotation."""
        downloader = YFinanceDownloader()
        original_ua = downloader.session.headers['User-Agent']
        
        downloader._rotate_user_agent()
        new_ua = downloader.session.headers['User-Agent']
        
        assert new_ua != original_ua
        assert new_ua in [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        ]

    def test_calculate_delay(self):
        """Test delay calculation with exponential backoff."""
        downloader = YFinanceDownloader()
        
        # First attempt should have base delay
        delay1 = downloader._calculate_delay(0)
        assert 1.0 <= delay1 <= 1.2  # Base delay (1.0) + jitter (0-0.2)
        
        # Second attempt should have higher delay
        delay2 = downloader._calculate_delay(1)
        assert delay2 > delay1
        assert delay2 <= 10.0  # Should be capped at 10.0

    @patch('debug.debug_yfinance.requests.Session')
    def test_connectivity_check_success(self, mock_session):
        """Test successful connectivity check."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_session.return_value.get.return_value = mock_response
        
        downloader = YFinanceDownloader()
        result = downloader.check_connectivity()
        
        assert result is True

    @patch('debug.debug_yfinance.requests.Session')
    def test_connectivity_check_failure(self, mock_session):
        """Test failed connectivity check."""
        mock_session.return_value.get.side_effect = Exception("Connection failed")
        
        downloader = YFinanceDownloader()
        result = downloader.check_connectivity()
        
        assert result is False

    @patch('debug.debug_yfinance.requests.Session')
    def test_direct_api_request_success(self, mock_session):
        """Test successful direct API request."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"test content"
        mock_response.json.return_value = {
            'chart': {
                'result': [{
                    'timestamp': [1640995200, 1641081600],  # Sample timestamps
                    'indicators': {
                        'quote': [{
                            'open': [100.0, 101.0],
                            'high': [102.0, 103.0],
                            'low': [99.0, 100.0],
                            'close': [101.0, 102.0],
                            'volume': [1000, 1100]
                        }]
                    }
                }]
            }
        }
        mock_session.return_value.get.return_value = mock_response
        
        downloader = YFinanceDownloader()
        result = downloader.direct_api_request('AAPL', '1mo', '1d')
        
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert 'Open' in result.columns
        assert 'High' in result.columns
        assert 'Low' in result.columns
        assert 'Close' in result.columns
        assert 'Volume' in result.columns

    @patch('debug.debug_yfinance.requests.Session')
    def test_direct_api_request_failure(self, mock_session):
        """Test failed direct API request."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_session.return_value.get.return_value = mock_response
        
        downloader = YFinanceDownloader()
        result = downloader.direct_api_request('INVALID', '1mo', '1d')
        
        assert result is None

    @patch('debug.debug_yfinance.yf.download')
    def test_download_ticker_success(self, mock_yf_download):
        """Test successful ticker download."""
        # Mock successful yfinance download
        mock_data = pd.DataFrame({
            'Open': [100.0, 101.0],
            'High': [102.0, 103.0],
            'Low': [99.0, 100.0],
            'Close': [101.0, 102.0],
            'Volume': [1000, 1100]
        }, index=pd.to_datetime(['2022-01-01', '2022-01-02']))
        mock_yf_download.return_value = mock_data
        
        # Mock the direct API request to return None (so it falls back to yfinance)
        with patch.object(YFinanceDownloader, 'direct_api_request', return_value=None):
            downloader = YFinanceDownloader(single_attempt=True)
            result = downloader.download_ticker('AAPL', '1mo', '1d')
        
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        # Note: successful_downloads is only updated in download_multiple, not download_ticker

    @patch('debug.debug_yfinance.yf.download')
    def test_download_ticker_failure(self, mock_yf_download):
        """Test failed ticker download."""
        # Mock failed yfinance download
        mock_yf_download.side_effect = Exception("Download failed")
        
        downloader = YFinanceDownloader(single_attempt=True)
        result = downloader.download_ticker('INVALID', '1mo', '1d')
        
        assert result is None
        assert 'INVALID' in downloader.failed_downloads

    def test_download_multiple_limit(self):
        """Test that download_multiple limits to 5 tickers."""
        downloader = YFinanceDownloader(single_attempt=True)
        
        # Test with more than 5 tickers
        many_tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA']
        
        with patch.object(downloader, 'download_ticker') as mock_download:
            mock_download.return_value = pd.DataFrame()
            result = downloader.download_multiple(many_tickers, '1mo', '1d')
        
        # Should only process first 5 tickers
        assert len(result) == 5
        assert mock_download.call_count == 5

    def test_print_summary(self, capsys):
        """Test summary printing."""
        downloader = YFinanceDownloader()
        downloader.successful_downloads = ['AAPL', 'GOOGL']
        downloader.failed_downloads = ['INVALID']
        
        downloader.print_summary()
        captured = capsys.readouterr()
        
        assert "DOWNLOAD SUMMARY" in captured.out
        assert "Total tickers processed: 3" in captured.out
        assert "Successfully downloaded: 2 (66.7%)" in captured.out
        assert "Failed downloads: 1 (33.3%)" in captured.out
        assert "AAPL" in captured.out
        assert "GOOGL" in captured.out
        assert "INVALID" in captured.out


class TestHelperFunctions:
    """Test class for helper functions."""

    def test_get_tickers_for_docker(self):
        """Test get_tickers_for_docker function."""
        tickers = get_tickers_for_docker()
        
        assert len(tickers) == 1
        assert tickers[0] == DEFAULT_TICKERS[0]
        assert tickers[0] == 'AAPL'

    @patch('builtins.input')
    def test_prompt_for_tickers_docker_environment(self, mock_input):
        """Test prompt_for_tickers in Docker environment."""
        # Mock Docker environment
        with patch.dict(os.environ, {'DOCKER_CONTAINER': 'true'}):
            tickers = prompt_for_tickers()
        
        assert len(tickers) == 1
        assert tickers[0] == 'AAPL'
        # Should not call input() in Docker environment
        mock_input.assert_not_called()

    @patch('builtins.input')
    def test_prompt_for_tickers_all_selection(self, mock_input):
        """Test prompt_for_tickers with 'all' selection."""
        # Mock non-Docker environment
        with patch.dict(os.environ, {}, clear=True):
            with patch('os.path.exists', return_value=False):
                mock_input.return_value = 'all'
                tickers = prompt_for_tickers()
        
        assert len(tickers) == 5
        assert tickers == DEFAULT_TICKERS

    @patch('builtins.input')
    def test_prompt_for_tickers_specific_selection(self, mock_input):
        """Test prompt_for_tickers with specific selection."""
        # Mock non-Docker environment
        with patch.dict(os.environ, {}, clear=True):
            with patch('os.path.exists', return_value=False):
                mock_input.return_value = '1,3'
                tickers = prompt_for_tickers()
        
        assert len(tickers) == 2
        assert tickers == ['AAPL', 'BTC-USD']

    @patch('builtins.input')
    def test_prompt_for_tickers_fallback(self, mock_input):
        """Test prompt_for_tickers with input error fallback."""
        # Mock non-Docker environment
        with patch.dict(os.environ, {}, clear=True):
            with patch('os.path.exists', return_value=False):
                mock_input.side_effect = Exception("Input error")
                tickers = prompt_for_tickers()
        
        assert len(tickers) == 1
        assert tickers[0] == 'AAPL'


class TestConstants:
    """Test class for constants and configuration."""

    def test_default_tickers(self):
        """Test DEFAULT_TICKERS constant."""
        assert len(DEFAULT_TICKERS) == 5
        assert 'AAPL' in DEFAULT_TICKERS
        assert 'EURUSD=X' in DEFAULT_TICKERS
        assert 'BTC-USD' in DEFAULT_TICKERS
        assert 'GLD' in DEFAULT_TICKERS
        assert 'CL=F' in DEFAULT_TICKERS

    def test_user_agents(self):
        """Test USER_AGENTS list."""
        from debug.debug_yfinance import USER_AGENTS
        
        assert len(USER_AGENTS) == 5
        assert all('Mozilla' in ua for ua in USER_AGENTS)
        assert all('AppleWebKit' in ua or 'Gecko' in ua for ua in USER_AGENTS)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
