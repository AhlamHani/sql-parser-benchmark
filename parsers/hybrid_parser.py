"""
Hybrid SQL parser combining sqlglot and sql_metadata with filtering.
Achieves highest accuracy by leveraging strengths of both parsers.
"""

import logging
import sqlglot
from sql_metadata import Parser as SQLMetadataParser


class HybridParser:
    """
    Hybrid parser that combines sqlglot and sql_metadata with keyword filtering.
    """
    
    # SQL keywords that parsers incorrectly identify as tables
    SQL_KEYWORDS = {
        'ADD', 'RESTRICT', 'CASCADE', 'IF', 'NOT', 'EXISTS', 'NULL', 'DEFAULT',
        'CURRENT_TIMESTAMP', 'ON', 'UPDATE', 'DELETE', 'SET', 'WHERE', 'AND', 'OR',
        'USING', 'FORCE', 'INDEX', 'KEY', 'UNIQUE', 'PRIMARY', 'FOREIGN',
    }
    
    # Common table aliases to filter out
    COMMON_ALIASES = {'sap', 'i', 'p', 't', 'iv', 'ranked', 'duplicates'}
    
    # Postgres operator classes
    POSTGRES_OPCLASSES = {'text_pattern_ops', 'varchar_pattern_ops', 'bpchar_pattern_ops'}
    
    def __init__(self, engine='postgres'):
        """
        Initialize parser with database engine.
        
        Args:
            engine: Database engine ('mysql' or 'postgres')
        """
        self.engine = engine
    
    def extract_tables(self, query):
        """
        Extract table names from SQL query.
        
        Args:
            query: SQL query string
            
        Returns:
            Sorted list of table names
        """
        candidates = set()
        
        # Strategy 1: sqlglot (engine-aware)
        candidates.update(self._extract_sqlglot(query))
        
        # Strategy 2: sql_metadata (engine-agnostic fallback)
        candidates.update(self._extract_sql_metadata(query))
        
        # Filter out noise
        candidates = self._filter_keywords(candidates)
        
        # Engine-specific filtering
        if self.engine == 'postgres':
            candidates = {t for t in candidates if t not in self.POSTGRES_OPCLASSES}
        
        return sorted(list(candidates))
    
    def _extract_sqlglot(self, query):
        """Extract tables using sqlglot."""
        try:
            parsed = sqlglot.parse_one(query, read=self.engine)
            
            # Handle ALTER statements specially to get FK references
            if parsed.key.upper() == "ALTER":
                tables = set()
                if hasattr(parsed, 'this') and parsed.this:
                    tables.add(parsed.this.name)
                # Also get FK reference tables
                for table_expr in parsed.find_all(sqlglot.exp.Table):
                    if table_expr.name:
                        tables.add(table_expr.name)
                return tables
            
            # Standard table extraction
            return {table.name for table in parsed.find_all(sqlglot.exp.Table) if table.name}
        except Exception as e:
            logging.debug(f"sqlglot failed: {e}")
            return set()
    
    def _extract_sql_metadata(self, query):
        """Extract tables using sql_metadata."""
        try:
            parser = SQLMetadataParser(query)
            tables = set()
            for table in parser.tables:
                # Handle schema.table format
                parts = table.split('.')
                if len(parts) == 2:
                    tables.add(parts[0])  # schema
                    tables.add(parts[1])  # table
                else:
                    tables.add(table)
            return tables
        except Exception as e:
            logging.debug(f"sql_metadata failed: {e}")
            return set()
    
    def _filter_keywords(self, candidates):
        """Filter out SQL keywords and common aliases."""
        filtered = {t for t in candidates if t.upper() not in self.SQL_KEYWORDS}
        filtered = {t for t in filtered if t not in self.COMMON_ALIASES}
        filtered = {t for t in filtered if not t.upper().startswith('IF ')}
        filtered = {t for t in filtered if t.upper() != 'IF NOT EXISTS'}
        return filtered
