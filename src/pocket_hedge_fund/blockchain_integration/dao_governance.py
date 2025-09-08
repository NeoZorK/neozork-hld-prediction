"""DAO Governance - Decentralized governance and voting system"""

import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid
import json

logger = logging.getLogger(__name__)


class ProposalType(Enum):
    """Proposal type enumeration."""
    FUND_MANAGEMENT = "fund_management"
    FEE_CHANGE = "fee_change"
    STRATEGY_APPROVAL = "strategy_approval"
    EMERGENCY_ACTION = "emergency_action"
    GOVERNANCE_CHANGE = "governance_change"
    TREASURY_MANAGEMENT = "treasury_management"


class ProposalStatus(Enum):
    """Proposal status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    SUCCEEDED = "succeeded"
    DEFEATED = "defeated"
    EXECUTED = "executed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class VoteType(Enum):
    """Vote type enumeration."""
    FOR = "for"
    AGAINST = "against"
    ABSTAIN = "abstain"


class GovernanceRole(Enum):
    """Governance role enumeration."""
    MEMBER = "member"
    DELEGATE = "delegate"
    MODERATOR = "moderator"
    ADMIN = "admin"


@dataclass
class GovernanceProposal:
    """Governance proposal data class."""
    proposal_id: str
    title: str
    description: str
    proposal_type: ProposalType
    proposer_address: str
    status: ProposalStatus
    voting_power_required: float
    voting_duration: int  # hours
    created_at: datetime
    voting_start: datetime
    voting_end: datetime
    execution_delay: int  # hours
    execution_data: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class Vote:
    """Vote data class."""
    vote_id: str
    proposal_id: str
    voter_address: str
    vote_type: VoteType
    voting_power: float
    cast_at: datetime
    transaction_hash: str
    metadata: Dict[str, Any]


@dataclass
class GovernanceMember:
    """Governance member data class."""
    member_id: str
    wallet_address: str
    role: GovernanceRole
    voting_power: float
    delegated_voting_power: float
    joined_at: datetime
    last_activity: datetime
    is_active: bool


class DAOGovernance:
    """Decentralized governance and voting system."""
    
    def __init__(self):
        self.proposals: Dict[str, GovernanceProposal] = {}
        self.votes: Dict[str, List[Vote]] = {}
        self.members: Dict[str, GovernanceMember] = {}
        self.delegations: Dict[str, Dict[str, float]] = {}  # delegator -> delegate -> amount
        self.execution_queue: List[Dict[str, Any]] = []
        self.governance_config: Dict[str, Any] = {}
        
        # Initialize governance components
        self._initialize_governance_components()
        
    def _initialize_governance_components(self):
        """Initialize governance system components."""
        # Set default governance configuration
        self.governance_config = {
            'min_proposal_deposit': 1000.0,  # Minimum tokens required to create proposal
            'voting_duration_hours': 72,  # Default voting duration
            'execution_delay_hours': 24,  # Delay before execution after voting ends
            'quorum_percentage': 0.05,  # 5% of total voting power required
            'majority_threshold': 0.5,  # 50% majority required
            'emergency_threshold': 0.75,  # 75% required for emergency actions
            'max_proposal_description_length': 10000,
            'max_active_proposals': 10
        }
        
    async def create_proposal(self, proposer_address: str, title: str, description: str,
                            proposal_type: ProposalType, execution_data: Dict[str, Any],
                            voting_duration_hours: int = None) -> Dict[str, Any]:
        """Create a new governance proposal."""
        try:
            # Validate proposer
            if proposer_address not in self.members:
                return {'error': 'Proposer is not a governance member'}
            
            proposer = self.members[proposer_address]
            if not proposer.is_active:
                return {'error': 'Proposer is not active'}
            
            # Check proposal deposit requirement
            deposit_required = self.governance_config['min_proposal_deposit']
            if proposer.voting_power < deposit_required:
                return {'error': f'Insufficient voting power. Required: {deposit_required}'}
            
            # Check active proposal limit
            active_proposals = len([p for p in self.proposals.values() 
                                  if p.status == ProposalStatus.ACTIVE])
            if active_proposals >= self.governance_config['max_active_proposals']:
                return {'error': 'Maximum number of active proposals reached'}
            
            # Validate proposal data
            validation_result = await self._validate_proposal_data(title, description, execution_data)
            if not validation_result['valid']:
                return {'error': f'Invalid proposal data: {validation_result["error"]}'}
            
            # Create proposal
            proposal_id = str(uuid.uuid4())
            voting_duration = voting_duration_hours or self.governance_config['voting_duration_hours']
            
            proposal = GovernanceProposal(
                proposal_id=proposal_id,
                title=title,
                description=description,
                proposal_type=proposal_type,
                proposer_address=proposer_address,
                status=ProposalStatus.DRAFT,
                voting_power_required=self._calculate_voting_power_required(proposal_type),
                voting_duration=voting_duration,
                created_at=datetime.now(),
                voting_start=datetime.now() + timedelta(hours=1),  # 1 hour delay before voting starts
                voting_end=datetime.now() + timedelta(hours=voting_duration + 1),
                execution_delay=self.governance_config['execution_delay_hours'],
                execution_data=execution_data,
                metadata={}
            )
            
            # Store proposal
            self.proposals[proposal_id] = proposal
            self.votes[proposal_id] = []
            
            logger.info(f"Created proposal {proposal_id}: {title}")
            return {
                'status': 'success',
                'proposal_id': proposal_id,
                'proposal': proposal.__dict__,
                'voting_starts_at': proposal.voting_start,
                'voting_ends_at': proposal.voting_end
            }
            
        except Exception as e:
            logger.error(f"Failed to create proposal: {e}")
            return {'error': str(e)}
    
    async def cast_vote(self, proposal_id: str, voter_address: str, 
                       vote_type: VoteType, voting_power: float = None) -> Dict[str, Any]:
        """Cast a vote on a proposal."""
        try:
            # Validate proposal exists
            if proposal_id not in self.proposals:
                return {'error': 'Proposal not found'}
            
            proposal = self.proposals[proposal_id]
            
            # Check if proposal is in voting period
            now = datetime.now()
            if now < proposal.voting_start:
                return {'error': 'Voting has not started yet'}
            if now > proposal.voting_end:
                return {'error': 'Voting period has ended'}
            if proposal.status != ProposalStatus.ACTIVE:
                return {'error': 'Proposal is not active for voting'}
            
            # Validate voter
            if voter_address not in self.members:
                return {'error': 'Voter is not a governance member'}
            
            voter = self.members[voter_address]
            if not voter.is_active:
                return {'error': 'Voter is not active'}
            
            # Check if voter has already voted
            existing_votes = self.votes.get(proposal_id, [])
            for vote in existing_votes:
                if vote.voter_address == voter_address:
                    return {'error': 'Voter has already cast a vote on this proposal'}
            
            # Calculate voting power
            if voting_power is None:
                voting_power = await self._calculate_voter_power(voter_address, proposal_id)
            
            if voting_power <= 0:
                return {'error': 'Voter has no voting power'}
            
            # Create vote
            vote_id = str(uuid.uuid4())
            vote = Vote(
                vote_id=vote_id,
                proposal_id=proposal_id,
                voter_address=voter_address,
                vote_type=vote_type,
                voting_power=voting_power,
                cast_at=datetime.now(),
                transaction_hash=f'0x{str(uuid.uuid4()).replace("-", "")}',
                metadata={}
            )
            
            # Store vote
            self.votes[proposal_id].append(vote)
            
            logger.info(f"Vote cast on proposal {proposal_id}: {vote_type.value} with {voting_power} power")
            return {
                'status': 'success',
                'vote_id': vote_id,
                'proposal_id': proposal_id,
                'voter_address': voter_address,
                'vote_type': vote_type.value,
                'voting_power': voting_power,
                'vote': vote.__dict__
            }
            
        except Exception as e:
            logger.error(f"Failed to cast vote: {e}")
            return {'error': str(e)}
    
    async def execute_proposal(self, proposal_id: str, executor_address: str) -> Dict[str, Any]:
        """Execute a successful proposal."""
        try:
            # Validate proposal exists
            if proposal_id not in self.proposals:
                return {'error': 'Proposal not found'}
            
            proposal = self.proposals[proposal_id]
            
            # Check if proposal can be executed
            if proposal.status != ProposalStatus.SUCCEEDED:
                return {'error': 'Proposal has not succeeded and cannot be executed'}
            
            # Check execution delay
            execution_time = proposal.voting_end + timedelta(hours=proposal.execution_delay)
            if datetime.now() < execution_time:
                return {'error': f'Execution delay not met. Can execute after {execution_time}'}
            
            # Validate executor
            if executor_address not in self.members:
                return {'error': 'Executor is not a governance member'}
            
            executor = self.members[executor_address]
            if not executor.is_active:
                return {'error': 'Executor is not active'}
            
            # Execute proposal based on type
            execution_result = await self._execute_proposal_action(proposal)
            if 'error' in execution_result:
                return execution_result
            
            # Update proposal status
            proposal.status = ProposalStatus.EXECUTED
            proposal.metadata['executed_at'] = datetime.now()
            proposal.metadata['executor'] = executor_address
            
            logger.info(f"Executed proposal {proposal_id}: {proposal.title}")
            return {
                'status': 'success',
                'proposal_id': proposal_id,
                'execution_result': execution_result,
                'executed_at': datetime.now(),
                'executor': executor_address
            }
            
        except Exception as e:
            logger.error(f"Failed to execute proposal: {e}")
            return {'error': str(e)}
    
    async def delegate_voting_power(self, delegator_address: str, delegate_address: str, 
                                  amount: float) -> Dict[str, Any]:
        """Delegate voting power to another member."""
        try:
            # Validate delegator
            if delegator_address not in self.members:
                return {'error': 'Delegator is not a governance member'}
            
            delegator = self.members[delegator_address]
            if not delegator.is_active:
                return {'error': 'Delegator is not active'}
            
            # Validate delegate
            if delegate_address not in self.members:
                return {'error': 'Delegate is not a governance member'}
            
            delegate = self.members[delegate_address]
            if not delegate.is_active:
                return {'error': 'Delegate is not active'}
            
            # Check delegation amount
            if amount <= 0:
                return {'error': 'Delegation amount must be positive'}
            
            if amount > delegator.voting_power:
                return {'error': 'Insufficient voting power to delegate'}
            
            # Update delegation
            if delegator_address not in self.delegations:
                self.delegations[delegator_address] = {}
            
            self.delegations[delegator_address][delegate_address] = amount
            
            # Update member voting powers
            delegator.voting_power -= amount
            delegate.delegated_voting_power += amount
            
            logger.info(f"Delegated {amount} voting power from {delegator_address} to {delegate_address}")
            return {
                'status': 'success',
                'delegator_address': delegator_address,
                'delegate_address': delegate_address,
                'amount': amount,
                'delegated_at': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Failed to delegate voting power: {e}")
            return {'error': str(e)}
    
    async def get_proposal_status(self, proposal_id: str) -> Dict[str, Any]:
        """Get detailed proposal status and voting results."""
        try:
            # Validate proposal exists
            if proposal_id not in self.proposals:
                return {'error': 'Proposal not found'}
            
            proposal = self.proposals[proposal_id]
            votes = self.votes.get(proposal_id, [])
            
            # Calculate voting results
            total_votes = len(votes)
            for_votes = sum(v.voting_power for v in votes if v.vote_type == VoteType.FOR)
            against_votes = sum(v.voting_power for v in votes if v.vote_type == VoteType.AGAINST)
            abstain_votes = sum(v.voting_power for v in votes if v.vote_type == VoteType.ABSTAIN)
            total_voting_power = for_votes + against_votes + abstain_votes
            
            # Calculate percentages
            total_members = len([m for m in self.members.values() if m.is_active])
            quorum_percentage = (total_voting_power / max(total_members, 1)) * 100
            
            # Determine if proposal succeeded
            quorum_met = quorum_percentage >= (self.governance_config['quorum_percentage'] * 100)
            majority_met = for_votes > against_votes if total_voting_power > 0 else False
            
            # Update proposal status if voting has ended
            if datetime.now() > proposal.voting_end and proposal.status == ProposalStatus.ACTIVE:
                if quorum_met and majority_met:
                    proposal.status = ProposalStatus.SUCCEEDED
                else:
                    proposal.status = ProposalStatus.DEFEATED
            
            return {
                'status': 'success',
                'proposal': proposal.__dict__,
                'voting_results': {
                    'total_votes': total_votes,
                    'for_votes': for_votes,
                    'against_votes': against_votes,
                    'abstain_votes': abstain_votes,
                    'total_voting_power': total_voting_power,
                    'quorum_percentage': quorum_percentage,
                    'quorum_met': quorum_met,
                    'majority_met': majority_met,
                    'proposal_succeeded': quorum_met and majority_met
                },
                'votes': [vote.__dict__ for vote in votes]
            }
            
        except Exception as e:
            logger.error(f"Failed to get proposal status: {e}")
            return {'error': str(e)}
    
    async def get_governance_members(self, limit: int = 100) -> Dict[str, Any]:
        """Get list of governance members."""
        try:
            members = list(self.members.values())
            
            # Sort by voting power (descending)
            members.sort(key=lambda x: x.voting_power + x.delegated_voting_power, reverse=True)
            
            # Apply limit
            members = members[:limit]
            
            return {
                'status': 'success',
                'members': [member.__dict__ for member in members],
                'total_members': len(self.members),
                'active_members': len([m for m in self.members.values() if m.is_active]),
                'returned_count': len(members)
            }
            
        except Exception as e:
            logger.error(f"Failed to get governance members: {e}")
            return {'error': str(e)}
    
    async def _validate_proposal_data(self, title: str, description: str, 
                                    execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate proposal data."""
        try:
            # Check title length
            if len(title) < 10 or len(title) > 200:
                return {'valid': False, 'error': 'Title must be between 10 and 200 characters'}
            
            # Check description length
            max_desc_length = self.governance_config['max_proposal_description_length']
            if len(description) < 50 or len(description) > max_desc_length:
                return {'valid': False, 'error': f'Description must be between 50 and {max_desc_length} characters'}
            
            # Validate execution data
            if not execution_data:
                return {'valid': False, 'error': 'Execution data is required'}
            
            return {'valid': True, 'error': None}
            
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def _calculate_voting_power_required(self, proposal_type: ProposalType) -> float:
        """Calculate voting power required for proposal type."""
        try:
            # Different proposal types may require different thresholds
            thresholds = {
                ProposalType.FUND_MANAGEMENT: 0.1,  # 10% of total voting power
                ProposalType.FEE_CHANGE: 0.15,  # 15% of total voting power
                ProposalType.STRATEGY_APPROVAL: 0.05,  # 5% of total voting power
                ProposalType.EMERGENCY_ACTION: 0.25,  # 25% of total voting power
                ProposalType.GOVERNANCE_CHANGE: 0.2,  # 20% of total voting power
                ProposalType.TREASURY_MANAGEMENT: 0.15  # 15% of total voting power
            }
            
            return thresholds.get(proposal_type, 0.1)
            
        except Exception as e:
            logger.error(f"Failed to calculate voting power required: {e}")
            return 0.1
    
    async def _calculate_voter_power(self, voter_address: str, proposal_id: str) -> float:
        """Calculate voting power for a voter."""
        try:
            if voter_address not in self.members:
                return 0.0
            
            member = self.members[voter_address]
            
            # Base voting power from member's tokens
            base_power = member.voting_power
            
            # Add delegated voting power
            delegated_power = 0.0
            for delegator, delegations in self.delegations.items():
                if voter_address in delegations:
                    delegated_power += delegations[voter_address]
            
            return base_power + delegated_power
            
        except Exception as e:
            logger.error(f"Failed to calculate voter power: {e}")
            return 0.0
    
    async def _execute_proposal_action(self, proposal: GovernanceProposal) -> Dict[str, Any]:
        """Execute the action specified in the proposal."""
        try:
            execution_data = proposal.execution_data
            proposal_type = proposal.proposal_type
            
            if proposal_type == ProposalType.FUND_MANAGEMENT:
                return await self._execute_fund_management_action(execution_data)
            elif proposal_type == ProposalType.FEE_CHANGE:
                return await self._execute_fee_change_action(execution_data)
            elif proposal_type == ProposalType.STRATEGY_APPROVAL:
                return await self._execute_strategy_approval_action(execution_data)
            elif proposal_type == ProposalType.EMERGENCY_ACTION:
                return await self._execute_emergency_action(execution_data)
            elif proposal_type == ProposalType.GOVERNANCE_CHANGE:
                return await self._execute_governance_change_action(execution_data)
            elif proposal_type == ProposalType.TREASURY_MANAGEMENT:
                return await self._execute_treasury_management_action(execution_data)
            else:
                return {'error': f'Unknown proposal type: {proposal_type.value}'}
                
        except Exception as e:
            logger.error(f"Failed to execute proposal action: {e}")
            return {'error': str(e)}
    
    async def _execute_fund_management_action(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute fund management action."""
        try:
            # TODO: Implement fund management actions
            # This would execute actions like changing fund parameters, etc.
            
            return {
                'status': 'success',
                'action_type': 'fund_management',
                'executed_at': datetime.now()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _execute_fee_change_action(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute fee change action."""
        try:
            # TODO: Implement fee change actions
            # This would change fund fees, management fees, etc.
            
            return {
                'status': 'success',
                'action_type': 'fee_change',
                'executed_at': datetime.now()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _execute_strategy_approval_action(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute strategy approval action."""
        try:
            # TODO: Implement strategy approval actions
            # This would approve or reject trading strategies
            
            return {
                'status': 'success',
                'action_type': 'strategy_approval',
                'executed_at': datetime.now()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _execute_emergency_action(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute emergency action."""
        try:
            # TODO: Implement emergency actions
            # This would execute emergency measures like pausing trading, etc.
            
            return {
                'status': 'success',
                'action_type': 'emergency_action',
                'executed_at': datetime.now()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _execute_governance_change_action(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute governance change action."""
        try:
            # TODO: Implement governance change actions
            # This would change governance parameters, voting rules, etc.
            
            return {
                'status': 'success',
                'action_type': 'governance_change',
                'executed_at': datetime.now()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _execute_treasury_management_action(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute treasury management action."""
        try:
            # TODO: Implement treasury management actions
            # This would manage fund treasury, distributions, etc.
            
            return {
                'status': 'success',
                'action_type': 'treasury_management',
                'executed_at': datetime.now()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_governance_summary(self) -> Dict[str, Any]:
        """Get governance system summary."""
        total_proposals = len(self.proposals)
        active_proposals = len([p for p in self.proposals.values() if p.status == ProposalStatus.ACTIVE])
        succeeded_proposals = len([p for p in self.proposals.values() if p.status == ProposalStatus.SUCCEEDED])
        total_members = len(self.members)
        active_members = len([m for m in self.members.values() if m.is_active])
        total_votes = sum(len(votes) for votes in self.votes.values())
        
        return {
            'total_proposals': total_proposals,
            'active_proposals': active_proposals,
            'succeeded_proposals': succeeded_proposals,
            'total_members': total_members,
            'active_members': active_members,
            'total_votes': total_votes,
            'governance_config': self.governance_config
        }