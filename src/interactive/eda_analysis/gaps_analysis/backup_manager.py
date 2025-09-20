# -*- coding: utf-8 -*-
"""
Backup Manager for NeoZork Interactive ML Trading Strategy Development.

This module provides backup functionality for MTF data before gap fixing.
"""

import os
import shutil
import pickle
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from src.common.logger import print_info, print_warning, print_error, print_debug


class BackupManager:
    """
    Backup manager for MTF data.
    
    Features:
    - Automatic backup creation
    - Backup restoration
    - Backup management
    - Compression support
    - Backup validation
    """
    
    def __init__(self, backup_dir: str = "data/backups"):
        """
        Initialize the backup manager.
        
        Args:
            backup_dir: Directory to store backups
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.current_backup = None
    
    def create_backup(self, mtf_data: Dict[str, Any], 
                     symbol: str, 
                     description: str = "Pre-gap-fixing backup") -> Dict[str, Any]:
        """
        Create a backup of MTF data.
        
        Args:
            mtf_data: MTF data to backup
            symbol: Symbol name
            description: Backup description
            
        Returns:
            Dictionary containing backup information
        """
        try:
            print_info(f"💾 Creating backup for {symbol}...")
            
            # Create backup timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{symbol.lower()}_backup_{timestamp}"
            backup_path = self.backup_dir / backup_name
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Create backup metadata
            backup_metadata = {
                'symbol': symbol,
                'description': description,
                'created_at': datetime.now().isoformat(),
                'backup_type': 'mtf_data',
                'version': '1.0'
            }
            
            # Save MTF data
            mtf_file = backup_path / "mtf_data.pkl"
            with open(mtf_file, 'wb') as f:
                pickle.dump(mtf_data, f)
            
            # Save metadata
            metadata_file = backup_path / "metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(backup_metadata, f, indent=2)
            
            # Calculate backup size
            backup_size = self._calculate_backup_size(backup_path)
            
            # Update metadata with size
            backup_metadata['backup_size_bytes'] = backup_size
            with open(metadata_file, 'w') as f:
                json.dump(backup_metadata, f, indent=2)
            
            self.current_backup = {
                'backup_path': backup_path,
                'backup_name': backup_name,
                'metadata': backup_metadata
            }
            
            print_info(f"✅ Backup created: {backup_name} ({backup_size / 1024 / 1024:.2f} MB)")
            
            return {
                'status': 'success',
                'backup_path': str(backup_path),
                'backup_name': backup_name,
                'backup_size': backup_size,
                'metadata': backup_metadata
            }
            
        except Exception as e:
            print_error(f"Error creating backup: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def restore_backup(self, backup_name: str) -> Dict[str, Any]:
        """
        Restore data from backup.
        
        Args:
            backup_name: Name of the backup to restore
            
        Returns:
            Dictionary containing restored data
        """
        try:
            print_info(f"🔄 Restoring backup: {backup_name}...")
            
            backup_path = self.backup_dir / backup_name
            
            if not backup_path.exists():
                return {
                    'status': 'error',
                    'message': f'Backup not found: {backup_name}'
                }
            
            # Load metadata
            metadata_file = backup_path / "metadata.json"
            if not metadata_file.exists():
                return {
                    'status': 'error',
                    'message': 'Backup metadata not found'
                }
            
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            # Load MTF data
            mtf_file = backup_path / "mtf_data.pkl"
            if not mtf_file.exists():
                return {
                    'status': 'error',
                    'message': 'Backup data file not found'
                }
            
            with open(mtf_file, 'rb') as f:
                mtf_data = pickle.load(f)
            
            print_info(f"✅ Backup restored: {backup_name}")
            
            return {
                'status': 'success',
                'mtf_data': mtf_data,
                'metadata': metadata,
                'backup_path': str(backup_path)
            }
            
        except Exception as e:
            print_error(f"Error restoring backup: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def list_backups(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        List available backups.
        
        Args:
            symbol: Optional symbol filter
            
        Returns:
            Dictionary containing backup list
        """
        try:
            backups = []
            
            for backup_path in self.backup_dir.iterdir():
                if backup_path.is_dir():
                    metadata_file = backup_path / "metadata.json"
                    if metadata_file.exists():
                        try:
                            with open(metadata_file, 'r') as f:
                                metadata = json.load(f)
                            
                            # Filter by symbol if specified
                            if symbol is None or metadata.get('symbol', '').lower() == symbol.lower():
                                backup_size = self._calculate_backup_size(backup_path)
                                backups.append({
                                    'backup_name': backup_path.name,
                                    'backup_path': str(backup_path),
                                    'metadata': metadata,
                                    'backup_size': backup_size
                                })
                        except Exception as e:
                            print_debug(f"Error reading backup metadata {backup_path}: {e}")
                            continue
            
            # Sort by creation time (newest first)
            backups.sort(key=lambda x: x['metadata'].get('created_at', ''), reverse=True)
            
            return {
                'status': 'success',
                'backups': backups,
                'total_backups': len(backups)
            }
            
        except Exception as e:
            print_error(f"Error listing backups: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'backups': []
            }
    
    def delete_backup(self, backup_name: str) -> Dict[str, Any]:
        """
        Delete a backup.
        
        Args:
            backup_name: Name of the backup to delete
            
        Returns:
            Dictionary containing deletion result
        """
        try:
            print_info(f"🗑️  Deleting backup: {backup_name}...")
            
            backup_path = self.backup_dir / backup_name
            
            if not backup_path.exists():
                return {
                    'status': 'error',
                    'message': f'Backup not found: {backup_name}'
                }
            
            # Remove backup directory
            shutil.rmtree(backup_path)
            
            print_info(f"✅ Backup deleted: {backup_name}")
            
            return {
                'status': 'success',
                'message': f'Backup {backup_name} deleted successfully'
            }
            
        except Exception as e:
            print_error(f"Error deleting backup: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def cleanup_old_backups(self, keep_count: int = 5) -> Dict[str, Any]:
        """
        Clean up old backups, keeping only the specified number.
        
        Args:
            keep_count: Number of backups to keep
            
        Returns:
            Dictionary containing cleanup result
        """
        try:
            print_info(f"🧹 Cleaning up old backups (keeping {keep_count})...")
            
            # List all backups
            list_result = self.list_backups()
            if list_result['status'] != 'success':
                return list_result
            
            backups = list_result['backups']
            
            if len(backups) <= keep_count:
                return {
                    'status': 'success',
                    'message': f'No cleanup needed. Current backups: {len(backups)}'
                }
            
            # Delete old backups
            deleted_count = 0
            for backup in backups[keep_count:]:
                delete_result = self.delete_backup(backup['backup_name'])
                if delete_result['status'] == 'success':
                    deleted_count += 1
            
            print_info(f"✅ Cleanup completed. Deleted {deleted_count} old backups")
            
            return {
                'status': 'success',
                'deleted_count': deleted_count,
                'remaining_count': len(backups) - deleted_count
            }
            
        except Exception as e:
            print_error(f"Error cleaning up backups: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _calculate_backup_size(self, backup_path: Path) -> int:
        """
        Calculate backup size in bytes.
        
        Args:
            backup_path: Path to backup directory
            
        Returns:
            Backup size in bytes
        """
        try:
            total_size = 0
            for file_path in backup_path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            return total_size
        except Exception as e:
            print_debug(f"Error calculating backup size: {e}")
            return 0
    
    def validate_backup(self, backup_name: str) -> Dict[str, Any]:
        """
        Validate a backup.
        
        Args:
            backup_name: Name of the backup to validate
            
        Returns:
            Dictionary containing validation result
        """
        try:
            print_info(f"🔍 Validating backup: {backup_name}...")
            
            backup_path = self.backup_dir / backup_name
            
            if not backup_path.exists():
                return {
                    'status': 'error',
                    'message': f'Backup not found: {backup_name}'
                }
            
            # Check metadata file
            metadata_file = backup_path / "metadata.json"
            if not metadata_file.exists():
                return {
                    'status': 'error',
                    'message': 'Backup metadata not found'
                }
            
            # Check MTF data file
            mtf_file = backup_path / "mtf_data.pkl"
            if not mtf_file.exists():
                return {
                    'status': 'error',
                    'message': 'Backup data file not found'
                }
            
            # Try to load metadata
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
            except Exception as e:
                return {
                    'status': 'error',
                    'message': f'Invalid metadata file: {e}'
                }
            
            # Try to load MTF data
            try:
                with open(mtf_file, 'rb') as f:
                    mtf_data = pickle.load(f)
            except Exception as e:
                return {
                    'status': 'error',
                    'message': f'Invalid data file: {e}'
                }
            
            print_info(f"✅ Backup validated: {backup_name}")
            
            return {
                'status': 'success',
                'backup_name': backup_name,
                'metadata': metadata,
                'data_valid': True
            }
            
        except Exception as e:
            print_error(f"Error validating backup: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
