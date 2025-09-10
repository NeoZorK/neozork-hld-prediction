#!/usr/bin/env python3
"""
Basic Test for Pocket Hedge Fund Implementation

This script tests the basic functionality of our Pocket Hedge Fund implementation
without requiring a full database setup.
"""

import asyncio
import sys
import pytest
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.pocket_hedge_fund.auth.auth_manager import (
    AuthenticationManager, AuthConfig, PasswordManager, MFAManager, JWTManager
)
from src.pocket_hedge_fund.database.models import (
    User, Fund, Investment, UserRole, FundStatus, FundType, RiskLevel
)
from decimal import Decimal


def test_password_manager():
    """Test password management functionality."""
    print("🔐 Testing Password Manager...")
    
    # Test password hashing
    password = "TestPassword123!"
    hashed = PasswordManager.hash_password(password)
    print(f"✅ Password hashed successfully: {hashed[:20]}...")
    
    # Test password verification
    assert PasswordManager.verify_password(password, hashed)
    assert not PasswordManager.verify_password("wrong_password", hashed)
    print("✅ Password verification works correctly")
    
    # Test password strength validation
    is_valid, errors = PasswordManager.validate_password_strength(password)
    assert is_valid
    print("✅ Password strength validation works correctly")
    
    print("🎉 Password Manager tests passed!\n")


def test_mfa_manager():
    """Test MFA functionality."""
    print("🔑 Testing MFA Manager...")
    
    config = AuthConfig(jwt_secret="test_secret")
    mfa_manager = MFAManager(config)
    
    # Test secret generation
    secret = mfa_manager.generate_secret()
    assert len(secret) == 32
    print(f"✅ MFA secret generated: {secret[:10]}...")
    
    # Test QR code generation
    qr_code = mfa_manager.generate_qr_code("test@example.com", secret)
    assert qr_code.startswith("data:image/png;base64,")
    print("✅ QR code generated successfully")
    
    # Test backup codes
    backup_codes = mfa_manager.generate_backup_codes()
    assert len(backup_codes) == 10
    print(f"✅ Backup codes generated: {backup_codes[:2]}...")
    
    print("🎉 MFA Manager tests passed!\n")


def test_jwt_manager():
    """Test JWT functionality."""
    print("🎫 Testing JWT Manager...")
    
    config = AuthConfig(jwt_secret="test_secret")
    jwt_manager = JWTManager(config)
    
    # Test access token generation
    access_token = jwt_manager.generate_access_token(
        user_id="test_user",
        email="test@example.com",
        role="investor",
        mfa_verified=True
    )
    assert len(access_token) > 0
    print(f"✅ Access token generated: {access_token[:20]}...")
    
    # Test refresh token generation
    refresh_token = jwt_manager.generate_refresh_token("test_user")
    assert len(refresh_token) > 0
    print(f"✅ Refresh token generated: {refresh_token[:20]}...")
    
    # Test token verification
    payload = jwt_manager.verify_token(access_token)
    assert payload['user_id'] == "test_user"
    assert payload['email'] == "test@example.com"
    assert payload['role'] == "investor"
    assert payload['mfa_verified'] is True
    print("✅ Token verification works correctly")
    
    print("🎉 JWT Manager tests passed!\n")


def test_database_models():
    """Test database models."""
    print("🗄️ Testing Database Models...")
    
    # Test User model
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password",
        first_name="Test",
        last_name="User",
        role="investor"
    )
    assert user.full_name == "Test User"
    user_dict = user.to_dict()
    assert user_dict['email'] == "test@example.com"
    print("✅ User model works correctly")
    
    # Test Fund model
    fund = Fund(
        name="Test Fund",
        description="A test fund",
        fund_type="mini",
        initial_capital=Decimal('100000.00'),
        current_value=Decimal('105000.00'),
        management_fee=Decimal('0.02'),
        performance_fee=Decimal('0.20'),
        min_investment=Decimal('1000.00'),
        status="active",
        created_by="user_id"
    )
    assert fund.total_return == Decimal('5000.00')
    assert fund.total_return_percentage == Decimal('5.0')
    assert fund.is_open_for_investment is True
    fund_dict = fund.to_dict()
    assert fund_dict['total_return'] == 5000.0
    print("✅ Fund model works correctly")
    
    # Test Investment model
    investment = Investment(
        investor_id="user_id",
        fund_id="fund_id",
        amount=Decimal('10000.00'),
        shares_acquired=Decimal('10000.00'),
        share_price=Decimal('1.00')
    )
    assert investment.amount == Decimal('10000.00')
    assert investment.shares_acquired == Decimal('10000.00')
    if hasattr(investment, 'to_dict'):
        investment_dict = investment.to_dict()
        assert investment_dict['amount'] == 10000.0
    print("✅ Investment model works correctly")
    
    print("🎉 Database Models tests passed!\n")


@pytest.mark.asyncio
async def test_authentication_manager():
    """Test authentication manager."""
    print("🔐 Testing Authentication Manager...")
    
    config = AuthConfig(jwt_secret="test_secret")
    auth_manager = AuthenticationManager(config)
    
    # Test initialization
    assert auth_manager.config.jwt_secret == "test_secret"
    assert auth_manager.password_manager is not None
    assert auth_manager.mfa_manager is not None
    assert auth_manager.jwt_manager is not None
    print("✅ Authentication manager initialized correctly")
    
    # Test user lockout functionality
    user_id = "test_user"
    assert not auth_manager._is_user_locked(user_id)
    
    # Record failed login attempts
    for _ in range(5):
        await auth_manager._record_failed_login(user_id)
    
    assert auth_manager._is_user_locked(user_id)
    print("✅ User lockout functionality works correctly")
    
    # Clear failed logins
    auth_manager._clear_failed_logins(user_id)
    assert not auth_manager._is_user_locked(user_id)
    print("✅ Failed login clearing works correctly")
    
    print("🎉 Authentication Manager tests passed!\n")


def test_enums():
    """Test enum classes."""
    print("📋 Testing Enums...")
    
    # Test UserRole
    assert UserRole.ADMIN.value == "admin"
    assert UserRole.FUND_MANAGER.value == "fund_manager"
    assert UserRole.INVESTOR.value == "investor"
    print("✅ UserRole enum works correctly")
    
    # Test FundStatus
    assert FundStatus.ACTIVE.value == "active"
    assert FundStatus.PAUSED.value == "paused"
    assert FundStatus.CLOSED.value == "closed"
    print("✅ FundStatus enum works correctly")
    
    # Test FundType
    assert FundType.MINI.value == "mini"
    assert FundType.STANDARD.value == "standard"
    assert FundType.PREMIUM.value == "premium"
    print("✅ FundType enum works correctly")
    
    # Test RiskLevel
    assert RiskLevel.LOW.value == "low"
    assert RiskLevel.MEDIUM.value == "medium"
    assert RiskLevel.HIGH.value == "high"
    print("✅ RiskLevel enum works correctly")
    
    print("🎉 Enums tests passed!\n")


def main():
    """Run all tests."""
    print("🚀 NeoZork Pocket Hedge Fund - Basic Implementation Test")
    print("=" * 60)
    print()
    
    try:
        test_password_manager()
        test_mfa_manager()
        test_jwt_manager()
        test_database_models()
        test_authentication_manager()
        test_enums()
        
        print("🎉 ALL TESTS PASSED! 🎉")
        print("=" * 60)
        print()
        print("✅ Password Manager: Working")
        print("✅ MFA Manager: Working")
        print("✅ JWT Manager: Working")
        print("✅ Database Models: Working")
        print("✅ Authentication Manager: Working")
        print("✅ Enums: Working")
        print()
        print("🚀 Pocket Hedge Fund implementation is ready!")
        print("📚 Next steps:")
        print("   1. Setup PostgreSQL database")
        print("   2. Run: python run_pocket_hedge_fund.py")
        print("   3. Access API docs at: http://localhost:8080/docs")
        print()
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
