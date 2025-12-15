"""
Database module for AES grading system.
Provides SQLite-based checkpoint and resume functionality.
"""

from .db_manager import DatabaseManager

__all__ = ['DatabaseManager']
