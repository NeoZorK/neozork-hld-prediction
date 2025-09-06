# -*- coding: utf-8 -*-
"""
Compliance Monitor for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive compliance monitoring and reporting capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import warnings

class ComplianceStandard(Enum):
    """Compliance standard enumeration."""
    GDPR = "gdpr"
    SOX = "sox"
    PCI_DSS = "pci_dss"
    HIPAA = "hipaa"
    ISO_27001 = "iso_27001"
    FINRA = "finra"
    SEC = "sec"

class ComplianceStatus(Enum):
    """Compliance status enumeration."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    UNDER_REVIEW = "under_review"

class ComplianceMonitor:
    """
    Compliance monitoring system for regulatory adherence.
    
    Features:
    - Compliance Standard Monitoring
    - Policy Management
    - Risk Assessment
    - Compliance Reporting
    - Audit Trail
    - Violation Detection
    """
    
    def __init__(self):
        """Initialize the Compliance Monitor."""
        self.compliance_policies = {}
        self.compliance_checks = {}
        self.compliance_reports = {}
        self.violations = {}
        self.audit_trail = []
        self.risk_assessments = {}
    
    def create_compliance_policy(self, policy_name: str, standard: str, 
                                requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a compliance policy.
        
        Args:
            policy_name: Name of the policy
            standard: Compliance standard
            requirements: List of requirements
            
        Returns:
            Policy creation result
        """
        try:
            # Validate standard
            valid_standards = [s.value for s in ComplianceStandard]
            if standard not in valid_standards:
                return {"status": "error", "message": f"Invalid standard: {standard}"}
            
            # Check if policy already exists
            if policy_name in self.compliance_policies:
                return {"status": "error", "message": f"Policy {policy_name} already exists"}
            
            # Generate policy ID
            policy_id = f"policy_{int(time.time())}"
            
            # Create policy
            policy = {
                "policy_id": policy_id,
                "policy_name": policy_name,
                "standard": standard,
                "requirements": requirements,
                "created_time": time.time(),
                "last_updated": time.time(),
                "is_active": True,
                "version": 1
            }
            
            # Store policy
            self.compliance_policies[policy_name] = policy
            
            # Log audit event
            self._log_audit_event("policy_created", "system", {
                "policy_name": policy_name,
                "standard": standard,
                "n_requirements": len(requirements)
            })
            
            result = {
                "status": "success",
                "policy_id": policy_id,
                "policy_name": policy_name,
                "standard": standard,
                "requirements": requirements,
                "n_requirements": len(requirements),
                "message": "Compliance policy created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create compliance policy: {str(e)}"}
    
    def run_compliance_check(self, policy_name: str, check_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a compliance check against a policy.
        
        Args:
            policy_name: Name of the policy
            check_data: Data to check against policy
            
        Returns:
            Compliance check result
        """
        try:
            # Check if policy exists
            if policy_name not in self.compliance_policies:
                return {"status": "error", "message": f"Policy {policy_name} not found"}
            
            policy = self.compliance_policies[policy_name]
            
            # Check if policy is active
            if not policy["is_active"]:
                return {"status": "error", "message": f"Policy {policy_name} is not active"}
            
            # Generate check ID
            check_id = f"check_{int(time.time())}"
            
            # Run compliance checks
            check_results = []
            violations = []
            overall_status = ComplianceStatus.COMPLIANT.value
            
            for requirement in policy["requirements"]:
                requirement_id = requirement.get("id", f"req_{len(check_results)}")
                requirement_type = requirement.get("type", "unknown")
                requirement_description = requirement.get("description", "")
                
                # Simulate compliance check
                is_compliant, violation_details = self._check_requirement(requirement, check_data)
                
                check_result = {
                    "requirement_id": requirement_id,
                    "requirement_type": requirement_type,
                    "requirement_description": requirement_description,
                    "is_compliant": is_compliant,
                    "violation_details": violation_details,
                    "check_time": time.time()
                }
                
                check_results.append(check_result)
                
                if not is_compliant:
                    violations.append(check_result)
                    overall_status = ComplianceStatus.NON_COMPLIANT.value
            
            # Determine overall status
            if len(violations) > 0 and len(violations) < len(check_results):
                overall_status = ComplianceStatus.PARTIALLY_COMPLIANT.value
            
            # Store check results
            self.compliance_checks[check_id] = {
                "check_id": check_id,
                "policy_name": policy_name,
                "standard": policy["standard"],
                "check_results": check_results,
                "violations": violations,
                "overall_status": overall_status,
                "check_time": time.time(),
                "n_requirements": len(check_results),
                "n_violations": len(violations)
            }
            
            # Store violations
            if violations:
                self.violations[check_id] = {
                    "check_id": check_id,
                    "policy_name": policy_name,
                    "standard": policy["standard"],
                    "violations": violations,
                    "violation_time": time.time(),
                    "severity": self._calculate_violation_severity(violations)
                }
            
            # Log audit event
            self._log_audit_event("compliance_check", "system", {
                "check_id": check_id,
                "policy_name": policy_name,
                "overall_status": overall_status,
                "n_violations": len(violations)
            })
            
            result = {
                "status": "success",
                "check_id": check_id,
                "policy_name": policy_name,
                "standard": policy["standard"],
                "overall_status": overall_status,
                "n_requirements": len(check_results),
                "n_violations": len(violations),
                "check_results": check_results,
                "violations": violations,
                "message": "Compliance check completed successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to run compliance check: {str(e)}"}
    
    def generate_compliance_report(self, policy_name: str, time_range: str = "30d") -> Dict[str, Any]:
        """
        Generate a compliance report.
        
        Args:
            policy_name: Name of the policy
            time_range: Time range for the report
            
        Returns:
            Compliance report result
        """
        try:
            # Check if policy exists
            if policy_name not in self.compliance_policies:
                return {"status": "error", "message": f"Policy {policy_name} not found"}
            
            policy = self.compliance_policies[policy_name]
            
            # Calculate time range
            time_ranges = {
                "7d": 7 * 24 * 3600,
                "30d": 30 * 24 * 3600,
                "90d": 90 * 24 * 3600,
                "1y": 365 * 24 * 3600
            }
            
            if time_range not in time_ranges:
                return {"status": "error", "message": f"Invalid time range: {time_range}"}
            
            range_seconds = time_ranges[time_range]
            current_time = time.time()
            start_time = current_time - range_seconds
            
            # Filter compliance checks
            relevant_checks = [
                check for check in self.compliance_checks.values()
                if check["policy_name"] == policy_name and check["check_time"] >= start_time
            ]
            
            # Calculate statistics
            total_checks = len(relevant_checks)
            compliant_checks = len([c for c in relevant_checks if c["overall_status"] == ComplianceStatus.COMPLIANT.value])
            non_compliant_checks = len([c for c in relevant_checks if c["overall_status"] == ComplianceStatus.NON_COMPLIANT.value])
            partially_compliant_checks = len([c for c in relevant_checks if c["overall_status"] == ComplianceStatus.PARTIALLY_COMPLIANT.value])
            
            compliance_rate = (compliant_checks / total_checks * 100) if total_checks > 0 else 0
            
            # Calculate violation statistics
            total_violations = sum(c["n_violations"] for c in relevant_checks)
            violation_rate = (total_violations / (total_checks * policy["n_requirements"]) * 100) if total_checks > 0 else 0
            
            # Generate report ID
            report_id = f"report_{int(time.time())}"
            
            # Create report
            report = {
                "report_id": report_id,
                "policy_name": policy_name,
                "standard": policy["standard"],
                "time_range": time_range,
                "generated_time": time.time(),
                "statistics": {
                    "total_checks": total_checks,
                    "compliant_checks": compliant_checks,
                    "non_compliant_checks": non_compliant_checks,
                    "partially_compliant_checks": partially_compliant_checks,
                    "compliance_rate": compliance_rate,
                    "total_violations": total_violations,
                    "violation_rate": violation_rate
                },
                "checks": relevant_checks
            }
            
            # Store report
            self.compliance_reports[report_id] = report
            
            result = {
                "status": "success",
                "report_id": report_id,
                "policy_name": policy_name,
                "standard": policy["standard"],
                "time_range": time_range,
                "statistics": report["statistics"],
                "n_checks": total_checks,
                "message": "Compliance report generated successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to generate compliance report: {str(e)}"}
    
    def assess_risk(self, policy_name: str, risk_factors: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess compliance risk.
        
        Args:
            policy_name: Name of the policy
            risk_factors: Risk factors to assess
            
        Returns:
            Risk assessment result
        """
        try:
            # Check if policy exists
            if policy_name not in self.compliance_policies:
                return {"status": "error", "message": f"Policy {policy_name} not found"}
            
            policy = self.compliance_policies[policy_name]
            
            # Generate assessment ID
            assessment_id = f"risk_{int(time.time())}"
            
            # Calculate risk score
            risk_score = self._calculate_risk_score(risk_factors)
            
            # Determine risk level
            if risk_score >= 80:
                risk_level = "critical"
            elif risk_score >= 60:
                risk_level = "high"
            elif risk_score >= 40:
                risk_level = "medium"
            elif risk_score >= 20:
                risk_level = "low"
            else:
                risk_level = "minimal"
            
            # Identify risk factors
            risk_factors_analysis = self._analyze_risk_factors(risk_factors)
            
            # Generate recommendations
            recommendations = self._generate_risk_recommendations(risk_level, risk_factors_analysis)
            
            # Create risk assessment
            assessment = {
                "assessment_id": assessment_id,
                "policy_name": policy_name,
                "standard": policy["standard"],
                "risk_score": risk_score,
                "risk_level": risk_level,
                "risk_factors": risk_factors,
                "risk_factors_analysis": risk_factors_analysis,
                "recommendations": recommendations,
                "assessment_time": time.time()
            }
            
            # Store assessment
            self.risk_assessments[assessment_id] = assessment
            
            result = {
                "status": "success",
                "assessment_id": assessment_id,
                "policy_name": policy_name,
                "standard": policy["standard"],
                "risk_score": risk_score,
                "risk_level": risk_level,
                "risk_factors_analysis": risk_factors_analysis,
                "recommendations": recommendations,
                "message": "Risk assessment completed successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to assess risk: {str(e)}"}
    
    def get_violations(self, policy_name: str = None, limit: int = 100) -> Dict[str, Any]:
        """
        Get compliance violations.
        
        Args:
            policy_name: Filter by policy name (optional)
            limit: Maximum number of violations to return
            
        Returns:
            Violations result
        """
        try:
            # Filter violations
            filtered_violations = list(self.violations.values())
            
            if policy_name:
                filtered_violations = [v for v in filtered_violations if v["policy_name"] == policy_name]
            
            # Sort by violation time (newest first)
            filtered_violations.sort(key=lambda x: x["violation_time"], reverse=True)
            
            # Limit results
            limited_violations = filtered_violations[:limit]
            
            result = {
                "status": "success",
                "violations": limited_violations,
                "n_violations": len(limited_violations),
                "total_violations": len(self.violations)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get violations: {str(e)}"}
    
    def get_audit_trail(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get audit trail.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            Audit trail result
        """
        try:
            # Sort by timestamp (newest first)
            sorted_trail = sorted(self.audit_trail, key=lambda x: x.get("timestamp", 0), reverse=True)
            
            # Limit results
            limited_trail = sorted_trail[:limit]
            
            result = {
                "status": "success",
                "audit_trail": limited_trail,
                "n_entries": len(limited_trail),
                "total_entries": len(self.audit_trail)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get audit trail: {str(e)}"}
    
    def _check_requirement(self, requirement: Dict[str, Any], check_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Check a single requirement against data."""
        # Simulate requirement checking
        requirement_type = requirement.get("type", "unknown")
        
        # Simple compliance check simulation
        is_compliant = np.random.random() > 0.3  # 70% compliance rate
        
        violation_details = {}
        if not is_compliant:
            violation_details = {
                "violation_type": f"non_compliance_{requirement_type}",
                "description": f"Requirement {requirement.get('id', 'unknown')} not met",
                "severity": "medium"
            }
        
        return is_compliant, violation_details
    
    def _calculate_violation_severity(self, violations: List[Dict[str, Any]]) -> str:
        """Calculate overall violation severity."""
        if not violations:
            return "none"
        
        severities = [v.get("violation_details", {}).get("severity", "low") for v in violations]
        
        if "critical" in severities:
            return "critical"
        elif "high" in severities:
            return "high"
        elif "medium" in severities:
            return "medium"
        else:
            return "low"
    
    def _calculate_risk_score(self, risk_factors: Dict[str, Any]) -> float:
        """Calculate overall risk score."""
        # Simple risk score calculation
        base_score = 50.0
        
        # Adjust based on risk factors
        for factor, value in risk_factors.items():
            if isinstance(value, (int, float)):
                base_score += value * 10
            elif isinstance(value, bool):
                base_score += 20 if value else -10
            elif isinstance(value, str):
                if "high" in value.lower():
                    base_score += 30
                elif "medium" in value.lower():
                    base_score += 15
                elif "low" in value.lower():
                    base_score += 5
        
        return max(0, min(100, base_score))
    
    def _analyze_risk_factors(self, risk_factors: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risk factors."""
        analysis = {
            "high_risk_factors": [],
            "medium_risk_factors": [],
            "low_risk_factors": []
        }
        
        for factor, value in risk_factors.items():
            if isinstance(value, (int, float)) and value > 5:
                analysis["high_risk_factors"].append(factor)
            elif isinstance(value, bool) and value:
                analysis["medium_risk_factors"].append(factor)
            else:
                analysis["low_risk_factors"].append(factor)
        
        return analysis
    
    def _generate_risk_recommendations(self, risk_level: str, risk_factors_analysis: Dict[str, Any]) -> List[str]:
        """Generate risk mitigation recommendations."""
        recommendations = []
        
        if risk_level == "critical":
            recommendations.extend([
                "Immediate action required to address critical risk factors",
                "Implement emergency compliance measures",
                "Conduct immediate audit and remediation"
            ])
        elif risk_level == "high":
            recommendations.extend([
                "Address high-risk factors within 48 hours",
                "Implement additional monitoring and controls",
                "Schedule compliance review meeting"
            ])
        elif risk_level == "medium":
            recommendations.extend([
                "Address medium-risk factors within 1 week",
                "Review and update compliance procedures",
                "Increase monitoring frequency"
            ])
        else:
            recommendations.extend([
                "Continue current compliance practices",
                "Regular monitoring and review",
                "Maintain compliance documentation"
            ])
        
        return recommendations
    
    def _log_audit_event(self, event_type: str, user: str, details: Dict[str, Any]) -> None:
        """Log an audit event."""
        audit_entry = {
            "timestamp": time.time(),
            "event_type": event_type,
            "user": user,
            "details": details
        }
        self.audit_trail.append(audit_entry)
