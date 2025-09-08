"""
DAO Governance System

This module provides decentralized governance capabilities including:
- Investor voting on fund decisions
- Strategy approval and management
- Parameter changes and updates
- Emergency controls and safeguards
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio

logger = logging.getLogger(__name__)


class ProposalType(Enum):
    """Proposal types."""
    STRATEGY_CHANGE = "strategy_change"
    PARAMETER_UPDATE = "parameter_update"
    FEE_CHANGE = "fee_change"
    EMERGENCY_ACTION = "emergency_action"
    FUND_MANAGER_CHANGE = "fund_manager_change"
    WITHDRAWAL = "withdrawal"


class ProposalStatus(Enum):
    """Proposal status types."""
    DRAFT = "draft"
    ACTIVE = "active"
    PASSED = "passed"
    REJECTED = "rejected"
    EXECUTED = "executed"
    EXPIRED = "expired"


class VoteType(Enum):
    """Vote types."""
    YES = "yes"
    NO = "no"
    ABSTAIN = "abstain"


@dataclass
class Proposal:
    """Governance proposal data."""
    proposal_id: str
    title: str
    description: str
    proposal_type: ProposalType
    proposer: str
    created_at: datetime
    voting_start: datetime
    voting_end: datetime
    status: ProposalStatus
    votes_for: int = 0
    votes_against: int = 0
    votes_abstain: int = 0
    total_votes: int = 0
    quorum_threshold: float = 0.1  # 10% of total shares
    majority_threshold: float = 0.5  # 50% of votes
    execution_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Vote:
    """Vote data."""
    vote_id: str
    proposal_id: str
    voter: str
    vote_type: VoteType
    voting_power: float
    timestamp: datetime
    transaction_hash: Optional[str] = None


class DAOGovernance:
    """
    DAO Governance System for decentralized fund management.
    
    This system provides governance capabilities allowing investors to vote
    on fund decisions, strategy changes, and parameter updates.
    """
    
    def __init__(self):
        self.proposals = {}
        self.votes = {}
        self.voting_power = {}  # Address -> voting power
        self.governance_parameters = {
            'proposal_duration': 7,  # days
            'quorum_threshold': 0.1,  # 10% of total shares
            'majority_threshold': 0.5,  # 50% of votes
            'min_proposal_amount': 1000,  # minimum shares to create proposal
            'execution_delay': 1  # days delay before execution
        }
    
    async def create_proposal(self, proposer: str, title: str, description: str,
                            proposal_type: ProposalType, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new governance proposal.
        
        Args:
            proposer: Address of the proposer
            title: Proposal title
            description: Proposal description
            proposal_type: Type of proposal
            execution_data: Data needed for proposal execution
            
        Returns:
            Proposal creation results
        """
        try:
            logger.info(f"Creating proposal: {title}")
            
            # Check if proposer has enough voting power
            proposer_power = self.voting_power.get(proposer, 0)
            if proposer_power < self.governance_parameters['min_proposal_amount']:
                return {
                    'status': 'error',
                    'message': f'Insufficient voting power. Required: {self.governance_parameters["min_proposal_amount"]}, Available: {proposer_power}'
                }
            
            # Create proposal
            proposal_id = f"proposal_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            voting_start = datetime.now()
            voting_end = voting_start + timedelta(days=self.governance_parameters['proposal_duration'])
            
            proposal = Proposal(
                proposal_id=proposal_id,
                title=title,
                description=description,
                proposal_type=proposal_type,
                proposer=proposer,
                created_at=datetime.now(),
                voting_start=voting_start,
                voting_end=voting_end,
                status=ProposalStatus.ACTIVE,
                execution_data=execution_data
            )
            
            self.proposals[proposal_id] = proposal
            
            result = {
                'status': 'success',
                'proposal_id': proposal_id,
                'voting_start': voting_start,
                'voting_end': voting_end,
                'quorum_threshold': proposal.quorum_threshold,
                'majority_threshold': proposal.majority_threshold
            }
            
            logger.info(f"Proposal created: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Proposal creation failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def cast_vote(self, proposal_id: str, voter: str, vote_type: VoteType) -> Dict[str, Any]:
        """
        Cast a vote on a proposal.
        
        Args:
            proposal_id: ID of the proposal
            voter: Address of the voter
            vote_type: Type of vote (YES, NO, ABSTAIN)
            
        Returns:
            Voting results
        """
        try:
            logger.info(f"Voting {vote_type.value} on proposal {proposal_id} by {voter}")
            
            # Check if proposal exists and is active
            if proposal_id not in self.proposals:
                return {'status': 'error', 'message': 'Proposal not found'}
            
            proposal = self.proposals[proposal_id]
            if proposal.status != ProposalStatus.ACTIVE:
                return {'status': 'error', 'message': 'Proposal is not active'}
            
            # Check if voting period is still open
            if datetime.now() > proposal.voting_end:
                proposal.status = ProposalStatus.EXPIRED
                return {'status': 'error', 'message': 'Voting period has ended'}
            
            # Check if voter has already voted
            existing_vote = self._get_vote(proposal_id, voter)
            if existing_vote:
                return {'status': 'error', 'message': 'Voter has already voted'}
            
            # Get voter's voting power
            voting_power = self.voting_power.get(voter, 0)
            if voting_power == 0:
                return {'status': 'error', 'message': 'No voting power available'}
            
            # Create vote
            vote_id = f"vote_{proposal_id}_{voter}_{datetime.now().timestamp()}"
            vote = Vote(
                vote_id=vote_id,
                proposal_id=proposal_id,
                voter=voter,
                vote_type=vote_type,
                voting_power=voting_power,
                timestamp=datetime.now()
            )
            
            self.votes[vote_id] = vote
            
            # Update proposal vote counts
            if vote_type == VoteType.YES:
                proposal.votes_for += voting_power
            elif vote_type == VoteType.NO:
                proposal.votes_against += voting_power
            elif vote_type == VoteType.ABSTAIN:
                proposal.votes_abstain += voting_power
            
            proposal.total_votes += voting_power
            
            result = {
                'status': 'success',
                'vote_id': vote_id,
                'voting_power': voting_power,
                'vote_type': vote_type.value,
                'proposal_votes': {
                    'for': proposal.votes_for,
                    'against': proposal.votes_against,
                    'abstain': proposal.votes_abstain,
                    'total': proposal.total_votes
                }
            }
            
            logger.info(f"Vote cast: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Vote casting failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def execute_proposal(self, proposal_id: str, executor: str) -> Dict[str, Any]:
        """
        Execute a passed proposal.
        
        Args:
            proposal_id: ID of the proposal to execute
            executor: Address of the executor
            
        Returns:
            Execution results
        """
        try:
            logger.info(f"Executing proposal {proposal_id} by {executor}")
            
            # Check if proposal exists
            if proposal_id not in self.proposals:
                return {'status': 'error', 'message': 'Proposal not found'}
            
            proposal = self.proposals[proposal_id]
            
            # Check if proposal has passed
            if proposal.status != ProposalStatus.PASSED:
                return {'status': 'error', 'message': 'Proposal has not passed'}
            
            # Check execution delay
            execution_time = proposal.voting_end + timedelta(days=self.governance_parameters['execution_delay'])
            if datetime.now() < execution_time:
                return {'status': 'error', 'message': 'Execution delay not yet passed'}
            
            # Execute proposal based on type
            execution_result = await self._execute_proposal_action(proposal)
            
            if execution_result['status'] == 'success':
                proposal.status = ProposalStatus.EXECUTED
                
                result = {
                    'status': 'success',
                    'proposal_id': proposal_id,
                    'execution_result': execution_result,
                    'executed_at': datetime.now()
                }
                
                logger.info(f"Proposal executed: {result}")
                return result
            else:
                return {
                    'status': 'error',
                    'message': 'Proposal execution failed',
                    'execution_result': execution_result
                }
            
        except Exception as e:
            logger.error(f"Proposal execution failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _execute_proposal_action(self, proposal: Proposal) -> Dict[str, Any]:
        """Execute the action specified in the proposal."""
        try:
            if proposal.proposal_type == ProposalType.STRATEGY_CHANGE:
                return await self._execute_strategy_change(proposal.execution_data)
            elif proposal.proposal_type == ProposalType.PARAMETER_UPDATE:
                return await self._execute_parameter_update(proposal.execution_data)
            elif proposal.proposal_type == ProposalType.FEE_CHANGE:
                return await self._execute_fee_change(proposal.execution_data)
            elif proposal.proposal_type == ProposalType.EMERGENCY_ACTION:
                return await self._execute_emergency_action(proposal.execution_data)
            else:
                return {'status': 'error', 'message': 'Unknown proposal type'}
                
        except Exception as e:
            logger.error(f"Proposal action execution failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _execute_strategy_change(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute strategy change."""
        # TODO: Implement actual strategy change execution
        return {'status': 'success', 'action': 'strategy_change', 'data': execution_data}
    
    async def _execute_parameter_update(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute parameter update."""
        # TODO: Implement actual parameter update execution
        return {'status': 'success', 'action': 'parameter_update', 'data': execution_data}
    
    async def _execute_fee_change(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute fee change."""
        # TODO: Implement actual fee change execution
        return {'status': 'success', 'action': 'fee_change', 'data': execution_data}
    
    async def _execute_emergency_action(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute emergency action."""
        # TODO: Implement actual emergency action execution
        return {'status': 'success', 'action': 'emergency_action', 'data': execution_data}
    
    async def check_proposal_status(self, proposal_id: str) -> Dict[str, Any]:
        """
        Check the current status of a proposal.
        
        Args:
            proposal_id: ID of the proposal
            
        Returns:
            Proposal status information
        """
        try:
            if proposal_id not in self.proposals:
                return {'status': 'error', 'message': 'Proposal not found'}
            
            proposal = self.proposals[proposal_id]
            
            # Check if voting period has ended
            if datetime.now() > proposal.voting_end and proposal.status == ProposalStatus.ACTIVE:
                # Calculate if proposal passed
                total_voting_power = sum(self.voting_power.values())
                quorum_met = proposal.total_votes >= (total_voting_power * proposal.quorum_threshold)
                
                if quorum_met:
                    majority_met = proposal.votes_for > proposal.votes_against
                    if majority_met:
                        proposal.status = ProposalStatus.PASSED
                    else:
                        proposal.status = ProposalStatus.REJECTED
                else:
                    proposal.status = ProposalStatus.REJECTED
            
            return {
                'status': 'success',
                'proposal': {
                    'proposal_id': proposal.proposal_id,
                    'title': proposal.title,
                    'description': proposal.description,
                    'proposal_type': proposal.proposal_type.value,
                    'proposer': proposal.proposer,
                    'status': proposal.status.value,
                    'voting_start': proposal.voting_start,
                    'voting_end': proposal.voting_end,
                    'votes': {
                        'for': proposal.votes_for,
                        'against': proposal.votes_against,
                        'abstain': proposal.votes_abstain,
                        'total': proposal.total_votes
                    },
                    'thresholds': {
                        'quorum': proposal.quorum_threshold,
                        'majority': proposal.majority_threshold
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Proposal status check failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _get_vote(self, proposal_id: str, voter: str) -> Optional[Vote]:
        """Get existing vote for a proposal by a voter."""
        for vote in self.votes.values():
            if vote.proposal_id == proposal_id and vote.voter == voter:
                return vote
        return None
    
    async def update_voting_power(self, address: str, new_power: float) -> Dict[str, Any]:
        """
        Update voting power for an address.
        
        Args:
            address: Address to update
            new_power: New voting power
            
        Returns:
            Update results
        """
        try:
            logger.info(f"Updating voting power for {address} to {new_power}")
            
            old_power = self.voting_power.get(address, 0)
            self.voting_power[address] = new_power
            
            result = {
                'status': 'success',
                'address': address,
                'old_power': old_power,
                'new_power': new_power,
                'change': new_power - old_power
            }
            
            logger.info(f"Voting power updated: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Voting power update failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_governance_analytics(self) -> Dict[str, Any]:
        """
        Get governance analytics and statistics.
        
        Returns:
            Governance analytics data
        """
        total_proposals = len(self.proposals)
        active_proposals = len([p for p in self.proposals.values() if p.status == ProposalStatus.ACTIVE])
        passed_proposals = len([p for p in self.proposals.values() if p.status == ProposalStatus.PASSED])
        executed_proposals = len([p for p in self.proposals.values() if p.status == ProposalStatus.EXECUTED])
        
        total_votes = len(self.votes)
        total_voting_power = sum(self.voting_power.values())
        total_voters = len(self.voting_power)
        
        return {
            'proposal_stats': {
                'total_proposals': total_proposals,
                'active_proposals': active_proposals,
                'passed_proposals': passed_proposals,
                'executed_proposals': executed_proposals
            },
            'voting_stats': {
                'total_votes': total_votes,
                'total_voting_power': total_voting_power,
                'total_voters': total_voters
            },
            'governance_parameters': self.governance_parameters,
            'recent_proposals': list(self.proposals.values())[-5:] if self.proposals else [],
            'top_voters': sorted(
                [(addr, power) for addr, power in self.voting_power.items()],
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }
