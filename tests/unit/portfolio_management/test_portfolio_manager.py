"""
Unit tests for PortfolioManager
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from decimal import Decimal

from src.pocket_hedge_fund.portfolio_management.core.portfolio_manager import PortfolioManager
from src.pocket_hedge_fund.portfolio_management.models.portfolio_models import Portfolio, Asset, AssetType


class TestPortfolioManager:
    """Test cases for PortfolioManager."""
    
    @pytest.fixture
    def mock_db_manager(self):
        """Mock database manager."""
        return AsyncMock()
    
    @pytest.fixture
    def portfolio_manager(self, mock_db_manager):
        """Portfolio manager instance with mocked database."""
        return PortfolioManager(mock_db_manager)
    
    @pytest.fixture
    def sample_portfolio_data(self):
        """Sample portfolio data for testing."""
        return {
            'investor_id': 'investor_123',
            'fund_id': 'fund_456',
            'name': 'Test Portfolio',
            'description': 'Test portfolio for unit testing',
            'initial_capital': Decimal('10000.00')
        }
    
    @pytest.mark.asyncio
    async def test_create_portfolio_success(self, portfolio_manager, sample_portfolio_data):
        """Test successful portfolio creation."""
        # Act
        portfolio = await portfolio_manager.create_portfolio(
            investor_id=sample_portfolio_data['investor_id'],
            fund_id=sample_portfolio_data['fund_id'],
            name=sample_portfolio_data['name'],
            description=sample_portfolio_data['description'],
            initial_capital=sample_portfolio_data['initial_capital']
        )
        
        # Assert
        assert portfolio is not None
        assert portfolio.investor_id == sample_portfolio_data['investor_id']
        assert portfolio.fund_id == sample_portfolio_data['fund_id']
        assert portfolio.name == sample_portfolio_data['name']
        assert portfolio.description == sample_portfolio_data['description']
        assert portfolio.initial_capital == sample_portfolio_data['initial_capital']
        assert portfolio.current_capital == sample_portfolio_data['initial_capital']
        assert portfolio.is_active is True
        assert len(portfolio.risk_limits) > 0
        
        # Verify database save was called
        portfolio_manager.db_manager.execute_command.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_portfolio_without_db(self, sample_portfolio_data):
        """Test portfolio creation without database manager."""
        # Arrange
        portfolio_manager = PortfolioManager(None)
        
        # Act
        portfolio = await portfolio_manager.create_portfolio(
            investor_id=sample_portfolio_data['investor_id'],
            fund_id=sample_portfolio_data['fund_id'],
            name=sample_portfolio_data['name'],
            initial_capital=sample_portfolio_data['initial_capital']
        )
        
        # Assert
        assert portfolio is not None
        assert portfolio.investor_id == sample_portfolio_data['investor_id']
        assert portfolio.fund_id == sample_portfolio_data['fund_id']
        assert portfolio.name == sample_portfolio_data['name']
    
    @pytest.mark.asyncio
    async def test_get_portfolio_success(self, portfolio_manager):
        """Test successful portfolio retrieval."""
        # Arrange
        portfolio_id = 'portfolio_123'
        expected_portfolio = Portfolio(
            id=portfolio_id,
            investor_id='investor_123',
            fund_id='fund_456',
            name='Test Portfolio'
        )
        portfolio_manager.portfolios[portfolio_id] = expected_portfolio
        
        # Act
        result = await portfolio_manager.get_portfolio(portfolio_id)
        
        # Assert
        assert result is not None
        assert result.id == portfolio_id
        assert result.name == 'Test Portfolio'
    
    @pytest.mark.asyncio
    async def test_get_portfolio_not_found(self, portfolio_manager):
        """Test portfolio retrieval when portfolio doesn't exist."""
        # Arrange
        portfolio_id = 'nonexistent_portfolio'
        
        # Act
        result = await portfolio_manager.get_portfolio(portfolio_id)
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_update_portfolio_success(self, portfolio_manager):
        """Test successful portfolio update."""
        # Arrange
        portfolio = Portfolio(
            id='portfolio_123',
            investor_id='investor_123',
            fund_id='fund_456',
            name='Original Name'
        )
        portfolio_manager.portfolios[portfolio.id] = portfolio
        
        # Act
        portfolio.name = 'Updated Name'
        portfolio.description = 'Updated Description'
        result = await portfolio_manager.update_portfolio(portfolio)
        
        # Assert
        assert result is True
        assert portfolio.name == 'Updated Name'
        assert portfolio.description == 'Updated Description'
        assert portfolio.updated_at is not None
        
        # Verify database update was called
        portfolio_manager.db_manager.execute_command.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_portfolio_success(self, portfolio_manager):
        """Test successful portfolio deletion."""
        # Arrange
        portfolio_id = 'portfolio_123'
        portfolio = Portfolio(
            id=portfolio_id,
            investor_id='investor_123',
            fund_id='fund_456',
            name='Test Portfolio'
        )
        portfolio_manager.portfolios[portfolio_id] = portfolio
        
        # Act
        result = await portfolio_manager.delete_portfolio(portfolio_id)
        
        # Assert
        assert result is True
        assert portfolio_id not in portfolio_manager.portfolios
        
        # Verify database delete was called
        portfolio_manager.db_manager.execute_command.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_portfolio_by_fund(self, portfolio_manager):
        """Test getting portfolios by fund ID."""
        # Arrange
        fund_id = 'fund_456'
        portfolio1 = Portfolio(
            id='portfolio_1',
            investor_id='investor_1',
            fund_id=fund_id,
            name='Portfolio 1'
        )
        portfolio2 = Portfolio(
            id='portfolio_2',
            investor_id='investor_2',
            fund_id=fund_id,
            name='Portfolio 2'
        )
        portfolio3 = Portfolio(
            id='portfolio_3',
            investor_id='investor_3',
            fund_id='fund_789',
            name='Portfolio 3'
        )
        
        portfolio_manager.portfolios = {
            'portfolio_1': portfolio1,
            'portfolio_2': portfolio2,
            'portfolio_3': portfolio3
        }
        
        # Act
        result = await portfolio_manager.get_portfolio_by_fund(fund_id)
        
        # Assert
        assert len(result) == 2
        assert portfolio1 in result
        assert portfolio2 in result
        assert portfolio3 not in result
    
    @pytest.mark.asyncio
    async def test_get_portfolio_by_investor(self, portfolio_manager):
        """Test getting portfolios by investor ID."""
        # Arrange
        investor_id = 'investor_123'
        portfolio1 = Portfolio(
            id='portfolio_1',
            investor_id=investor_id,
            fund_id='fund_1',
            name='Portfolio 1'
        )
        portfolio2 = Portfolio(
            id='portfolio_2',
            investor_id=investor_id,
            fund_id='fund_2',
            name='Portfolio 2'
        )
        portfolio3 = Portfolio(
            id='portfolio_3',
            investor_id='investor_456',
            fund_id='fund_3',
            name='Portfolio 3'
        )
        
        portfolio_manager.portfolios = {
            'portfolio_1': portfolio1,
            'portfolio_2': portfolio2,
            'portfolio_3': portfolio3
        }
        
        # Act
        result = await portfolio_manager.get_portfolio_by_investor(investor_id)
        
        # Assert
        assert len(result) == 2
        assert portfolio1 in result
        assert portfolio2 in result
        assert portfolio3 not in result
    
    @pytest.mark.asyncio
    async def test_calculate_portfolio_metrics(self, portfolio_manager):
        """Test portfolio metrics calculation."""
        # Arrange
        portfolio = Portfolio(
            id='portfolio_123',
            investor_id='investor_123',
            fund_id='fund_456',
            name='Test Portfolio',
            initial_capital=Decimal('10000.00')
        )
        
        # Add some mock positions
        asset1 = Asset(
            id='asset_1',
            symbol='BTC',
            name='Bitcoin',
            asset_type=AssetType.CRYPTO
        )
        asset2 = Asset(
            id='asset_2',
            symbol='ETH',
            name='Ethereum',
            asset_type=AssetType.CRYPTO
        )
        
        from src.pocket_hedge_fund.portfolio_management.models.portfolio_models import Position, PositionType, PositionStatus
        
        position1 = Position(
            id='pos_1',
            portfolio_id=portfolio.id,
            asset_id='asset_1',
            asset=asset1,
            position_type=PositionType.LONG,
            quantity=Decimal('1.0'),
            entry_price=Decimal('50000.00'),
            current_price=Decimal('55000.00'),
            market_value=Decimal('55000.00'),
            unrealized_pnl=Decimal('5000.00'),
            realized_pnl=Decimal('0.00'),
            entry_date=datetime.now(datetime.UTC),
            status=PositionStatus.ACTIVE
        )
        
        position2 = Position(
            id='pos_2',
            portfolio_id=portfolio.id,
            asset_id='asset_2',
            asset=asset2,
            position_type=PositionType.LONG,
            quantity=Decimal('10.0'),
            entry_price=Decimal('3000.00'),
            current_price=Decimal('3200.00'),
            market_value=Decimal('32000.00'),
            unrealized_pnl=Decimal('2000.00'),
            realized_pnl=Decimal('0.00'),
            entry_date=datetime.now(datetime.UTC),
            status=PositionStatus.ACTIVE
        )
        
        portfolio.positions = [position1, position2]
        
        # Act
        metrics = await portfolio_manager.calculate_portfolio_metrics(portfolio)
        
        # Assert
        assert metrics is not None
        assert 'total_value' in metrics
        assert 'total_pnl' in metrics
        assert 'positions_count' in metrics
        assert 'active_positions' in metrics
        assert metrics['total_value'] > 0
        assert metrics['active_positions'] == 2
    
    @pytest.mark.asyncio
    async def test_validate_portfolio_limits(self, portfolio_manager):
        """Test portfolio limits validation."""
        # Arrange
        portfolio = Portfolio(
            id='portfolio_123',
            investor_id='investor_123',
            fund_id='fund_456',
            name='Test Portfolio'
        )
        
        # Set risk limits
        portfolio.risk_limits = {
            'max_position_size': 0.1,  # 10% max per position
            'max_sector_exposure': 0.3,  # 30% max per sector
            'max_drawdown': 0.15,  # 15% max drawdown
            'var_limit': 0.05,  # 5% VaR limit
            'leverage_limit': 2.0  # 2x max leverage
        }
        
        # Act
        validation_result = await portfolio_manager.validate_portfolio_limits(portfolio)
        
        # Assert
        assert validation_result is not None
        assert 'is_valid' in validation_result
        assert 'violations' in validation_result
        assert 'warnings' in validation_result
        assert isinstance(validation_result['is_valid'], bool)
        assert isinstance(validation_result['violations'], list)
        assert isinstance(validation_result['warnings'], list)
