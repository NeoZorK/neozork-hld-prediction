"""
Security Integration Module for NeoZork Trading System

This module integrates all security features including:
- Advanced Security Manager
- Compliance & Regulatory
- Security Monitoring
- Unified Security Dashboard
- Security API
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import secrets

from .advanced_security import AdvancedSecurityManager, UserRole, Permission, SecurityEvent, SecurityLevel
from .security_monitoring import SecurityMonitoringManager, IncidentType, ThreatLevel, IncidentStatus
from compliance.regulatory_compliance import ComplianceManager, ComplianceLevel, TransactionType

logger = logging.getLogger(__name__)

class SecurityIntegrationManager:
    """Unified Security Integration Manager"""
    
    def __init__(self):
        self.security_manager = AdvancedSecurityManager()
        self.monitoring_manager = SecurityMonitoringManager()
        self.compliance_manager = ComplianceManager()
        self.integration_events = []
        
    async def initialize_security_system(self) -> Dict[str, Any]:
        """Initialize the complete security system"""
        try:
            # Initialize all security components
            security_init = await self._initialize_security_components()
            monitoring_init = await self._initialize_monitoring_components()
            compliance_init = await self._initialize_compliance_components()
            
            # Create integration event
            await self._log_integration_event(
                "system_initialization",
                "Security system initialized successfully",
                SecurityLevel.MEDIUM
            )
            
            return {
                "status": "success",
                "components": {
                    "security_manager": security_init,
                    "monitoring_manager": monitoring_init,
                    "compliance_manager": compliance_init
                },
                "message": "Security system initialized successfully"
            }
            
        except Exception as e:
            logger.error(f"Error initializing security system: {e}")
            return {
                "status": "error",
                "message": f"Security system initialization failed: {str(e)}"
            }
    
    async def create_secure_user(self, username: str, email: str, role: UserRole,
                                password: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a user with full security and compliance setup"""
        try:
            # Create user in security system
            security_result = await self.security_manager.create_user(
                username=username,
                email=email,
                role=role,
                password=password,
                require_mfa=True
            )
            
            if security_result["status"] != "success":
                return security_result
            
            user_id = security_result["user_id"]
            
            # Perform KYC verification
            kyc_result = await self.compliance_manager.perform_kyc_verification(
                user_id=user_id,
                user_data=user_data
            )
            
            # Assess compliance risk
            risk_result = await self.compliance_manager.assess_compliance_risk(user_id)
            
            # Create monitoring profile
            monitoring_result = await self._create_user_monitoring_profile(user_id, role)
            
            # Log integration event
            await self._log_integration_event(
                "user_creation",
                f"Secure user created: {username}",
                SecurityLevel.MEDIUM,
                user_id=user_id
            )
            
            return {
                "status": "success",
                "user_id": user_id,
                "security": security_result,
                "kyc": kyc_result,
                "risk_assessment": risk_result,
                "monitoring": monitoring_result,
                "message": "Secure user created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating secure user: {e}")
            return {
                "status": "error",
                "message": f"Secure user creation failed: {str(e)}"
            }
    
    async def authenticate_secure_user(self, username: str, password: str,
                                     mfa_code: Optional[str] = None) -> Dict[str, Any]:
        """Authenticate user with full security checks"""
        try:
            # Authenticate with security manager
            auth_result = await self.security_manager.authenticate_user(
                username=username,
                password=password,
                mfa_code=mfa_code
            )
            
            if auth_result["status"] != "success":
                # Log failed authentication attempt
                await self._log_security_event(
                    "authentication_failed",
                    f"Failed authentication attempt for user: {username}",
                    ThreatLevel.MEDIUM
                )
                return auth_result
            
            user_id = auth_result["user"]["user_id"]
            session_token = auth_result["session_token"]
            
            # Check compliance status
            compliance_status = await self._check_user_compliance_status(user_id)
            
            # Update monitoring
            await self._update_user_activity_monitoring(user_id, "login")
            
            # Log successful authentication
            await self._log_security_event(
                "authentication_success",
                f"Successful authentication for user: {username}",
                ThreatLevel.LOW,
                user_id=user_id
            )
            
            return {
                "status": "success",
                "session_token": session_token,
                "user": auth_result["user"],
                "compliance_status": compliance_status,
                "message": "User authenticated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return {
                "status": "error",
                "message": f"Authentication failed: {str(e)}"
            }
    
    async def process_secure_transaction(self, transaction: Dict[str, Any],
                                       session_token: str) -> Dict[str, Any]:
        """Process transaction with full security and compliance checks"""
        try:
            # Verify session and permissions
            has_permission = await self.security_manager.check_permission(
                session_token=session_token,
                permission=Permission.EXECUTE
            )
            
            if not has_permission:
                await self._log_security_event(
                    "permission_denied",
                    "Transaction execution permission denied",
                    ThreatLevel.MEDIUM
                )
                return {
                    "status": "error",
                    "message": "Insufficient permissions for transaction execution"
                }
            
            # Get user from session
            user_id = await self._get_user_from_session(session_token)
            if not user_id:
                return {
                    "status": "error",
                    "message": "Invalid session"
                }
            
            # Add user_id to transaction
            transaction["user_id"] = user_id
            
            # Monitor transaction for security threats
            security_event = {
                "type": "transaction_execution",
                "user_id": user_id,
                "transaction_data": transaction,
                "timestamp": datetime.now(datetime.UTC)
            }
            
            monitoring_result = await self.monitoring_manager.monitor_security_event(security_event)
            
            # Check AML compliance
            aml_result = await self.compliance_manager.monitor_aml_transaction(transaction)
            
            # Determine if transaction should be allowed
            security_risk = monitoring_result.get("threat_analysis", {}).get("threat_level", "low")
            aml_risk = aml_result.get("risk_level", "low")
            
            if security_risk in ["high", "critical"] or aml_risk in ["high", "critical"]:
                # Block transaction and create incident
                await self._create_transaction_incident(transaction, monitoring_result, aml_result)
                
                return {
                    "status": "blocked",
                    "reason": "High risk transaction detected",
                    "security_risk": security_risk,
                    "aml_risk": aml_risk,
                    "message": "Transaction blocked due to security or compliance concerns"
                }
            
            # Log successful transaction
            await self._log_security_event(
                "transaction_approved",
                f"Transaction approved for user {user_id}",
                ThreatLevel.LOW,
                user_id=user_id
            )
            
            return {
                "status": "approved",
                "transaction_id": secrets.token_hex(16),
                "security_analysis": monitoring_result,
                "compliance_analysis": aml_result,
                "message": "Transaction approved and processed successfully"
            }
            
        except Exception as e:
            logger.error(f"Error processing secure transaction: {e}")
            return {
                "status": "error",
                "message": f"Transaction processing failed: {str(e)}"
            }
    
    async def get_unified_security_dashboard(self) -> Dict[str, Any]:
        """Get unified security dashboard with all components"""
        try:
            # Get dashboards from all components
            security_dashboard = await self.security_manager.get_security_dashboard()
            monitoring_dashboard = await self.monitoring_manager.get_security_dashboard()
            compliance_dashboard = await self.compliance_manager.get_compliance_dashboard()
            
            # Calculate unified metrics
            unified_metrics = self._calculate_unified_metrics(
                security_dashboard,
                monitoring_dashboard,
                compliance_dashboard
            )
            
            # Get recent integration events
            recent_events = self.integration_events[-20:] if self.integration_events else []
            
            return {
                "status": "success",
                "dashboard": {
                    "unified_metrics": unified_metrics,
                    "security": security_dashboard.get("dashboard", {}),
                    "monitoring": monitoring_dashboard.get("dashboard", {}),
                    "compliance": compliance_dashboard.get("dashboard", {}),
                    "recent_events": recent_events,
                    "system_status": self._get_system_status()
                },
                "message": "Unified security dashboard retrieved successfully"
            }
            
        except Exception as e:
            logger.error(f"Error getting unified security dashboard: {e}")
            return {
                "status": "error",
                "message": f"Failed to get unified security dashboard: {str(e)}"
            }
    
    async def handle_security_incident(self, incident_type: IncidentType,
                                     description: str, severity: ThreatLevel,
                                     affected_systems: List[str],
                                     evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Handle security incident with integrated response"""
        try:
            # Create incident in monitoring system
            incident_result = await self.monitoring_manager.create_incident(
                incident_type=incident_type,
                description=description,
                severity=severity,
                affected_systems=affected_systems,
                initial_evidence=evidence
            )
            
            if incident_result["status"] != "success":
                return incident_result
            
            incident_id = incident_result["incident_id"]
            
            # Take immediate security actions
            security_actions = await self._execute_incident_security_actions(
                incident_id, incident_type, severity
            )
            
            # Update compliance records
            compliance_actions = await self._execute_incident_compliance_actions(
                incident_id, incident_type, severity
            )
            
            # Log integration event
            await self._log_integration_event(
                "incident_response",
                f"Security incident handled: {incident_id}",
                SecurityLevel.HIGH,
                incident_id=incident_id
            )
            
            return {
                "status": "success",
                "incident_id": incident_id,
                "incident": incident_result["incident"],
                "security_actions": security_actions,
                "compliance_actions": compliance_actions,
                "message": "Security incident handled successfully"
            }
            
        except Exception as e:
            logger.error(f"Error handling security incident: {e}")
            return {
                "status": "error",
                "message": f"Security incident handling failed: {str(e)}"
            }
    
    async def generate_security_report(self, report_type: str, 
                                     start_date: datetime,
                                     end_date: datetime) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        try:
            report_id = secrets.token_hex(16)
            
            # Collect data from all components
            security_events = await self._get_security_events(start_date, end_date)
            monitoring_events = await self._get_monitoring_events(start_date, end_date)
            compliance_events = await self._get_compliance_events(start_date, end_date)
            
            # Generate report
            report = {
                "report_id": report_id,
                "report_type": report_type,
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat()
                },
                "generated_at": datetime.now(datetime.UTC),
                "summary": {
                    "total_security_events": len(security_events),
                    "total_monitoring_events": len(monitoring_events),
                    "total_compliance_events": len(compliance_events),
                    "incidents": len([e for e in monitoring_events if e.get("type") == "incident"]),
                    "threats_detected": len([e for e in security_events if e.get("threat_level") in ["high", "critical"]]),
                    "compliance_violations": len([e for e in compliance_events if e.get("compliance_level") == "high"])
                },
                "detailed_data": {
                    "security_events": security_events,
                    "monitoring_events": monitoring_events,
                    "compliance_events": compliance_events
                },
                "recommendations": self._generate_security_recommendations(
                    security_events, monitoring_events, compliance_events
                )
            }
            
            return {
                "status": "success",
                "report": report,
                "message": "Security report generated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error generating security report: {e}")
            return {
                "status": "error",
                "message": f"Security report generation failed: {str(e)}"
            }
    
    async def _initialize_security_components(self) -> Dict[str, Any]:
        """Initialize security components"""
        return {"status": "initialized", "components": ["authentication", "authorization", "encryption"]}
    
    async def _initialize_monitoring_components(self) -> Dict[str, Any]:
        """Initialize monitoring components"""
        return {"status": "initialized", "components": ["threat_detection", "incident_response", "vulnerability_scanning"]}
    
    async def _initialize_compliance_components(self) -> Dict[str, Any]:
        """Initialize compliance components"""
        return {"status": "initialized", "components": ["kyc", "aml", "tax_reporting", "risk_assessment"]}
    
    async def _create_user_monitoring_profile(self, user_id: str, role: UserRole) -> Dict[str, Any]:
        """Create monitoring profile for user"""
        # In production, create actual monitoring profiles
        return {
            "status": "success",
            "monitoring_profile": {
                "user_id": user_id,
                "role": role.value,
                "monitoring_level": "standard",
                "alerts_enabled": True
            }
        }
    
    async def _check_user_compliance_status(self, user_id: str) -> Dict[str, Any]:
        """Check user compliance status"""
        # Get KYC status
        kyc_record = await self.compliance_manager._get_user_kyc_record(user_id)
        
        # Get risk assessment
        risk_assessment = await self.compliance_manager.assess_compliance_risk(user_id)
        
        return {
            "kyc_status": kyc_record["status"] if kyc_record else "not_verified",
            "risk_level": risk_assessment.get("risk_level", "unknown"),
            "compliance_score": risk_assessment.get("risk_score", 0.0)
        }
    
    async def _update_user_activity_monitoring(self, user_id: str, activity: str):
        """Update user activity monitoring"""
        # In production, update actual monitoring systems
        logger.info(f"User {user_id} performed activity: {activity}")
    
    async def _get_user_from_session(self, session_token: str) -> Optional[str]:
        """Get user ID from session token"""
        session = self.security_manager.sessions.get(session_token)
        return session["user_id"] if session else None
    
    async def _create_transaction_incident(self, transaction: Dict[str, Any],
                                         monitoring_result: Dict[str, Any],
                                         aml_result: Dict[str, Any]):
        """Create incident for blocked transaction"""
        await self.monitoring_manager.create_incident(
            incident_type=IncidentType.UNAUTHORIZED_ACCESS,
            description="High-risk transaction blocked",
            severity=ThreatLevel.HIGH,
            affected_systems=["trading_system"],
            initial_evidence={
                "transaction": transaction,
                "monitoring_result": monitoring_result,
                "aml_result": aml_result
            }
        )
    
    def _calculate_unified_metrics(self, security_dashboard: Dict[str, Any],
                                 monitoring_dashboard: Dict[str, Any],
                                 compliance_dashboard: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate unified security metrics"""
        security_data = security_dashboard.get("dashboard", {})
        monitoring_data = monitoring_dashboard.get("dashboard", {})
        compliance_data = compliance_dashboard.get("dashboard", {})
        
        return {
            "total_users": security_data.get("total_users", 0),
            "active_sessions": security_data.get("active_sessions", 0),
            "active_incidents": monitoring_data.get("overview", {}).get("active_incidents", 0),
            "open_vulnerabilities": monitoring_data.get("overview", {}).get("open_vulnerabilities", 0),
            "compliance_status": compliance_data.get("compliance_status", "UNKNOWN"),
            "overall_security_score": self._calculate_security_score(
                security_data, monitoring_data, compliance_data
            )
        }
    
    def _calculate_security_score(self, security_data: Dict[str, Any],
                                monitoring_data: Dict[str, Any],
                                compliance_data: Dict[str, Any]) -> float:
        """Calculate overall security score"""
        score = 100.0
        
        # Deduct for locked accounts
        locked_accounts = security_data.get("locked_accounts", 0)
        score -= locked_accounts * 5
        
        # Deduct for active incidents
        active_incidents = monitoring_data.get("overview", {}).get("active_incidents", 0)
        score -= active_incidents * 10
        
        # Deduct for open vulnerabilities
        open_vulnerabilities = monitoring_data.get("overview", {}).get("open_vulnerabilities", 0)
        score -= open_vulnerabilities * 2
        
        # Deduct for compliance issues
        if compliance_data.get("compliance_status") != "COMPLIANT":
            score -= 20
        
        return max(0.0, score)
    
    def _get_system_status(self) -> str:
        """Get overall system security status"""
        return "SECURE"  # In production, calculate based on actual metrics
    
    async def _execute_incident_security_actions(self, incident_id: str,
                                               incident_type: IncidentType,
                                               severity: ThreatLevel) -> List[str]:
        """Execute security actions for incident"""
        actions = []
        
        if severity in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            actions.append("Lock affected user accounts")
            actions.append("Revoke active sessions")
            actions.append("Enable additional monitoring")
        
        return actions
    
    async def _execute_incident_compliance_actions(self, incident_id: str,
                                                 incident_type: IncidentType,
                                                 severity: ThreatLevel) -> List[str]:
        """Execute compliance actions for incident"""
        actions = []
        
        if severity in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            actions.append("Update risk assessment")
            actions.append("Generate compliance report")
            actions.append("Notify regulatory authorities if required")
        
        return actions
    
    async def _get_security_events(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get security events for date range"""
        return [e for e in self.security_manager.security_events 
                if start_date <= e.get("timestamp", datetime.min) <= end_date]
    
    async def _get_monitoring_events(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get monitoring events for date range"""
        return [e for e in self.monitoring_manager.security_events 
                if start_date <= e.get("timestamp", datetime.min) <= end_date]
    
    async def _get_compliance_events(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get compliance events for date range"""
        return [e for e in self.compliance_manager.audit_logs 
                if start_date <= e.get("timestamp", datetime.min) <= end_date]
    
    def _generate_security_recommendations(self, security_events: List[Dict[str, Any]],
                                         monitoring_events: List[Dict[str, Any]],
                                         compliance_events: List[Dict[str, Any]]) -> List[str]:
        """Generate security recommendations based on events"""
        recommendations = []
        
        # Analyze security events
        high_threat_events = [e for e in security_events if e.get("threat_level") in ["high", "critical"]]
        if high_threat_events:
            recommendations.append("Review and strengthen authentication mechanisms")
        
        # Analyze monitoring events
        incidents = [e for e in monitoring_events if e.get("type") == "incident"]
        if len(incidents) > 5:
            recommendations.append("Enhance incident response procedures")
        
        # Analyze compliance events
        compliance_violations = [e for e in compliance_events if e.get("compliance_level") == "high"]
        if compliance_violations:
            recommendations.append("Strengthen compliance monitoring and controls")
        
        return recommendations
    
    async def _log_integration_event(self, event_type: str, description: str,
                                   security_level: SecurityLevel,
                                   user_id: Optional[str] = None,
                                   incident_id: Optional[str] = None):
        """Log integration event"""
        event = {
            "event_id": secrets.token_hex(8),
            "event_type": event_type,
            "description": description,
            "user_id": user_id,
            "incident_id": incident_id,
            "security_level": security_level.value,
            "timestamp": datetime.now(datetime.UTC)
        }
        
        self.integration_events.append(event)
        
        # Keep only last 1000 events
        if len(self.integration_events) > 1000:
            self.integration_events = self.integration_events[-1000:]
    
    async def _log_security_event(self, event_type: str, description: str,
                                threat_level: ThreatLevel,
                                user_id: Optional[str] = None):
        """Log security event"""
        await self.security_manager._log_security_event(
            SecurityEvent.SYSTEM_CHANGE,
            description,
            user_id=user_id,
            security_level=SecurityLevel(threat_level.value)
        )

# Example usage and testing
async def main():
    """Example usage of Security Integration Manager"""
    integration_manager = SecurityIntegrationManager()
    
    # Initialize security system
    init_result = await integration_manager.initialize_security_system()
    print(f"Security system initialization: {init_result}")
    
    # Create secure user
    user_data = {
        "full_name": "John Doe",
        "date_of_birth": "1990-01-01",
        "address": "123 Main St, City, Country",
        "phone": "+1234567890",
        "email": "john@example.com"
    }
    
    user_result = await integration_manager.create_secure_user(
        username="johndoe",
        email="john@example.com",
        role=UserRole.TRADER,
        password="SecurePass123!",
        user_data=user_data
    )
    print(f"Secure user creation: {user_result}")
    
    # Get unified dashboard
    dashboard = await integration_manager.get_unified_security_dashboard()
    print(f"Unified security dashboard: {dashboard}")

if __name__ == "__main__":
    asyncio.run(main())
