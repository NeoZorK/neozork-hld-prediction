"""
Unit tests for PositionManager
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from decimal import Decimal

from src.pocket_hedge_fund.portfolio_management.core.position_manager import PositionManager
from src.pocket_hedge_fund.portfolio_management.models.portfolio_models import (
    Portfolio, Position, Asset, AssetType, PositionType, PositionStatus
)
from src.pocket_hedge_fund.portfolio_management.models.transaction_models import Transaction, TransactionType, TransactionStatus


class TestPositionManager:
    """Test cases for PositionManager."""
    
    @pytest.fixture
    def mock_db_manager(self):
        """Mock database manager."""
        return AsyncMock()
    
    @pytest.fixture
    def position_manager(self, mock_db_manager):
        """Position manager instance with mocked database."""
        return PositionManager(mock_db_manager)
    
    @pytest.fixture
    def sample_portfolio(self):
        """Sample portfolio for testing."""
        return Portfolio(
            id='portfolio_123',
            investor_id='investor_123',
            fund_id='fund_456',
            name='Test Portfolio',
            initial_capital=Decimal('10000.00')
        )
    
    @pytest.fixture
    def sample_asset(self):
        """Sample asset for testing."""
        return Asset(
            id='asset_123',
            symbol='BTC',
            name='Bitcoin',
            asset_type=AssetType.CRYPTO,
            currency='USD'
        )
    
    @pytest.mark.asyncio
    async def test_add_position_success(self, position_manager, sample_portfolio, sample_asset):
        """Test successful position addition."""
        # Arrange
        quantity = Decimal('1.0')
        entry_price = Decimal('50000.00')
        stop_loss = Decimal('45000.00')
        take_profit = Decimal('60000.00')
        risk_level = 0.02
        
        # Act
        position = await position_manager.add_position(
            portfolio=sample_portfolio,
            asset=sample_asset,
            position_type=PositionType.LONG,
            quantity=quantity,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_level=risk_level
        )
        
        # Assert
        assert position is not None
        assert position.portfolio_id == sample_portfolio.id
        assert position.asset_id == sample_asset.id
        assert position.asset == sample_asset
        assert position.position_type == PositionType.LONG
        assert position.quantity == quantity
        assert position.entry_price == entry_price
        assert position.current_price == entry_price
        assert position.market_value == quantity * entry_price
        assert position.unrealized_pnl == Decimal('0')
        assert position.realized_pnl == Decimal('0')
        assert position.stop_loss == stop_loss
        assert position.take_profit == take_profit
        assert position.risk_level == risk_level
        assert position.status == PositionStatus.ACTIVE
        
        # Verify position was added to portfolio
        assert len(sample_portfolio.positions) == 1
        assert sample_portfolio.positions[0] == position
        
        # Verify database save was called
        position_manager.db_manager.execute_command.assert_called()
    
    @pytest.mark.asyncio
    async def test_add_position_already_exists(self, position_manager, sample_portfolio, sample_asset):
        """Test adding position when position already exists."""
        # Arrange
        existing_position = Position(
            id='existing_pos',
            portfolio_id=sample_portfolio.id,
            asset_id=sample_asset.id,
            asset=sample_asset,
            position_type=PositionType.LONG,
            quantity=Decimal('1.0'),
            entry_price=Decimal('50000.00'),
            current_price=Decimal('50000.00'),
            market_value=Decimal('50000.00'),
            unrealized_pnl=Decimal('0'),
            realized_pnl=Decimal('0'),
            entry_date=datetime.now(datetime.UTC),
            status=PositionStatus.ACTIVE
        )
        sample_portfolio.positions.append(existing_position)
        
        # Act & Assert
        with pytest.raises(ValueError, match="Position for asset .* already exists"):
            await position_manager.add_position(
                portfolio=sample_portfolio,
                asset=sample_asset,
                position_type=PositionType.LONG,
                quantity=Decimal('1.0'),
                entry_price=Decimal('50000.00')
            )
    
    @pytest.mark.asyncio
    async def test_update_position_success(self, position_manager, sample_portfolio, sample_asset):
        """Test successful position update."""
        # Arrange
        position = Position(
            id='pos_123',
            portfolio_id=sample_portfolio.id,
            asset_id=sample_asset.id,
            asset=sample_asset,
            position_type=PositionType.LONG,
            quantity=Decimal('1.0'),
            entry_price=Decimal('50000.00'),
            current_price=Decimal('50000.00'),
            market_value=Decimal('50000.00'),
            unrealized_pnl=Decimal('0'),
            realized_pnl=Decimal('0'),
            entry_date=datetime.now(datetime.UTC),
            status=PositionStatus.ACTIVE
        )
        
        # Act
        result = await position_manager.update_position(
            position=position,
            quantity=Decimal('2.0'),
            stop_loss=Decimal('45000.00'),
            take_profit=Decimal('60000.00'),
            risk_level=0.03
        )
        
        # Assert
        assert result is True
        assert position.quantity == Decimal('2.0')
        assert position.stop_loss == Decimal('45000.00')
        assert position.take_profit == Decimal('60000.00')
        assert position.risk_level == 0.03
        assert position.updated_at is not None
        
        # Verify database update was called
        position_manager.db_manager.execute_command.assert_called()
    
    @pytest.mark.asyncio
    async def test_update_position_no_changes(self, position_manager, sample_portfolio, sample_asset):
        """Test position update with no changes."""
        # Arrange
        position = Position(
            id='pos_123',
            portfolio_id=sample_portfolio.id,
            asset_id=sample_asset.id,
            asset=sample_asset,
            position_type=PositionType.LONG,
            quantity=Decimal('1.0'),
            entry_price=Decimal('50000.00'),
            current_price=Decimal('50000.00'),
            market_value=Decimal('50000.00'),
            unrealized_pnl=Decimal('0'),
            realized_pnl=Decimal('0'),
            entry_date=datetime.now(datetime.UTC),
            status=PositionStatus.ACTIVE
        )
        
        # Act
        result = await position_manager.update_position(position=position)
        
        # Assert
        assert result is False  # No changes made
    
    @pytest.mark.asyncio
    async def test_close_position_success(self, position_manager, sample_portfolio, sample_asset):
        """Test successful position closure."""
        # Arrange
        position = Position(
            id='pos_123',
            portfolio_id=sample_portfolio.id,
            asset_id=sample_asset.id,
            asset=sample_asset,
            position_type=PositionType.LONG,
            quantity=Decimal('1.0'),
            entry_price=Decimal('50000.00'),
            current_price=Decimal('55000.00'),
            market_value=Decimal('55000.00'),
            unrealized_pnl=Decimal('5000.00'),
            realized_pnl=Decimal('0'),
            entry_date=datetime.now(datetime.UTC),
            status=PositionStatus.ACTIVE
        )
        close_price = Decimal('55000.00')
        original_quantity = position.quantity  # Save original quantity
        
        # Act
        transaction = await position_manager.close_position(
            position=position,
            close_price=close_price
        )
        
        # Assert
        assert transaction is not None
        assert transaction.portfolio_id == sample_portfolio.id
        assert transaction.asset_id == sample_asset.id
        assert transaction.transaction_type == TransactionType.SELL
        assert transaction.quantity == original_quantity  # Compare with original quantity
        assert transaction.price == close_price
        assert transaction.status == TransactionStatus.EXECUTED
        
        # Verify position was updated
        assert position.status == PositionStatus.CLOSED
        assert position.closed_at is not None
        assert position.realized_pnl == Decimal('5000.00')  # Profit from long position
        
        # Verify database operations were called
        assert position_manager.db_manager.execute_command.call_count >= 2
    
    @pytest.mark.asyncio
    async def test_close_position_partial(self, position_manager, sample_portfolio, sample_asset):
        """Test partial position closure."""
        # Arrange
        position = Position(
            id='pos_123',
            portfolio_id=sample_portfolio.id,
            asset_id=sample_asset.id,
            asset=sample_asset,
            position_type=PositionType.LONG,
            quantity=Decimal('2.0'),
            entry_price=Decimal('50000.00'),
            current_price=Decimal('55000.00'),
            market_value=Decimal('110000.00'),
            unrealized_pnl=Decimal('10000.00'),
            realized_pnl=Decimal('0'),
            entry_date=datetime.now(datetime.UTC),
            status=PositionStatus.ACTIVE
        )
        close_quantity = Decimal('1.0')
        close_price = Decimal('55000.00')
        
        # Act
        transaction = await position_manager.close_position(
            position=position,
            close_price=close_price,
            close_quantity=close_quantity
        )
        
        # Assert
        assert transaction is not None
        assert transaction.quantity == close_quantity
        
        # Verify position was partially closed
        assert position.quantity == Decimal('1.0')  # Remaining quantity
        assert position.status == PositionStatus.ACTIVE  # Still active
        assert position.realized_pnl == Decimal('5000.00')  # Profit from closed portion
    
    @pytest.mark.asyncio
    async def test_close_position_inactive(self, position_manager, sample_portfolio, sample_asset):
        """Test closing inactive position."""
        # Arrange
        position = Position(
            id='pos_123',
            portfolio_id=sample_portfolio.id,
            asset_id=sample_asset.id,
            asset=sample_asset,
            position_type=PositionType.LONG,
            quantity=Decimal('1.0'),
            entry_price=Decimal('50000.00'),
            current_price=Decimal('55000.00'),
            market_value=Decimal('55000.00'),
            unrealized_pnl=Decimal('5000.00'),
            realized_pnl=Decimal('0'),
            entry_date=datetime.now(datetime.UTC),
            status=PositionStatus.CLOSED  # Already closed
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Position .* is not active"):
            await position_manager.close_position(
                position=position,
                close_price=Decimal('55000.00')
            )
    
    @pytest.mark.asyncio
    async def test_update_position_prices(self, position_manager, sample_portfolio, sample_asset):
        """Test updating position prices."""
        # Arrange
        position1 = Position(
            id='pos_1',
            portfolio_id=sample_portfolio.id,
            asset_id='asset_1',
            asset=sample_asset,
            position_type=PositionType.LONG,
            quantity=Decimal('1.0'),
            entry_price=Decimal('50000.00'),
            current_price=Decimal('50000.00'),
            market_value=Decimal('50000.00'),
            unrealized_pnl=Decimal('0'),
            realized_pnl=Decimal('0'),
            entry_date=datetime.now(datetime.UTC),
            status=PositionStatus.ACTIVE
        )
        
        position2 = Position(
            id='pos_2',
            portfolio_id=sample_portfolio.id,
            asset_id='asset_2',
            asset=sample_asset,
            position_type=PositionType.LONG,
            quantity=Decimal('2.0'),
            entry_price=Decimal('3000.00'),
            current_price=Decimal('3000.00'),
            market_value=Decimal('6000.00'),
            unrealized_pnl=Decimal('0'),
            realized_pnl=Decimal('0'),
            entry_date=datetime.now(datetime.UTC),
            status=PositionStatus.ACTIVE
        )
        
        sample_portfolio.positions = [position1, position2]
        
        price_updates = {
            'asset_1': Decimal('55000.00'),
            'asset_2': Decimal('3200.00')
        }
        
        # Act
        result = await position_manager.update_position_prices(sample_portfolio, price_updates)
        
        # Assert
        assert result is True
        assert position1.current_price == Decimal('55000.00')
        assert position1.market_value == Decimal('55000.00')
        assert position1.unrealized_pnl == Decimal('5000.00')  # Profit from price increase
        
        assert position2.current_price == Decimal('3200.00')
        assert position2.market_value == Decimal('6400.00')
        assert position2.unrealized_pnl == Decimal('400.00')  # Profit from price increase
        
        # Verify database updates were called
        assert position_manager.db_manager.execute_command.call_count >= 2
    
    @pytest.mark.asyncio
    async def test_check_stop_loss_take_profit(self, position_manager, sample_portfolio, sample_asset):
        """Test stop loss and take profit checking."""
        # Arrange
        position1 = Position(
            id='pos_1',
            portfolio_id=sample_portfolio.id,
            asset_id='asset_1',
            asset=sample_asset,
            position_type=PositionType.LONG,
            quantity=Decimal('1.0'),
            entry_price=Decimal('50000.00'),
            current_price=Decimal('50000.00'),
            market_value=Decimal('50000.00'),
            unrealized_pnl=Decimal('0'),
            realized_pnl=Decimal('0'),
            entry_date=datetime.now(datetime.UTC),
            stop_loss=Decimal('45000.00'),
            take_profit=Decimal('60000.00'),
            status=PositionStatus.ACTIVE
        )
        
        position2 = Position(
            id='pos_2',
            portfolio_id=sample_portfolio.id,
            asset_id='asset_2',
            asset=sample_asset,
            position_type=PositionType.SHORT,
            quantity=Decimal('1.0'),
            entry_price=Decimal('50000.00'),
            current_price=Decimal('50000.00'),
            market_value=Decimal('50000.00'),
            unrealized_pnl=Decimal('0'),
            realized_pnl=Decimal('0'),
            entry_date=datetime.now(datetime.UTC),
            stop_loss=Decimal('55000.00'),
            take_profit=Decimal('40000.00'),
            status=PositionStatus.ACTIVE
        )
        
        sample_portfolio.positions = [position1, position2]
        
        # Test stop loss trigger for long position
        price_updates = {
            'asset_1': Decimal('44000.00'),  # Below stop loss
            'asset_2': Decimal('50000.00')
        }
        
        # Act
        triggered_positions = await position_manager.check_stop_loss_take_profit(
            sample_portfolio, price_updates
        )
        
        # Assert
        assert len(triggered_positions) == 1
        assert triggered_positions[0]['position'] == position1
        assert triggered_positions[0]['close_reason'] == 'stop_loss'
        assert triggered_positions[0]['trigger_price'] == Decimal('44000.00')
        
        # Test take profit trigger for short position
        price_updates = {
            'asset_1': Decimal('50000.00'),
            'asset_2': Decimal('39000.00')  # Below take profit for short
        }
        
        # Act
        triggered_positions = await position_manager.check_stop_loss_take_profit(
            sample_portfolio, price_updates
        )
        
        # Assert
        assert len(triggered_positions) == 1
        assert triggered_positions[0]['position'] == position2
        assert triggered_positions[0]['close_reason'] == 'take_profit'
        assert triggered_positions[0]['trigger_price'] == Decimal('39000.00')
    
    @pytest.mark.asyncio
    async def test_get_position_performance(self, position_manager, sample_portfolio, sample_asset):
        """Test getting position performance metrics."""
        # Arrange
        position = Position(
            id='pos_123',
            portfolio_id=sample_portfolio.id,
            asset_id=sample_asset.id,
            asset=sample_asset,
            position_type=PositionType.LONG,
            quantity=Decimal('1.0'),
            entry_price=Decimal('50000.00'),
            current_price=Decimal('55000.00'),
            market_value=Decimal('55000.00'),
            unrealized_pnl=Decimal('5000.00'),
            realized_pnl=Decimal('1000.00'),
            entry_date=datetime.now(datetime.UTC),
            status=PositionStatus.ACTIVE
        )
        
        # Act
        performance = await position_manager.get_position_performance(position)
        
        # Assert
        assert performance is not None
        assert performance['position_id'] == position.id
        assert performance['asset_id'] == position.asset_id
        assert performance['asset_name'] == position.asset.name
        assert performance['position_type'] == position.position_type.value
        assert performance['quantity'] == float(position.quantity)
        assert performance['entry_price'] == float(position.entry_price)
        assert performance['current_price'] == float(position.current_price)
        assert performance['market_value'] == float(position.market_value)
        assert performance['unrealized_pnl'] == float(position.unrealized_pnl)
        assert performance['realized_pnl'] == float(position.realized_pnl)
        assert performance['return_percentage'] == 10.0  # 10% return
        assert performance['status'] == position.status.value
