"""Investor Portal API - RESTful API endpoints for investor dashboard and operations"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import uuid
import json

# Import our components
from ..auth.jwt_manager import JWTManager, UserRole, TokenType

logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter(prefix="/api/v1/investor", tags=["investor-portal"])
security = HTTPBearer()


class InvestmentRequest(BaseModel):
    """Request model for making an investment."""
    fund_id: str = Field(..., description="Fund ID to invest in")
    amount: float = Field(..., description="Investment amount", gt=0)
    investment_type: str = Field(default="lump_sum", description="Investment type")
    notes: Optional[str] = Field(None, description="Investment notes", max_length=500)


class WithdrawalRequest(BaseModel):
    """Request model for making a withdrawal."""
    fund_id: str = Field(..., description="Fund ID to withdraw from")
    amount: float = Field(..., description="Withdrawal amount", gt=0)
    withdrawal_type: str = Field(default="partial", description="Withdrawal type")
    notes: Optional[str] = Field(None, description="Withdrawal notes", max_length=500)


class DashboardResponse(BaseModel):
    """Response model for investor dashboard data."""
    investor_id: str
    total_investments: float
    total_withdrawals: float
    net_investment: float
    current_portfolio_value: float
    total_pnl: float
    total_return_percentage: float
    active_investments: int
    funds_invested: List[Dict[str, Any]]
    recent_transactions: List[Dict[str, Any]]
    performance_summary: Dict[str, Any]
    risk_metrics: Dict[str, Any]


class InvestmentResponse(BaseModel):
    """Response model for investment data."""
    investment_id: str
    fund_id: str
    fund_name: str
    amount: float
    investment_type: str
    status: str
    created_at: datetime
    notes: Optional[str]


class TransactionResponse(BaseModel):
    """Response model for transaction data."""
    transaction_id: str
    transaction_type: str
    fund_id: str
    fund_name: str
    amount: float
    status: str
    created_at: datetime
    notes: Optional[str]


class PortfolioSummaryResponse(BaseModel):
    """Response model for portfolio summary."""
    total_value: float
    total_invested: float
    total_pnl: float
    total_return_percentage: float
    daily_change: float
    daily_change_percentage: float
    asset_allocation: Dict[str, float]
    performance_metrics: Dict[str, Any]


class InvestorPortalAPI:
    """Investor portal API endpoints."""
    
    def __init__(self, database_manager, jwt_manager: JWTManager):
        self.database_manager = database_manager
        self.jwt_manager = jwt_manager
        
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
        """Get current authenticated user from token."""
        try:
            token = credentials.credentials
            payload = self.jwt_manager.verify_token(token, TokenType.ACCESS)
            
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Get user details from database
            user_query = """
            SELECT * FROM users WHERE id = :user_id
            """
            
            user_result = await self.database_manager.execute_query(
                user_query, 
                {"user_id": payload.user_id}
            )
            
            if 'error' in user_result or not user_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user_data = user_result['query_result']['data'][0]
            
            return {
                "user_id": user_data['id'],
                "username": user_data['username'],
                "email": user_data['email'],
                "role": payload.role,
                "permissions": payload.permissions,
                "is_active": user_data['is_active']
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get current user: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def _check_permission(self, user_permissions: List[str], required_permission: str) -> bool:
        """Check if user has required permission."""
        return self.jwt_manager.has_permission(user_permissions, required_permission)
    
    def _is_valid_uuid(self, uuid_string: str) -> bool:
        """Validate UUID format."""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False
    
    @router.get("/dashboard", response_model=DashboardResponse)
    async def get_investor_dashboard(
        self,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> DashboardResponse:
        """Get investor dashboard data."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "portfolio:read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to access investor dashboard"
                )
            
            investor_id = current_user['user_id']
            
            # Get total investments
            investments_query = """
            SELECT COALESCE(SUM(amount), 0) as total_investments
            FROM fund_investors 
            WHERE investor_id = :investor_id AND transaction_type = 'investment'
            """
            
            investments_result = await self.database_manager.execute_query(
                investments_query,
                {"investor_id": investor_id}
            )
            
            if 'error' in investments_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {investments_result['error']}"
                )
            
            total_investments = float(investments_result['query_result']['data'][0]['total_investments'])
            
            # Get total withdrawals
            withdrawals_query = """
            SELECT COALESCE(SUM(amount), 0) as total_withdrawals
            FROM fund_investors 
            WHERE investor_id = :investor_id AND transaction_type = 'withdrawal'
            """
            
            withdrawals_result = await self.database_manager.execute_query(
                withdrawals_query,
                {"investor_id": investor_id}
            )
            
            if 'error' in withdrawals_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {withdrawals_result['error']}"
                )
            
            total_withdrawals = float(withdrawals_result['query_result']['data'][0]['total_withdrawals'])
            net_investment = total_investments - total_withdrawals
            
            # Get current portfolio value
            portfolio_query = """
            SELECT 
                fi.fund_id,
                f.name as fund_name,
                fi.amount as invested_amount,
                f.current_value as fund_value,
                fi.amount * (f.current_value / f.initial_capital) as current_value
            FROM fund_investors fi
            JOIN funds f ON fi.fund_id = f.id
            WHERE fi.investor_id = :investor_id 
            AND fi.transaction_type = 'investment'
            """
            
            portfolio_result = await self.database_manager.execute_query(
                portfolio_query,
                {"investor_id": investor_id}
            )
            
            if 'error' in portfolio_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {portfolio_result['error']}"
                )
            
            current_portfolio_value = 0.0
            funds_invested = []
            active_investments = 0
            
            for row in portfolio_result['query_result']['data']:
                current_value = float(row['current_value'])
                invested_amount = float(row['invested_amount'])
                current_portfolio_value += current_value
                
                if invested_amount > 0:
                    active_investments += 1
                
                funds_invested.append({
                    "fund_id": row['fund_id'],
                    "fund_name": row['fund_name'],
                    "invested_amount": invested_amount,
                    "current_value": current_value,
                    "pnl": current_value - invested_amount,
                    "return_percentage": ((current_value - invested_amount) / invested_amount * 100) if invested_amount > 0 else 0
                })
            
            total_pnl = current_portfolio_value - net_investment
            total_return_percentage = (total_pnl / net_investment * 100) if net_investment > 0 else 0
            
            # Get recent transactions
            recent_transactions_query = """
            SELECT 
                fi.id as transaction_id,
                fi.transaction_type,
                fi.fund_id,
                f.name as fund_name,
                fi.amount,
                fi.status,
                fi.created_at,
                fi.notes
            FROM fund_investors fi
            JOIN funds f ON fi.fund_id = f.id
            WHERE fi.investor_id = :investor_id
            ORDER BY fi.created_at DESC
            LIMIT 10
            """
            
            recent_transactions_result = await self.database_manager.execute_query(
                recent_transactions_query,
                {"investor_id": investor_id}
            )
            
            if 'error' in recent_transactions_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {recent_transactions_result['error']}"
                )
            
            recent_transactions = []
            for row in recent_transactions_result['query_result']['data']:
                recent_transactions.append({
                    "transaction_id": row['transaction_id'],
                    "transaction_type": row['transaction_type'],
                    "fund_id": row['fund_id'],
                    "fund_name": row['fund_name'],
                    "amount": float(row['amount']),
                    "status": row['status'],
                    "created_at": row['created_at'].isoformat(),
                    "notes": row['notes']
                })
            
            # Calculate performance summary
            performance_summary = {
                "total_return": total_pnl,
                "total_return_percentage": total_return_percentage,
                "best_performing_fund": max(funds_invested, key=lambda x: x['return_percentage'])['fund_name'] if funds_invested else None,
                "worst_performing_fund": min(funds_invested, key=lambda x: x['return_percentage'])['fund_name'] if funds_invested else None,
                "average_return": sum(f['return_percentage'] for f in funds_invested) / len(funds_invested) if funds_invested else 0
            }
            
            # Calculate risk metrics
            risk_metrics = {
                "portfolio_volatility": 0.15,  # Placeholder - would calculate from historical data
                "max_drawdown": 0.08,  # Placeholder
                "sharpe_ratio": 1.2,  # Placeholder
                "beta": 0.85  # Placeholder
            }
            
            return DashboardResponse(
                investor_id=investor_id,
                total_investments=total_investments,
                total_withdrawals=total_withdrawals,
                net_investment=net_investment,
                current_portfolio_value=current_portfolio_value,
                total_pnl=total_pnl,
                total_return_percentage=total_return_percentage,
                active_investments=active_investments,
                funds_invested=funds_invested,
                recent_transactions=recent_transactions,
                performance_summary=performance_summary,
                risk_metrics=risk_metrics
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get investor dashboard: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.post("/invest", response_model=InvestmentResponse)
    async def make_investment(
        self,
        request: InvestmentRequest = ...,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> InvestmentResponse:
        """Make an investment in a fund."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "portfolio:update"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to make investments"
                )
            
            # Validate fund_id format
            if not self._is_valid_uuid(request.fund_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid fund ID format"
                )
            
            # Validate investment amount
            if request.amount <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Investment amount must be positive"
                )
            
            # Check if fund exists
            fund_query = "SELECT * FROM funds WHERE id = :fund_id"
            fund_result = await self.database_manager.execute_query(
                fund_query,
                {"fund_id": request.fund_id}
            )
            
            if 'error' in fund_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {fund_result['error']}"
                )
            
            if not fund_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Fund not found"
                )
            
            fund_data = fund_result['query_result']['data'][0]
            
            # Check if fund is accepting investments
            if not fund_data['is_active']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Fund is not currently accepting investments"
                )
            
            # Create investment record
            investment_id = str(uuid.uuid4())
            investment_query = """
            INSERT INTO fund_investors (
                id, fund_id, investor_id, amount, transaction_type, 
                status, notes, created_at, updated_at
            ) VALUES (
                :id, :fund_id, :investor_id, :amount, :transaction_type,
                :status, :notes, :created_at, :updated_at
            )
            """
            
            now = datetime.now()
            investment_params = {
                "id": investment_id,
                "fund_id": request.fund_id,
                "investor_id": current_user['user_id'],
                "amount": request.amount,
                "transaction_type": "investment",
                "status": "pending",
                "notes": request.notes,
                "created_at": now,
                "updated_at": now
            }
            
            investment_result = await self.database_manager.execute_query(investment_query, investment_params)
            
            if 'error' in investment_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to create investment: {investment_result['error']}"
                )
            
            # Update fund value (simplified - in production would be more complex)
            update_fund_query = """
            UPDATE funds 
            SET current_value = current_value + :amount, updated_at = :updated_at
            WHERE id = :fund_id
            """
            
            update_fund_params = {
                "fund_id": request.fund_id,
                "amount": request.amount,
                "updated_at": now
            }
            
            await self.database_manager.execute_query(update_fund_query, update_fund_params)
            
            logger.info(f"Investment created successfully: {request.amount} in fund {request.fund_id}")
            
            return InvestmentResponse(
                investment_id=investment_id,
                fund_id=request.fund_id,
                fund_name=fund_data['name'],
                amount=request.amount,
                investment_type=request.investment_type,
                status="pending",
                created_at=now,
                notes=request.notes
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to make investment: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.post("/withdraw", response_model=TransactionResponse)
    async def make_withdrawal(
        self,
        request: WithdrawalRequest = ...,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> TransactionResponse:
        """Make a withdrawal from a fund."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "portfolio:update"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to make withdrawals"
                )
            
            # Validate fund_id format
            if not self._is_valid_uuid(request.fund_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid fund ID format"
                )
            
            # Validate withdrawal amount
            if request.amount <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Withdrawal amount must be positive"
                )
            
            # Check if fund exists
            fund_query = "SELECT * FROM funds WHERE id = :fund_id"
            fund_result = await self.database_manager.execute_query(
                fund_query,
                {"fund_id": request.fund_id}
            )
            
            if 'error' in fund_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {fund_result['error']}"
                )
            
            if not fund_result['query_result']['data']:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Fund not found"
                )
            
            fund_data = fund_result['query_result']['data'][0]
            
            # Check investor's current investment in the fund
            investment_query = """
            SELECT COALESCE(SUM(amount), 0) as total_invested
            FROM fund_investors 
            WHERE fund_id = :fund_id AND investor_id = :investor_id AND transaction_type = 'investment'
            """
            
            investment_result = await self.database_manager.execute_query(
                investment_query,
                {"fund_id": request.fund_id, "investor_id": current_user['user_id']}
            )
            
            if 'error' in investment_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {investment_result['error']}"
                )
            
            total_invested = float(investment_result['query_result']['data'][0]['total_invested'])
            
            # Check if investor has enough invested
            if request.amount > total_invested:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient investment balance. Available: {total_invested}"
                )
            
            # Create withdrawal record
            withdrawal_id = str(uuid.uuid4())
            withdrawal_query = """
            INSERT INTO fund_investors (
                id, fund_id, investor_id, amount, transaction_type, 
                status, notes, created_at, updated_at
            ) VALUES (
                :id, :fund_id, :investor_id, :amount, :transaction_type,
                :status, :notes, :created_at, :updated_at
            )
            """
            
            now = datetime.now()
            withdrawal_params = {
                "id": withdrawal_id,
                "fund_id": request.fund_id,
                "investor_id": current_user['user_id'],
                "amount": request.amount,
                "transaction_type": "withdrawal",
                "status": "pending",
                "notes": request.notes,
                "created_at": now,
                "updated_at": now
            }
            
            withdrawal_result = await self.database_manager.execute_query(withdrawal_query, withdrawal_params)
            
            if 'error' in withdrawal_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to create withdrawal: {withdrawal_result['error']}"
                )
            
            # Update fund value (simplified - in production would be more complex)
            update_fund_query = """
            UPDATE funds 
            SET current_value = current_value - :amount, updated_at = :updated_at
            WHERE id = :fund_id
            """
            
            update_fund_params = {
                "fund_id": request.fund_id,
                "amount": request.amount,
                "updated_at": now
            }
            
            await self.database_manager.execute_query(update_fund_query, update_fund_params)
            
            logger.info(f"Withdrawal created successfully: {request.amount} from fund {request.fund_id}")
            
            return TransactionResponse(
                transaction_id=withdrawal_id,
                transaction_type="withdrawal",
                fund_id=request.fund_id,
                fund_name=fund_data['name'],
                amount=request.amount,
                status="pending",
                created_at=now,
                notes=request.notes
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to make withdrawal: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.get("/portfolio/summary", response_model=PortfolioSummaryResponse)
    async def get_portfolio_summary(
        self,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> PortfolioSummaryResponse:
        """Get portfolio summary for the investor."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "portfolio:read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to read portfolio"
                )
            
            investor_id = current_user['user_id']
            
            # Get portfolio data
            portfolio_query = """
            SELECT 
                fi.fund_id,
                f.name as fund_name,
                fi.amount as invested_amount,
                f.current_value as fund_value,
                f.initial_capital,
                fi.amount * (f.current_value / f.initial_capital) as current_value
            FROM fund_investors fi
            JOIN funds f ON fi.fund_id = f.id
            WHERE fi.investor_id = :investor_id 
            AND fi.transaction_type = 'investment'
            """
            
            portfolio_result = await self.database_manager.execute_query(
                portfolio_query,
                {"investor_id": investor_id}
            )
            
            if 'error' in portfolio_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {portfolio_result['error']}"
                )
            
            total_value = 0.0
            total_invested = 0.0
            asset_allocation = {}
            
            for row in portfolio_result['query_result']['data']:
                current_value = float(row['current_value'])
                invested_amount = float(row['invested_amount'])
                fund_name = row['fund_name']
                
                total_value += current_value
                total_invested += invested_amount
                asset_allocation[fund_name] = current_value
            
            # Normalize asset allocation to percentages
            if total_value > 0:
                asset_allocation = {k: (v / total_value * 100) for k, v in asset_allocation.items()}
            
            total_pnl = total_value - total_invested
            total_return_percentage = (total_pnl / total_invested * 100) if total_invested > 0 else 0
            
            # Calculate daily change (placeholder - would use historical data)
            daily_change = total_pnl * 0.01  # 1% of total PnL as placeholder
            daily_change_percentage = (daily_change / total_value * 100) if total_value > 0 else 0
            
            # Performance metrics
            performance_metrics = {
                "sharpe_ratio": 1.2,  # Placeholder
                "max_drawdown": 0.08,  # Placeholder
                "volatility": 0.15,  # Placeholder
                "beta": 0.85,  # Placeholder
                "alpha": 0.02  # Placeholder
            }
            
            return PortfolioSummaryResponse(
                total_value=total_value,
                total_invested=total_invested,
                total_pnl=total_pnl,
                total_return_percentage=total_return_percentage,
                daily_change=daily_change,
                daily_change_percentage=daily_change_percentage,
                asset_allocation=asset_allocation,
                performance_metrics=performance_metrics
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get portfolio summary: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @router.get("/transactions")
    async def get_transaction_history(
        self,
        page: int = Query(1, description="Page number", ge=1),
        page_size: int = Query(20, description="Page size", ge=1, le=100),
        transaction_type: Optional[str] = Query(None, description="Filter by transaction type"),
        fund_id: Optional[str] = Query(None, description="Filter by fund ID"),
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Get transaction history for the investor."""
        try:
            # Check permission
            if not self._check_permission(current_user['permissions'], "portfolio:read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to read transaction history"
                )
            
            investor_id = current_user['user_id']
            
            # Build query with filters
            where_conditions = ["fi.investor_id = :investor_id"]
            params = {"investor_id": investor_id}
            
            if transaction_type:
                where_conditions.append("fi.transaction_type = :transaction_type")
                params["transaction_type"] = transaction_type
            
            if fund_id:
                where_conditions.append("fi.fund_id = :fund_id")
                params["fund_id"] = fund_id
            
            where_clause = "WHERE " + " AND ".join(where_conditions)
            
            # Get total count
            count_query = f"""
            SELECT COUNT(*) as total 
            FROM fund_investors fi
            JOIN funds f ON fi.fund_id = f.id
            {where_clause}
            """
            count_result = await self.database_manager.execute_query(count_query, params)
            
            if 'error' in count_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {count_result['error']}"
                )
            
            total_count = count_result['query_result']['data'][0]['total']
            total_pages = (total_count + page_size - 1) // page_size
            
            # Get transactions with pagination
            offset = (page - 1) * page_size
            params["limit"] = page_size
            params["offset"] = offset
            
            transactions_query = f"""
            SELECT 
                fi.id as transaction_id,
                fi.transaction_type,
                fi.fund_id,
                f.name as fund_name,
                fi.amount,
                fi.status,
                fi.created_at,
                fi.notes
            FROM fund_investors fi
            JOIN funds f ON fi.fund_id = f.id
            {where_clause}
            ORDER BY fi.created_at DESC
            LIMIT :limit OFFSET :offset
            """
            
            transactions_result = await self.database_manager.execute_query(transactions_query, params)
            
            if 'error' in transactions_result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error: {transactions_result['error']}"
                )
            
            transactions = []
            for row in transactions_result['query_result']['data']:
                transactions.append({
                    "transaction_id": row['transaction_id'],
                    "transaction_type": row['transaction_type'],
                    "fund_id": row['fund_id'],
                    "fund_name": row['fund_name'],
                    "amount": float(row['amount']),
                    "status": row['status'],
                    "created_at": row['created_at'].isoformat(),
                    "notes": row['notes']
                })
            
            return {
                "transactions": transactions,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get transaction history: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


# Create router instance
def create_investor_portal_api_router(database_manager, jwt_manager: JWTManager) -> APIRouter:
    """Create and configure the investor portal API router."""
    api = InvestorPortalAPI(database_manager, jwt_manager)
    
    # Add the router methods to the router
    router.add_api_route("/dashboard", api.get_investor_dashboard, methods=["GET"])
    router.add_api_route("/invest", api.make_investment, methods=["POST"])
    router.add_api_route("/withdraw", api.make_withdrawal, methods=["POST"])
    router.add_api_route("/portfolio/summary", api.get_portfolio_summary, methods=["GET"])
    router.add_api_route("/transactions", api.get_transaction_history, methods=["GET"])
    
    return router
