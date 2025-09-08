"""
Tokenization System for Fund Shares

This module provides tokenization capabilities including:
- ERC-20 fund share tokens
- Fractional ownership management
- Secondary market trading
- Share analytics and reporting
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio

logger = logging.getLogger(__name__)


class TokenType(Enum):
    """Token types."""
    FUND_SHARE = "fund_share"
    GOVERNANCE = "governance"
    UTILITY = "utility"
    REWARD = "reward"


class ShareStatus(Enum):
    """Share status types."""
    ACTIVE = "active"
    LOCKED = "locked"
    BURNED = "burned"
    TRANSFERRED = "transferred"


@dataclass
class FundShare:
    """Fund share token data."""
    token_id: str
    owner_address: str
    amount: float
    share_percentage: float
    status: ShareStatus
    created_at: datetime
    last_transfer: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ShareTransaction:
    """Share transaction data."""
    transaction_id: str
    from_address: str
    to_address: str
    amount: float
    price: float
    transaction_type: str  # 'mint', 'burn', 'transfer', 'trade'
    timestamp: datetime
    block_number: Optional[int] = None
    transaction_hash: Optional[str] = None


class TokenizationSystem:
    """
    Tokenization System for fund shares.
    
    This system provides ERC-20 token functionality for fund shares,
    enabling fractional ownership and secondary market trading.
    """
    
    def __init__(self):
        self.fund_shares = {}
        self.share_transactions = []
        self.total_supply = 0
        self.circulating_supply = 0
        self.share_price = 1.0
        self.market_cap = 0.0
    
    async def create_fund_shares(self, total_supply: int, 
                               initial_price: float) -> Dict[str, Any]:
        """
        Create initial fund share tokens.
        
        Args:
            total_supply: Total number of shares to create
            initial_price: Initial price per share
            
        Returns:
            Token creation results
        """
        try:
            logger.info(f"Creating {total_supply} fund shares at ${initial_price} each...")
            
            self.total_supply = total_supply
            self.circulating_supply = total_supply
            self.share_price = initial_price
            self.market_cap = total_supply * initial_price
            
            # Create initial transaction record
            transaction = ShareTransaction(
                transaction_id=f"mint_initial_{datetime.now().timestamp()}",
                from_address="0x0000000000000000000000000000000000000000",  # Zero address for minting
                to_address="0x0000000000000000000000000000000000000001",  # Fund address
                amount=total_supply,
                price=initial_price,
                transaction_type="mint",
                timestamp=datetime.now()
            )
            
            self.share_transactions.append(transaction)
            
            result = {
                'status': 'success',
                'total_supply': total_supply,
                'initial_price': initial_price,
                'market_cap': self.market_cap,
                'transaction_id': transaction.transaction_id
            }
            
            logger.info(f"Fund shares created: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Fund share creation failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def mint_shares(self, to_address: str, amount: float, 
                         price: Optional[float] = None) -> Dict[str, Any]:
        """
        Mint new fund shares to an address.
        
        Args:
            to_address: Address to receive shares
            amount: Amount of shares to mint
            price: Price per share (uses current price if None)
            
        Returns:
            Minting results
        """
        try:
            logger.info(f"Minting {amount} shares to {to_address}...")
            
            if price is None:
                price = self.share_price
            
            # Create share record
            share = FundShare(
                token_id=f"share_{to_address}_{datetime.now().timestamp()}",
                owner_address=to_address,
                amount=amount,
                share_percentage=(amount / self.total_supply) * 100,
                status=ShareStatus.ACTIVE,
                created_at=datetime.now()
            )
            
            self.fund_shares[share.token_id] = share
            self.circulating_supply += amount
            self.market_cap += amount * price
            
            # Create transaction record
            transaction = ShareTransaction(
                transaction_id=f"mint_{datetime.now().timestamp()}",
                from_address="0x0000000000000000000000000000000000000000",  # Zero address
                to_address=to_address,
                amount=amount,
                price=price,
                transaction_type="mint",
                timestamp=datetime.now()
            )
            
            self.share_transactions.append(transaction)
            
            result = {
                'status': 'success',
                'token_id': share.token_id,
                'amount': amount,
                'price': price,
                'new_circulating_supply': self.circulating_supply,
                'transaction_id': transaction.transaction_id
            }
            
            logger.info(f"Shares minted: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Share minting failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def transfer_shares(self, from_address: str, to_address: str, 
                            amount: float, price: float) -> Dict[str, Any]:
        """
        Transfer shares between addresses.
        
        Args:
            from_address: Address sending shares
            to_address: Address receiving shares
            amount: Amount of shares to transfer
            price: Price per share
            
        Returns:
            Transfer results
        """
        try:
            logger.info(f"Transferring {amount} shares from {from_address} to {to_address}...")
            
            # Find shares owned by from_address
            sender_shares = [
                share for share in self.fund_shares.values()
                if share.owner_address == from_address and share.status == ShareStatus.ACTIVE
            ]
            
            if not sender_shares:
                return {'status': 'error', 'message': 'No shares found for sender'}
            
            # Calculate total available shares
            total_available = sum(share.amount for share in sender_shares)
            if total_available < amount:
                return {'status': 'error', 'message': 'Insufficient shares'}
            
            # Transfer shares (simplified - in reality would need more complex logic)
            remaining_amount = amount
            for share in sender_shares:
                if remaining_amount <= 0:
                    break
                
                transfer_amount = min(share.amount, remaining_amount)
                
                # Update existing share
                share.amount -= transfer_amount
                share.last_transfer = datetime.now()
                
                # Create new share for recipient
                new_share = FundShare(
                    token_id=f"share_{to_address}_{datetime.now().timestamp()}",
                    owner_address=to_address,
                    amount=transfer_amount,
                    share_percentage=(transfer_amount / self.total_supply) * 100,
                    status=ShareStatus.ACTIVE,
                    created_at=datetime.now()
                )
                
                self.fund_shares[new_share.token_id] = new_share
                remaining_amount -= transfer_amount
            
            # Create transaction record
            transaction = ShareTransaction(
                transaction_id=f"transfer_{datetime.now().timestamp()}",
                from_address=from_address,
                to_address=to_address,
                amount=amount,
                price=price,
                transaction_type="transfer",
                timestamp=datetime.now()
            )
            
            self.share_transactions.append(transaction)
            
            result = {
                'status': 'success',
                'amount': amount,
                'price': price,
                'transaction_id': transaction.transaction_id
            }
            
            logger.info(f"Shares transferred: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Share transfer failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def burn_shares(self, from_address: str, amount: float) -> Dict[str, Any]:
        """
        Burn (destroy) fund shares.
        
        Args:
            from_address: Address burning shares
            amount: Amount of shares to burn
            
        Returns:
            Burning results
        """
        try:
            logger.info(f"Burning {amount} shares from {from_address}...")
            
            # Find shares owned by from_address
            sender_shares = [
                share for share in self.fund_shares.values()
                if share.owner_address == from_address and share.status == ShareStatus.ACTIVE
            ]
            
            if not sender_shares:
                return {'status': 'error', 'message': 'No shares found for sender'}
            
            # Calculate total available shares
            total_available = sum(share.amount for share in sender_shares)
            if total_available < amount:
                return {'status': 'error', 'message': 'Insufficient shares'}
            
            # Burn shares
            remaining_amount = amount
            for share in sender_shares:
                if remaining_amount <= 0:
                    break
                
                burn_amount = min(share.amount, remaining_amount)
                share.amount -= burn_amount
                share.status = ShareStatus.BURNED
                remaining_amount -= burn_amount
            
            self.circulating_supply -= amount
            self.market_cap -= amount * self.share_price
            
            # Create transaction record
            transaction = ShareTransaction(
                transaction_id=f"burn_{datetime.now().timestamp()}",
                from_address=from_address,
                to_address="0x0000000000000000000000000000000000000000",  # Zero address
                amount=amount,
                price=self.share_price,
                transaction_type="burn",
                timestamp=datetime.now()
            )
            
            self.share_transactions.append(transaction)
            
            result = {
                'status': 'success',
                'amount': amount,
                'new_circulating_supply': self.circulating_supply,
                'transaction_id': transaction.transaction_id
            }
            
            logger.info(f"Shares burned: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Share burning failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def update_share_price(self, new_price: float) -> Dict[str, Any]:
        """
        Update the current share price.
        
        Args:
            new_price: New price per share
            
        Returns:
            Price update results
        """
        try:
            logger.info(f"Updating share price from ${self.share_price} to ${new_price}...")
            
            old_price = self.share_price
            self.share_price = new_price
            self.market_cap = self.circulating_supply * new_price
            
            result = {
                'status': 'success',
                'old_price': old_price,
                'new_price': new_price,
                'price_change': new_price - old_price,
                'price_change_pct': ((new_price - old_price) / old_price) * 100,
                'new_market_cap': self.market_cap
            }
            
            logger.info(f"Share price updated: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Share price update failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_share_analytics(self) -> Dict[str, Any]:
        """
        Get share analytics and statistics.
        
        Returns:
            Share analytics data
        """
        # Calculate holder distribution
        holder_distribution = {}
        for share in self.fund_shares.values():
            if share.status == ShareStatus.ACTIVE:
                if share.owner_address in holder_distribution:
                    holder_distribution[share.owner_address] += share.amount
                else:
                    holder_distribution[share.owner_address] = share.amount
        
        # Calculate transaction statistics
        total_transactions = len(self.share_transactions)
        mint_transactions = len([t for t in self.share_transactions if t.transaction_type == "mint"])
        transfer_transactions = len([t for t in self.share_transactions if t.transaction_type == "transfer"])
        burn_transactions = len([t for t in self.share_transactions if t.transaction_type == "burn"])
        
        return {
            'total_supply': self.total_supply,
            'circulating_supply': self.circulating_supply,
            'burned_supply': self.total_supply - self.circulating_supply,
            'current_price': self.share_price,
            'market_cap': self.market_cap,
            'total_holders': len(holder_distribution),
            'holder_distribution': holder_distribution,
            'transaction_stats': {
                'total_transactions': total_transactions,
                'mint_transactions': mint_transactions,
                'transfer_transactions': transfer_transactions,
                'burn_transactions': burn_transactions
            },
            'recent_transactions': self.share_transactions[-10:] if self.share_transactions else []
        }
    
    def get_holder_balance(self, address: str) -> Dict[str, Any]:
        """
        Get share balance for a specific address.
        
        Args:
            address: Address to check balance for
            
        Returns:
            Holder balance information
        """
        holder_shares = [
            share for share in self.fund_shares.values()
            if share.owner_address == address and share.status == ShareStatus.ACTIVE
        ]
        
        total_amount = sum(share.amount for share in holder_shares)
        total_percentage = (total_amount / self.total_supply) * 100 if self.total_supply > 0 else 0
        total_value = total_amount * self.share_price
        
        return {
            'address': address,
            'total_shares': total_amount,
            'share_percentage': total_percentage,
            'total_value': total_value,
            'individual_shares': [
                {
                    'token_id': share.token_id,
                    'amount': share.amount,
                    'created_at': share.created_at,
                    'last_transfer': share.last_transfer
                }
                for share in holder_shares
            ]
        }
