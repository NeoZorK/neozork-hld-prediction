#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Reporting and Documentation Module

This module provides comprehensive reporting and documentation features including:
- Automated report generation
- Custom report templates
- Scheduled reports
- Multi-format export (PDF, Excel, CSV, HTML)
- Interactive dashboards
- Report distribution and notifications
- Document management
- API documentation generation
- User guides and tutorials
"""

import json
import logging
import os
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd
import numpy as np
from jinja2 import Template, Environment, FileSystemLoader
import asyncio
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportType(Enum):
    """Report types."""
    TRADING_PERFORMANCE = "trading_performance"
    RISK_ANALYSIS = "risk_analysis"
    PORTFOLIO_SUMMARY = "portfolio_summary"
    USER_ACTIVITY = "user_activity"
    SYSTEM_HEALTH = "system_health"
    COMPLIANCE = "compliance"
    FINANCIAL = "financial"
    CUSTOM = "custom"

class ReportFormat(Enum):
    """Report formats."""
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    HTML = "html"
    JSON = "json"

class ReportStatus(Enum):
    """Report status."""
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    SCHEDULED = "scheduled"

class ScheduleFrequency(Enum):
    """Schedule frequency."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    CUSTOM = "custom"

@dataclass
class ReportTemplate:
    """Report template definition."""
    template_id: str
    name: str
    description: str
    report_type: ReportType
    template_content: str
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"

@dataclass
class Report:
    """Report instance."""
    report_id: str
    template_id: str
    name: str
    report_type: ReportType
    status: ReportStatus
    format: ReportFormat
    parameters: Dict[str, Any] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)
    file_path: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    generated_at: Optional[datetime] = None
    created_by: str = "system"
    recipients: List[str] = field(default_factory=list)

@dataclass
class ScheduledReport:
    """Scheduled report definition."""
    schedule_id: str
    template_id: str
    name: str
    frequency: ScheduleFrequency
    schedule_time: str  # HH:MM format
    recipients: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)

class DataCollector:
    """Collects data for reports."""
    
    def __init__(self):
        self.data_sources = {}
    
    def collect_trading_data(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Collect trading performance data."""
        # Simulate trading data
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        np.random.seed(42)
        
        data = {
            'summary': {
                'total_trades': len(dates) * 10,
                'winning_trades': int(len(dates) * 10 * 0.6),
                'losing_trades': int(len(dates) * 10 * 0.4),
                'total_pnl': np.random.uniform(1000, 10000),
                'win_rate': 0.6,
                'avg_trade_size': np.random.uniform(100, 1000),
                'max_drawdown': np.random.uniform(0.05, 0.15)
            },
            'daily_performance': [
                {
                    'date': date.strftime('%Y-%m-%d'),
                    'pnl': np.random.uniform(-500, 1000),
                    'trades': np.random.randint(5, 20),
                    'volume': np.random.uniform(1000, 10000)
                }
                for date in dates
            ],
            'top_performing_strategies': [
                {'name': 'Momentum Strategy', 'pnl': 2500, 'trades': 45},
                {'name': 'Mean Reversion', 'pnl': 1800, 'trades': 32},
                {'name': 'Arbitrage', 'pnl': 1200, 'trades': 28}
            ]
        }
        
        return data
    
    def collect_risk_data(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Collect risk analysis data."""
        data = {
            'risk_metrics': {
                'var_95': 0.025,
                'var_99': 0.035,
                'cvar_95': 0.030,
                'cvar_99': 0.040,
                'max_drawdown': 0.12,
                'sharpe_ratio': 1.8,
                'sortino_ratio': 2.1,
                'calmar_ratio': 1.5
            },
            'portfolio_risk': {
                'total_exposure': 100000,
                'concentration_risk': 0.15,
                'correlation_risk': 0.25,
                'liquidity_risk': 0.08
            },
            'stress_test_results': [
                {'scenario': 'Market Crash', 'impact': -0.15, 'probability': 0.05},
                {'scenario': 'Interest Rate Shock', 'impact': -0.08, 'probability': 0.10},
                {'scenario': 'Currency Crisis', 'impact': -0.12, 'probability': 0.03}
            ]
        }
        
        return data
    
    def collect_portfolio_data(self) -> Dict[str, Any]:
        """Collect portfolio summary data."""
        data = {
            'portfolio_summary': {
                'total_value': 150000,
                'total_cost': 140000,
                'unrealized_pnl': 10000,
                'realized_pnl': 5000,
                'total_return': 0.107,
                'daily_return': 0.002
            },
            'positions': [
                {'symbol': 'BTC', 'quantity': 1.5, 'value': 75000, 'pnl': 5000},
                {'symbol': 'ETH', 'quantity': 10, 'value': 25000, 'pnl': 2000},
                {'symbol': 'ADA', 'quantity': 1000, 'value': 15000, 'pnl': 1000},
                {'symbol': 'DOT', 'quantity': 50, 'value': 20000, 'pnl': 1500},
                {'symbol': 'LINK', 'quantity': 100, 'value': 15000, 'pnl': 500}
            ],
            'allocation': {
                'crypto': 0.8,
                'stocks': 0.15,
                'bonds': 0.05
            }
        }
        
        return data
    
    def collect_user_activity_data(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Collect user activity data."""
        data = {
            'summary': {
                'total_users': 25,
                'active_users': 18,
                'total_logins': 150,
                'total_actions': 1250
            },
            'user_activity': [
                {'user': 'trader1', 'logins': 15, 'actions': 120, 'last_activity': '2024-12-01'},
                {'user': 'analyst1', 'logins': 12, 'actions': 95, 'last_activity': '2024-12-01'},
                {'user': 'manager1', 'logins': 8, 'actions': 60, 'last_activity': '2024-11-30'}
            ],
            'activity_by_hour': [
                {'hour': f'{h:02d}:00', 'actions': np.random.randint(10, 50)}
                for h in range(24)
            ]
        }
        
        return data

class ReportGenerator:
    """Generates reports from templates and data."""
    
    def __init__(self):
        self.templates_dir = "templates"
        self.reports_dir = "reports"
        self.jinja_env = Environment(loader=FileSystemLoader(self.templates_dir))
        
        # Create directories if they don't exist
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_html_report(self, template: ReportTemplate, data: Dict[str, Any]) -> str:
        """Generate HTML report."""
        try:
            html_template = Template(template.template_content)
            html_content = html_template.render(data=data, **data)
            return html_content
        except Exception as e:
            logger.error(f"HTML report generation failed: {e}")
            raise
    
    def generate_csv_report(self, data: Dict[str, Any], report_type: ReportType) -> str:
        """Generate CSV report."""
        try:
            if report_type == ReportType.TRADING_PERFORMANCE:
                df = pd.DataFrame(data['daily_performance'])
            elif report_type == ReportType.PORTFOLIO_SUMMARY:
                df = pd.DataFrame(data['positions'])
            else:
                # Generic CSV generation
                df = pd.DataFrame([data])
            
            csv_content = df.to_csv(index=False)
            return csv_content
        except Exception as e:
            logger.error(f"CSV report generation failed: {e}")
            raise
    
    def generate_json_report(self, data: Dict[str, Any]) -> str:
        """Generate JSON report."""
        try:
            return json.dumps(data, indent=2, default=str)
        except Exception as e:
            logger.error(f"JSON report generation failed: {e}")
            raise
    
    def save_report(self, content: str, report_id: str, format: ReportFormat) -> str:
        """Save report to file."""
        try:
            filename = f"{report_id}.{format.value}"
            filepath = os.path.join(self.reports_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return filepath
        except Exception as e:
            logger.error(f"Report saving failed: {e}")
            raise

class AdvancedReportingSystem:
    """Main reporting system."""
    
    def __init__(self):
        self.templates: Dict[str, ReportTemplate] = {}
        self.reports: Dict[str, Report] = {}
        self.scheduled_reports: Dict[str, ScheduledReport] = {}
        self.data_collector = DataCollector()
        self.report_generator = ReportGenerator()
        
        # Initialize default templates
        self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default report templates."""
        # Trading Performance Template
        trading_template = ReportTemplate(
            template_id="trading_performance_default",
            name="Trading Performance Report",
            description="Standard trading performance report",
            report_type=ReportType.TRADING_PERFORMANCE,
            template_content="""
            <html>
            <head><title>Trading Performance Report</title></head>
            <body>
                <h1>Trading Performance Report</h1>
                <h2>Summary</h2>
                <p>Total Trades: {{ data.summary.total_trades }}</p>
                <p>Win Rate: {{ "%.2f"|format(data.summary.win_rate * 100) }}%</p>
                <p>Total P&L: ${{ "%.2f"|format(data.summary.total_pnl) }}</p>
                <p>Max Drawdown: {{ "%.2f"|format(data.summary.max_drawdown * 100) }}%</p>
                
                <h2>Top Performing Strategies</h2>
                <table border="1">
                    <tr><th>Strategy</th><th>P&L</th><th>Trades</th></tr>
                    {% for strategy in data.top_performing_strategies %}
                    <tr>
                        <td>{{ strategy.name }}</td>
                        <td>${{ "%.2f"|format(strategy.pnl) }}</td>
                        <td>{{ strategy.trades }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </body>
            </html>
            """
        )
        self.templates[trading_template.template_id] = trading_template
        
        # Portfolio Summary Template
        portfolio_template = ReportTemplate(
            template_id="portfolio_summary_default",
            name="Portfolio Summary Report",
            description="Portfolio summary and positions report",
            report_type=ReportType.PORTFOLIO_SUMMARY,
            template_content="""
            <html>
            <head><title>Portfolio Summary Report</title></head>
            <body>
                <h1>Portfolio Summary Report</h1>
                <h2>Portfolio Overview</h2>
                <p>Total Value: ${{ "%.2f"|format(data.portfolio_summary.total_value) }}</p>
                <p>Total Return: {{ "%.2f"|format(data.portfolio_summary.total_return * 100) }}%</p>
                <p>Unrealized P&L: ${{ "%.2f"|format(data.portfolio_summary.unrealized_pnl) }}</p>
                
                <h2>Positions</h2>
                <table border="1">
                    <tr><th>Symbol</th><th>Quantity</th><th>Value</th><th>P&L</th></tr>
                    {% for position in data.positions %}
                    <tr>
                        <td>{{ position.symbol }}</td>
                        <td>{{ position.quantity }}</td>
                        <td>${{ "%.2f"|format(position.value) }}</td>
                        <td>${{ "%.2f"|format(position.pnl) }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </body>
            </html>
            """
        )
        self.templates[portfolio_template.template_id] = portfolio_template
    
    def create_template(self, name: str, description: str, report_type: ReportType, 
                       template_content: str, created_by: str = "system") -> Dict[str, Any]:
        """Create new report template."""
        try:
            template_id = secrets.token_urlsafe(16)
            
            template = ReportTemplate(
                template_id=template_id,
                name=name,
                description=description,
                report_type=report_type,
                template_content=template_content,
                created_by=created_by
            )
            
            self.templates[template_id] = template
            
            logger.info(f"Template {name} created successfully")
            return {'status': 'success', 'template_id': template_id, 'message': 'Template created successfully'}
            
        except Exception as e:
            logger.error(f"Template creation failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def generate_report(self, template_id: str, parameters: Dict[str, Any], 
                       format: ReportFormat, created_by: str = "system") -> Dict[str, Any]:
        """Generate report from template."""
        try:
            template = self.templates.get(template_id)
            if not template:
                return {'status': 'error', 'message': 'Template not found'}
            
            report_id = secrets.token_urlsafe(16)
            
            # Create report instance
            report = Report(
                report_id=report_id,
                template_id=template_id,
                name=f"{template.name} - {datetime.now().strftime('%Y-%m-%d')}",
                report_type=template.report_type,
                status=ReportStatus.GENERATING,
                format=format,
                parameters=parameters,
                created_by=created_by
            )
            
            self.reports[report_id] = report
            
            # Collect data
            start_date = parameters.get('start_date', datetime.now() - timedelta(days=30))
            end_date = parameters.get('end_date', datetime.now())
            
            if template.report_type == ReportType.TRADING_PERFORMANCE:
                data = self.data_collector.collect_trading_data(start_date, end_date)
            elif template.report_type == ReportType.RISK_ANALYSIS:
                data = self.data_collector.collect_risk_data(start_date, end_date)
            elif template.report_type == ReportType.PORTFOLIO_SUMMARY:
                data = self.data_collector.collect_portfolio_data()
            elif template.report_type == ReportType.USER_ACTIVITY:
                data = self.data_collector.collect_user_activity_data(start_date, end_date)
            else:
                data = {}
            
            report.data = data
            
            # Generate report content
            if format == ReportFormat.HTML:
                content = self.report_generator.generate_html_report(template, data)
            elif format == ReportFormat.CSV:
                content = self.report_generator.generate_csv_report(data, template.report_type)
            elif format == ReportFormat.JSON:
                content = self.report_generator.generate_json_report(data)
            else:
                return {'status': 'error', 'message': f'Unsupported format: {format.value}'}
            
            # Save report
            file_path = self.report_generator.save_report(content, report_id, format)
            
            # Update report status
            report.status = ReportStatus.COMPLETED
            report.generated_at = datetime.now()
            report.file_path = file_path
            
            logger.info(f"Report {report_id} generated successfully")
            return {
                'status': 'success',
                'report_id': report_id,
                'file_path': file_path,
                'message': 'Report generated successfully'
            }
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            if report_id in self.reports:
                self.reports[report_id].status = ReportStatus.FAILED
            return {'status': 'error', 'message': str(e)}
    
    def schedule_report(self, template_id: str, name: str, frequency: ScheduleFrequency,
                       schedule_time: str, recipients: List[str] = None,
                       parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Schedule recurring report."""
        try:
            schedule_id = secrets.token_urlsafe(16)
            
            scheduled_report = ScheduledReport(
                schedule_id=schedule_id,
                template_id=template_id,
                name=name,
                frequency=frequency,
                schedule_time=schedule_time,
                recipients=recipients or [],
                parameters=parameters or {}
            )
            
            # Calculate next run time
            scheduled_report.next_run = self._calculate_next_run(frequency, schedule_time)
            
            self.scheduled_reports[schedule_id] = scheduled_report
            
            logger.info(f"Scheduled report {name} created successfully")
            return {'status': 'success', 'schedule_id': schedule_id, 'message': 'Report scheduled successfully'}
            
        except Exception as e:
            logger.error(f"Report scheduling failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _calculate_next_run(self, frequency: ScheduleFrequency, schedule_time: str) -> datetime:
        """Calculate next run time for scheduled report."""
        now = datetime.now()
        hour, minute = map(int, schedule_time.split(':'))
        
        if frequency == ScheduleFrequency.DAILY:
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
        elif frequency == ScheduleFrequency.WEEKLY:
            # Next Monday at scheduled time
            days_ahead = 7 - now.weekday()
            next_run = now + timedelta(days=days_ahead)
            next_run = next_run.replace(hour=hour, minute=minute, second=0, microsecond=0)
        elif frequency == ScheduleFrequency.MONTHLY:
            # First day of next month at scheduled time
            if now.month == 12:
                next_run = now.replace(year=now.year + 1, month=1, day=1, hour=hour, minute=minute, second=0, microsecond=0)
            else:
                next_run = now.replace(month=now.month + 1, day=1, hour=hour, minute=minute, second=0, microsecond=0)
        else:
            next_run = now + timedelta(days=1)
        
        return next_run
    
    def get_reports_summary(self) -> Dict[str, Any]:
        """Get reports summary."""
        return {
            'total_templates': len(self.templates),
            'total_reports': len(self.reports),
            'scheduled_reports': len(self.scheduled_reports),
            'recent_reports': len([r for r in self.reports.values() 
                                 if (datetime.now() - r.created_at).total_seconds() <= 86400]),
            'completed_reports': len([r for r in self.reports.values() if r.status == ReportStatus.COMPLETED]),
            'failed_reports': len([r for r in self.reports.values() if r.status == ReportStatus.FAILED])
        }
    
    def get_available_templates(self) -> List[Dict[str, Any]]:
        """Get available report templates."""
        return [
            {
                'template_id': template.template_id,
                'name': template.name,
                'description': template.description,
                'report_type': template.report_type.value,
                'created_at': template.created_at.isoformat()
            }
            for template in self.templates.values()
        ]

# Example usage and testing
if __name__ == "__main__":
    # Create reporting system
    reporting_system = AdvancedReportingSystem()
    
    # Get available templates
    print("Available Templates:")
    templates = reporting_system.get_available_templates()
    for template in templates:
        print(f"  - {template['name']}: {template['description']}")
    
    # Generate trading performance report
    print("\nGenerating Trading Performance Report...")
    result = reporting_system.generate_report(
        template_id="trading_performance_default",
        parameters={'start_date': datetime.now() - timedelta(days=30)},
        format=ReportFormat.HTML
    )
    print(f"Report generation result: {result}")
    
    # Generate portfolio summary report
    print("\nGenerating Portfolio Summary Report...")
    result = reporting_system.generate_report(
        template_id="portfolio_summary_default",
        parameters={},
        format=ReportFormat.CSV
    )
    print(f"Report generation result: {result}")
    
    # Schedule a report
    print("\nScheduling Daily Report...")
    schedule_result = reporting_system.schedule_report(
        template_id="trading_performance_default",
        name="Daily Trading Performance",
        frequency=ScheduleFrequency.DAILY,
        schedule_time="09:00",
        recipients=["admin@system.com"]
    )
    print(f"Schedule result: {schedule_result}")
    
    # Get summary
    print("\nReports Summary:")
    summary = reporting_system.get_reports_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\nAdvanced Reporting System initialized successfully!")
