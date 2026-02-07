"""Hybrid parser combining multiple strategies."""
import re
import sqlglot
from sql_metadata import Parser as SQLMetadataParser
import sqlparse
from sqlparse.tokens import Keyword


class HybridParser:
    """Combines all parsers to achieve maximum accuracy."""
    
    def __init__(self, engine='postgres'):
        self.engine = engine
    
    def extract_tables(self, query):
        # Get results from each parser
        sqlglot_tables = self._extract_sqlglot(query)
        metadata_tables = self._extract_sql_metadata(query)
        sqlparse_tables = self._extract_sqlparse(query)
        
        candidates = set()
        candidates.update(sqlglot_tables)
        candidates.update(metadata_tables)
        candidates.update(sqlparse_tables)
        
        # Filter using parser consensus and context
        filtered = self._filter_noise(candidates, sqlglot_tables, metadata_tables, sqlparse_tables, query)
        
        return sorted(list(filtered))
    
    def _extract_sqlglot(self, query):
        """Extract using sqlglot."""
        tables = set()
        try:
            parsed = sqlglot.parse_one(query, read=self.engine)
            
            if parsed.key.upper() == "ALTER":
                if hasattr(parsed, 'this') and parsed.this:
                    tables.add(parsed.this.name)
                for t in parsed.find_all(sqlglot.exp.Table):
                    if t.name and t.name != parsed.this.name:
                        tables.add(t.name)
                return tables
            
            if parsed.key.upper() == "CREATE" and hasattr(parsed, 'kind') and parsed.kind and parsed.kind.upper() == "TABLE":
                return tables
            
            for t in parsed.find_all(sqlglot.exp.Table):
                if t.name:
                    tables.add(t.name)
        except:
            pass
        return tables
    
    def _extract_sql_metadata(self, query):
        """Extract using sql_metadata."""
        tables = set()
        try:
            if query.strip().upper().startswith('CREATE TABLE'):
                return tables
            
            parser = SQLMetadataParser(query)
            for table in parser.tables:
                parts = table.split('.')
                if len(parts) == 2:
                    tables.add(parts[1])
                else:
                    tables.add(table)
        except:
            pass
        return tables
    
    def _extract_sqlparse(self, query):
        """Extract using sqlparse."""
        tables = set()
        try:
            parsed = sqlparse.parse(query)[0]
            tokens = list(parsed.flatten())
            
            for i, token in enumerate(tokens):
                if token.ttype is Keyword and token.value.upper() in ('FROM', 'JOIN', 'INTO', 'UPDATE', 'TABLE'):
                    for j in range(i + 1, len(tokens)):
                        next_token = tokens[j]
                        if next_token.ttype not in (sqlparse.tokens.Whitespace, sqlparse.tokens.Newline):
                            if next_token.ttype in (sqlparse.tokens.Name, None):
                                name = next_token.value.strip('`"\'')
                                if name and not self._is_keyword(name):
                                    tables.add(name)
                            break
        except:
            pass
        return tables
    
    def _filter_noise(self, candidates, sqlglot_tables, metadata_tables, sqlparse_tables, query):
        """Filter using parser consensus and context analysis."""
        keywords = {
            'ADD', 'RESTRICT', 'CASCADE', 'IF', 'NOT', 'EXISTS', 'NULL', 'DEFAULT',
            'CURRENT_TIMESTAMP', 'ON', 'UPDATE', 'DELETE', 'SET', 'WHERE', 'AND', 'OR',
            'USING', 'FORCE', 'INDEX', 'KEY', 'UNIQUE', 'PRIMARY', 'FOREIGN', 'REFERENCES',
            'CONSTRAINT', 'CHECK', 'ALGORITHM', 'INPLACE', 'LOCK', 'NONE', 'AFTER',
            'FIRST', 'LAST', 'BEFORE', 'COLUMN', 'COLUMNS', 'VALUES', 'VALUE',
        }
        
        opclasses = {'text_pattern_ops', 'varchar_pattern_ops', 'bpchar_pattern_ops'}
        
        filtered = set()
        for t in candidates:
            if t.upper() in keywords or t in opclasses:
                continue
            if ' ' in t or t.upper().startswith('IF '):
                continue
            if len(t) == 1:
                continue
            
            # Parser consensus: count how many parsers found it
            found_by = sum([t in sqlglot_tables, t in metadata_tables, t in sqlparse_tables])
            
            # If 2+ parsers agree, it's likely real
            if found_by >= 2:
                filtered.add(t)
                continue
            
            # If only 1 parser found it, apply stricter checks
            if found_by == 1:
                # Skip if it's a subquery alias
                if re.search(r'\)\s+(AS\s+)?' + re.escape(t) + r'\b', query, re.IGNORECASE):
                    continue
                # Always keep if found by sqlglot (most reliable)
                if t in sqlglot_tables:
                    filtered.add(t)
                    continue
                # Keep if has schema prefix
                if re.search(r'\w+\.' + re.escape(t) + r'\b', query, re.IGNORECASE):
                    filtered.add(t)
                    continue
                # Keep if appears after table keywords
                if re.search(r'\b(FROM|JOIN|INTO|UPDATE|TABLE|ON)\s+' + re.escape(t) + r'\b', query, re.IGNORECASE):
                    filtered.add(t)
                    continue
        
        return filtered
    
    def _is_keyword(self, word):
        """Check if word is a SQL keyword."""
        keywords = {
            'SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER',
            'ON', 'AND', 'OR', 'NOT', 'IN', 'EXISTS', 'BETWEEN', 'LIKE', 'IS',
            'NULL', 'TRUE', 'FALSE', 'AS', 'DISTINCT', 'ALL', 'ANY', 'SOME',
            'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'CREATE',
            'ALTER', 'DROP', 'TABLE', 'INDEX', 'VIEW', 'DATABASE', 'SCHEMA',
        }
        return word.upper() in keywords
