"""
Blockchain Integration Module

This module provides blockchain-native features including:
- Multi-chain management and integration
- Tokenization system for fund shares
- DAO governance for decentralized management
- Smart contract automation
"""

from .multi_chain_manager import MultiChainManager
from .tokenization_system import TokenizationSystem
from .dao_governance import DAOGovernance

__all__ = [
    "MultiChainManager",
    "TokenizationSystem", 
    "DAOGovernance"
]
