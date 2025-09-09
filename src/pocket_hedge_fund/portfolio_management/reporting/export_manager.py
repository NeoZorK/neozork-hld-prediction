"""
Export Manager - Portfolio Data Export

This module provides portfolio data export functionality including
PDF reports, Excel files, CSV exports, and API data exports.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, date
from decimal import Decimal
import json
import csv
import io

logger = logging.getLogger(__name__)


class ExportManager:
    """Portfolio data export functionality."""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        self.export_formats = {
            'json': self._export_to_json,
            'csv': self._export_to_csv,
            'excel': self._export_to_excel,
            'pdf': self._export_to_pdf,
            'xml': self._export_to_xml
        }
        
    async def export_portfolio_data(
        self, 
        portfolio_data: Dict[str, Any], 
        export_format: str = 'json',
        include_charts: bool = False
    ) -> Union[str, bytes]:
        """Export portfolio data in specified format."""
        try:
            if export_format not in self.export_formats:
                raise ValueError(f"Unsupported export format: {export_format}")
            
            # Prepare data for export
            export_data = await self._prepare_export_data(portfolio_data, include_charts)
            
            # Export in specified format
            result = await self.export_formats[export_format](export_data)
            
            logger.info(f"Exported portfolio data in {export_format} format")
            return result
            
        except Exception as e:
            logger.error(f"Failed to export portfolio data: {e}")
            raise
    
    async def export_performance_report(
        self, 
        performance_data: Dict[str, Any], 
        export_format: str = 'pdf'
    ) -> Union[str, bytes]:
        """Export performance report."""
        try:
            # Prepare performance report data
            report_data = {
                'report_type': 'performance',
                'generated_at': datetime.utcnow().isoformat(),
                'data': performance_data
            }
            
            # Export in specified format
            result = await self.export_formats[export_format](report_data)
            
            logger.info(f"Exported performance report in {export_format} format")
            return result
            
        except Exception as e:
            logger.error(f"Failed to export performance report: {e}")
            raise
    
    async def export_risk_report(
        self, 
        risk_data: Dict[str, Any], 
        export_format: str = 'pdf'
    ) -> Union[str, bytes]:
        """Export risk report."""
        try:
            # Prepare risk report data
            report_data = {
                'report_type': 'risk',
                'generated_at': datetime.utcnow().isoformat(),
                'data': risk_data
            }
            
            # Export in specified format
            result = await self.export_formats[export_format](report_data)
            
            logger.info(f"Exported risk report in {export_format} format")
            return result
            
        except Exception as e:
            logger.error(f"Failed to export risk report: {e}")
            raise
    
    async def export_comprehensive_report(
        self, 
        comprehensive_data: Dict[str, Any], 
        export_format: str = 'pdf'
    ) -> Union[str, bytes]:
        """Export comprehensive portfolio report."""
        try:
            # Prepare comprehensive report data
            report_data = {
                'report_type': 'comprehensive',
                'generated_at': datetime.utcnow().isoformat(),
                'data': comprehensive_data
            }
            
            # Export in specified format
            result = await self.export_formats[export_format](report_data)
            
            logger.info(f"Exported comprehensive report in {export_format} format")
            return result
            
        except Exception as e:
            logger.error(f"Failed to export comprehensive report: {e}")
            raise
    
    async def export_positions_data(
        self, 
        positions_data: List[Dict[str, Any]], 
        export_format: str = 'csv'
    ) -> Union[str, bytes]:
        """Export positions data."""
        try:
            # Prepare positions data
            export_data = {
                'data_type': 'positions',
                'generated_at': datetime.utcnow().isoformat(),
                'positions': positions_data
            }
            
            # Export in specified format
            result = await self.export_formats[export_format](export_data)
            
            logger.info(f"Exported positions data in {export_format} format")
            return result
            
        except Exception as e:
            logger.error(f"Failed to export positions data: {e}")
            raise
    
    async def export_transactions_data(
        self, 
        transactions_data: List[Dict[str, Any]], 
        export_format: str = 'csv'
    ) -> Union[str, bytes]:
        """Export transactions data."""
        try:
            # Prepare transactions data
            export_data = {
                'data_type': 'transactions',
                'generated_at': datetime.utcnow().isoformat(),
                'transactions': transactions_data
            }
            
            # Export in specified format
            result = await self.export_formats[export_format](export_data)
            
            logger.info(f"Exported transactions data in {export_format} format")
            return result
            
        except Exception as e:
            logger.error(f"Failed to export transactions data: {e}")
            raise
    
    # Export format implementations
    async def _export_to_json(self, data: Dict[str, Any]) -> str:
        """Export data to JSON format."""
        try:
            return json.dumps(data, indent=2, default=str, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to export to JSON: {e}")
            raise
    
    async def _export_to_csv(self, data: Dict[str, Any]) -> str:
        """Export data to CSV format."""
        try:
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            if 'data_type' in data:
                writer.writerow(['Data Type', data['data_type']])
                writer.writerow(['Generated At', data['generated_at']])
                writer.writerow([])  # Empty row
            
            # Write data based on type
            if 'positions' in data:
                await self._write_positions_csv(writer, data['positions'])
            elif 'transactions' in data:
                await self._write_transactions_csv(writer, data['transactions'])
            elif 'data' in data:
                await self._write_generic_csv(writer, data['data'])
            else:
                await self._write_generic_csv(writer, data)
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Failed to export to CSV: {e}")
            raise
    
    async def _export_to_excel(self, data: Dict[str, Any]) -> bytes:
        """Export data to Excel format."""
        try:
            # This would use openpyxl or xlsxwriter to create Excel files
            # For now, return empty bytes
            return b""
        except Exception as e:
            logger.error(f"Failed to export to Excel: {e}")
            raise
    
    async def _export_to_pdf(self, data: Dict[str, Any]) -> bytes:
        """Export data to PDF format."""
        try:
            # This would use reportlab or similar to create PDF reports
            # For now, return empty bytes
            return b""
        except Exception as e:
            logger.error(f"Failed to export to PDF: {e}")
            raise
    
    async def _export_to_xml(self, data: Dict[str, Any]) -> str:
        """Export data to XML format."""
        try:
            # This would create XML representation of the data
            # For now, return empty string
            return ""
        except Exception as e:
            logger.error(f"Failed to export to XML: {e}")
            raise
    
    # Helper methods
    async def _prepare_export_data(self, portfolio_data: Dict[str, Any], include_charts: bool) -> Dict[str, Any]:
        """Prepare data for export."""
        try:
            export_data = {
                'export_metadata': {
                    'generated_at': datetime.utcnow().isoformat(),
                    'export_version': '1.0',
                    'include_charts': include_charts
                },
                'portfolio_data': portfolio_data
            }
            
            if include_charts:
                # Add chart data if available
                export_data['charts'] = portfolio_data.get('charts', {})
            
            return export_data
            
        except Exception as e:
            logger.error(f"Failed to prepare export data: {e}")
            return {}
    
    async def _write_positions_csv(self, writer: csv.writer, positions: List[Dict[str, Any]]):
        """Write positions data to CSV."""
        try:
            if not positions:
                return
            
            # Write header
            headers = ['Asset ID', 'Asset Name', 'Position Type', 'Quantity', 'Entry Price', 
                      'Current Price', 'Market Value', 'Unrealized P&L', 'Weight %', 'Entry Date']
            writer.writerow(headers)
            
            # Write data rows
            for position in positions:
                row = [
                    position.get('asset_id', ''),
                    position.get('asset_name', ''),
                    position.get('position_type', ''),
                    position.get('quantity', 0),
                    position.get('entry_price', 0),
                    position.get('current_price', 0),
                    position.get('market_value', 0),
                    position.get('unrealized_pnl', 0),
                    position.get('weight_percentage', 0),
                    position.get('entry_date', '')
                ]
                writer.writerow(row)
                
        except Exception as e:
            logger.error(f"Failed to write positions CSV: {e}")
    
    async def _write_transactions_csv(self, writer: csv.writer, transactions: List[Dict[str, Any]]):
        """Write transactions data to CSV."""
        try:
            if not transactions:
                return
            
            # Write header
            headers = ['Transaction ID', 'Portfolio ID', 'Asset ID', 'Type', 'Quantity', 
                      'Price', 'Total Amount', 'Fees', 'Net Amount', 'Status', 'Execution Date']
            writer.writerow(headers)
            
            # Write data rows
            for transaction in transactions:
                row = [
                    transaction.get('id', ''),
                    transaction.get('portfolio_id', ''),
                    transaction.get('asset_id', ''),
                    transaction.get('transaction_type', ''),
                    transaction.get('quantity', 0),
                    transaction.get('price', 0),
                    transaction.get('total_amount', 0),
                    transaction.get('fees', 0),
                    transaction.get('net_amount', 0),
                    transaction.get('status', ''),
                    transaction.get('execution_date', '')
                ]
                writer.writerow(row)
                
        except Exception as e:
            logger.error(f"Failed to write transactions CSV: {e}")
    
    async def _write_generic_csv(self, writer: csv.writer, data: Dict[str, Any]):
        """Write generic data to CSV."""
        try:
            # Write key-value pairs
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    writer.writerow([key, json.dumps(value, default=str)])
                else:
                    writer.writerow([key, str(value)])
                    
        except Exception as e:
            logger.error(f"Failed to write generic CSV: {e}")
    
    async def create_export_schedule(
        self, 
        portfolio_id: str, 
        export_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create scheduled export configuration."""
        try:
            schedule = {
                'portfolio_id': portfolio_id,
                'export_format': export_config.get('format', 'pdf'),
                'frequency': export_config.get('frequency', 'weekly'),
                'include_charts': export_config.get('include_charts', True),
                'email_recipients': export_config.get('email_recipients', []),
                'created_at': datetime.utcnow().isoformat(),
                'next_export': self._calculate_next_export_time(export_config.get('frequency', 'weekly'))
            }
            
            # Save schedule to database
            if self.db_manager:
                await self._save_export_schedule(schedule)
            
            return schedule
            
        except Exception as e:
            logger.error(f"Failed to create export schedule: {e}")
            return {}
    
    def _calculate_next_export_time(self, frequency: str) -> str:
        """Calculate next export time based on frequency."""
        try:
            now = datetime.utcnow()
            
            if frequency == 'daily':
                next_time = now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
            elif frequency == 'weekly':
                # Next Monday at 9 AM
                days_ahead = 7 - now.weekday()
                if days_ahead == 7:
                    days_ahead = 0
                next_time = now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=days_ahead)
            elif frequency == 'monthly':
                # First day of next month at 9 AM
                if now.month == 12:
                    next_time = now.replace(year=now.year + 1, month=1, day=1, hour=9, minute=0, second=0, microsecond=0)
                else:
                    next_time = now.replace(month=now.month + 1, day=1, hour=9, minute=0, second=0, microsecond=0)
            else:
                next_time = now + timedelta(days=1)
            
            return next_time.isoformat()
            
        except Exception as e:
            logger.error(f"Failed to calculate next export time: {e}")
            return datetime.utcnow().isoformat()
    
    async def _save_export_schedule(self, schedule: Dict[str, Any]):
        """Save export schedule to database."""
        if not self.db_manager:
            return
        
        # This would save the schedule to the database
        pass
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported export formats."""
        return list(self.export_formats.keys())
    
    def get_export_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get export metadata."""
        return {
            'export_formats': self.get_supported_formats(),
            'data_size': len(str(data)),
            'export_timestamp': datetime.utcnow().isoformat()
        }
