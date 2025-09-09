"""
Database migrations for Pocket Hedge Fund.

This module provides database migration management for schema changes.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import os

from sqlalchemy import text, inspect
from sqlalchemy.exc import SQLAlchemyError
from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

from .connection import DatabaseManager
from .models import Base

logger = logging.getLogger(__name__)


class MigrationManager:
    """
    Database migration manager for Pocket Hedge Fund.
    
    Handles schema migrations, version control, and database updates.
    """
    
    def __init__(self, database_manager: DatabaseManager):
        """
        Initialize migration manager.
        
        Args:
            database_manager: Database manager instance
        """
        self.db_manager = database_manager
        self.alembic_cfg = None
        self._setup_alembic()
    
    def _setup_alembic(self):
        """Setup Alembic configuration."""
        try:
            # Get project root directory
            project_root = Path(__file__).parent.parent.parent.parent.parent
            alembic_dir = project_root / "alembic"
            
            # Create alembic directory if it doesn't exist
            alembic_dir.mkdir(exist_ok=True)
            
            # Setup alembic configuration
            self.alembic_cfg = Config()
            self.alembic_cfg.set_main_option("script_location", str(alembic_dir))
            self.alembic_cfg.set_main_option("sqlalchemy.url", self.db_manager.database_url)
            
            # Create alembic.ini if it doesn't exist
            alembic_ini = project_root / "alembic.ini"
            if not alembic_ini.exists():
                self._create_alembic_ini(alembic_ini)
            
            logger.info("Alembic configuration setup completed")
            
        except Exception as e:
            logger.error(f"Failed to setup Alembic: {e}")
            raise
    
    def _create_alembic_ini(self, alembic_ini_path: Path):
        """Create alembic.ini configuration file."""
        alembic_ini_content = """# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version number format
version_num_format = %04d

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses
# os.pathsep. If this key is omitted entirely, it falls back to the legacy
# behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
version_path_separator = os

# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = driver://user:pass@localhost/dbname


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the exec runner, execute a binary
# hooks = ruff
# ruff.type = exec
# ruff.executable = %(here)s/.venv/bin/ruff
# ruff.options = --fix REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""
        
        with open(alembic_ini_path, 'w') as f:
            f.write(alembic_ini_content)
        
        logger.info(f"Created alembic.ini at {alembic_ini_path}")
    
    async def init_migrations(self) -> Dict[str, Any]:
        """
        Initialize migration system.
        
        Returns:
            Dict containing initialization results
        """
        try:
            logger.info("Initializing database migrations...")
            
            # Initialize alembic
            command.init(self.alembic_cfg, "alembic")
            
            # Create initial migration
            await self.create_migration("Initial migration")
            
            logger.info("Database migrations initialized successfully")
            
            return {
                'status': 'success',
                'message': 'Database migrations initialized successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to initialize migrations: {e}")
            return {
                'status': 'error',
                'message': f'Failed to initialize migrations: {str(e)}'
            }
    
    async def create_migration(self, message: str, autogenerate: bool = True) -> Dict[str, Any]:
        """
        Create a new migration.
        
        Args:
            message: Migration message
            autogenerate: Whether to autogenerate migration from model changes
            
        Returns:
            Dict containing migration creation results
        """
        try:
            logger.info(f"Creating migration: {message}")
            
            if autogenerate:
                command.revision(
                    self.alembic_cfg,
                    message=message,
                    autogenerate=True
                )
            else:
                command.revision(
                    self.alembic_cfg,
                    message=message
                )
            
            logger.info(f"Migration created successfully: {message}")
            
            return {
                'status': 'success',
                'message': f'Migration created: {message}'
            }
            
        except Exception as e:
            logger.error(f"Failed to create migration: {e}")
            return {
                'status': 'error',
                'message': f'Failed to create migration: {str(e)}'
            }
    
    async def upgrade_database(self, revision: str = "head") -> Dict[str, Any]:
        """
        Upgrade database to specified revision.
        
        Args:
            revision: Target revision (default: "head")
            
        Returns:
            Dict containing upgrade results
        """
        try:
            logger.info(f"Upgrading database to revision: {revision}")
            
            command.upgrade(self.alembic_cfg, revision)
            
            logger.info(f"Database upgraded successfully to: {revision}")
            
            return {
                'status': 'success',
                'message': f'Database upgraded to: {revision}'
            }
            
        except Exception as e:
            logger.error(f"Failed to upgrade database: {e}")
            return {
                'status': 'error',
                'message': f'Failed to upgrade database: {str(e)}'
            }
    
    async def downgrade_database(self, revision: str) -> Dict[str, Any]:
        """
        Downgrade database to specified revision.
        
        Args:
            revision: Target revision
            
        Returns:
            Dict containing downgrade results
        """
        try:
            logger.info(f"Downgrading database to revision: {revision}")
            
            command.downgrade(self.alembic_cfg, revision)
            
            logger.info(f"Database downgraded successfully to: {revision}")
            
            return {
                'status': 'success',
                'message': f'Database downgraded to: {revision}'
            }
            
        except Exception as e:
            logger.error(f"Failed to downgrade database: {e}")
            return {
                'status': 'error',
                'message': f'Failed to downgrade database: {str(e)}'
            }
    
    async def get_current_revision(self) -> Dict[str, Any]:
        """
        Get current database revision.
        
        Returns:
            Dict containing current revision info
        """
        try:
            with self.db_manager.engine.connect() as connection:
                context = MigrationContext.configure(connection)
                current_rev = context.get_current_revision()
                
                return {
                    'status': 'success',
                    'current_revision': current_rev,
                    'message': f'Current revision: {current_rev}'
                }
                
        except Exception as e:
            logger.error(f"Failed to get current revision: {e}")
            return {
                'status': 'error',
                'message': f'Failed to get current revision: {str(e)}'
            }
    
    async def get_migration_history(self) -> Dict[str, Any]:
        """
        Get migration history.
        
        Returns:
            Dict containing migration history
        """
        try:
            script = ScriptDirectory.from_config(self.alembic_cfg)
            revisions = []
            
            for revision in script.walk_revisions():
                revisions.append({
                    'revision': revision.revision,
                    'down_revision': revision.down_revision,
                    'branch_labels': revision.branch_labels,
                    'depends_on': revision.depends_on,
                    'doc': revision.doc
                })
            
            return {
                'status': 'success',
                'revisions': revisions,
                'message': f'Found {len(revisions)} migrations'
            }
            
        except Exception as e:
            logger.error(f"Failed to get migration history: {e}")
            return {
                'status': 'error',
                'message': f'Failed to get migration history: {str(e)}'
            }
    
    async def create_tables(self) -> Dict[str, Any]:
        """
        Create all tables from models.
        
        Returns:
            Dict containing table creation results
        """
        try:
            logger.info("Creating database tables...")
            
            # Create all tables
            Base.metadata.create_all(bind=self.db_manager.engine)
            
            logger.info("Database tables created successfully")
            
            return {
                'status': 'success',
                'message': 'Database tables created successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            return {
                'status': 'error',
                'message': f'Failed to create tables: {str(e)}'
            }
    
    async def drop_tables(self) -> Dict[str, Any]:
        """
        Drop all tables.
        
        Returns:
            Dict containing table drop results
        """
        try:
            logger.info("Dropping database tables...")
            
            # Drop all tables
            Base.metadata.drop_all(bind=self.db_manager.engine)
            
            logger.info("Database tables dropped successfully")
            
            return {
                'status': 'success',
                'message': 'Database tables dropped successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to drop tables: {e}")
            return {
                'status': 'error',
                'message': f'Failed to drop tables: {str(e)}'
            }
    
    async def reset_database(self) -> Dict[str, Any]:
        """
        Reset database (drop and recreate all tables).
        
        Returns:
            Dict containing reset results
        """
        try:
            logger.info("Resetting database...")
            
            # Drop all tables
            await self.drop_tables()
            
            # Create all tables
            await self.create_tables()
            
            logger.info("Database reset successfully")
            
            return {
                'status': 'success',
                'message': 'Database reset successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to reset database: {e}")
            return {
                'status': 'error',
                'message': f'Failed to reset database: {str(e)}'
            }
