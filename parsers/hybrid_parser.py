"""Hybrid parser combining multiple strategies."""
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
        
        # Get aliases from sqlglot AST
        aliases = self._extract_aliases(query)
        
        # Filter using parser consensus and AST analysis
        filtered = self._filter_noise(candidates, sqlglot_tables, metadata_tables, sqlparse_tables, aliases)
        
        return sorted(list(filtered))
    
    def extract_columns(self, query):
        # Get results from parsers that support column extraction
        sqlglot_columns = self._extract_columns_sqlglot(query)
        metadata_columns = self._extract_columns_sql_metadata(query)
        
        candidates = set()
        candidates.update(sqlglot_columns)
        candidates.update(metadata_columns)
        
        # Check if query is DDL without column references
        try:
            parsed = sqlglot.parse_one(query, read=self.engine)
            key = parsed.key.upper()
            
            # Skip columns for DDL that doesn't reference columns
            if key == 'ALTER':
                # ALTER DROP COLUMN and CREATE INDEX with WHERE do reference columns
                if not any(x in query.upper() for x in ['DROP COLUMN', 'ADD COLUMN', 'MODIFY COLUMN']):
                    return []
            elif key == 'CREATE':
                # CREATE INDEX with WHERE clause references columns
                if 'WHERE' not in query.upper():
                    return []
            elif key == 'DROP':
                return []
        except:
            pass
        
        # Filter using consensus
        filtered = self._filter_column_noise(candidates, sqlglot_columns, metadata_columns)
        
        return sorted(list(filtered))
    
    def _extract_sqlglot(self, query):
        """Extract using sqlglot."""
        tables = set()
        try:
            parsed = sqlglot.parse_one(query, read=self.engine)
            
            if parsed.key.upper() == "DROP":
                if hasattr(parsed, 'kind') and parsed.kind and parsed.kind.upper() == "INDEX":
                    return tables
            
            if parsed.key.upper() == "ALTER":
                if hasattr(parsed, 'this') and parsed.this:
                    tables.add(parsed.this.name)
                for t in parsed.find_all(sqlglot.exp.Table):
                    if t.name and t.name != parsed.this.name:
                        tables.add(t.name)
                return tables
            
            if parsed.key.upper() == "CREATE":
                if hasattr(parsed, 'kind') and parsed.kind and parsed.kind.upper() == "TABLE":
                    return tables
                if hasattr(parsed, 'kind') and parsed.kind and parsed.kind.upper() == "INDEX":
                    for idx in parsed.find_all(sqlglot.exp.Index):
                        for t in idx.find_all(sqlglot.exp.Table):
                            if t.name:
                                tables.add(t.name)
                    return tables
            
            if parsed.key.upper() == "COMMAND":
                if 'CREATE' in query.upper() and 'INDEX' in query.upper() and 'ON' in query.upper():
                    import re
                    match = re.search(r'\bON\s+([`"]?\w+[`"]?)', query, re.IGNORECASE)
                    if match:
                        tables.add(match.group(1).strip('`"'))
                    return tables
            
            for t in parsed.find_all(sqlglot.exp.Table):
                if t.name:
                    tables.add(t.name)
                if hasattr(t, 'db') and t.db:
                    tables.add(t.db)
                if hasattr(t, 'catalog') and t.catalog:
                    tables.add(t.catalog)
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
    
    def _extract_columns_sqlglot(self, query):
        """Extract columns using sqlglot."""
        columns = set()
        try:
            parsed = sqlglot.parse_one(query, read=self.engine)
            
            # For INSERT with column list, get from Schema node
            for schema in parsed.find_all(sqlglot.exp.Schema):
                for expr in schema.expressions:
                    if isinstance(expr, sqlglot.exp.Identifier):
                        columns.add(expr.name)
            
            # For other queries, get from Column nodes
            for col in parsed.find_all(sqlglot.exp.Column):
                if col.name:
                    columns.add(col.name)
        except:
            pass
        return columns
    
    def _extract_columns_sql_metadata(self, query):
        """Extract columns using sql_metadata."""
        columns = set()
        try:
            parser = SQLMetadataParser(query)
            for col in parser.columns:
                # Remove table qualification
                parts = col.split('.')
                columns.add(parts[-1])
        except:
            pass
        return columns
    
    def _extract_aliases(self, query):
        """Extract table aliases using sqlglot AST."""
        aliases = set()
        try:
            parsed = sqlglot.parse_one(query, read=self.engine)
            
            # Find all table aliases
            for table_expr in parsed.find_all(sqlglot.exp.Table):
                if table_expr.alias:
                    aliases.add(table_expr.alias)
            
            # Find subquery aliases
            for subquery in parsed.find_all(sqlglot.exp.Subquery):
                if subquery.alias:
                    aliases.add(subquery.alias)
            
            # Find CTE aliases
            for cte in parsed.find_all(sqlglot.exp.CTE):
                if cte.alias:
                    aliases.add(cte.alias)
        except:
            pass
        return aliases
    
    def _filter_noise(self, candidates, sqlglot_tables, metadata_tables, sqlparse_tables, aliases):
        """Filter using parser consensus and AST analysis."""
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
            # Skip keywords and operator classes
            if t.upper() in keywords or t in opclasses:
                continue
            if ' ' in t or t.upper().startswith('IF '):
                continue
            if len(t) == 1:
                continue
            
            # Skip if it's a known alias
            if t in aliases:
                continue
            
            # Parser consensus: count how many parsers found it
            found_by = sum([t in sqlglot_tables, t in metadata_tables, t in sqlparse_tables])
            
            # If 2+ parsers agree, it's likely real
            if found_by >= 2:
                filtered.add(t)
                continue
            
            # If only 1 parser found it, trust sqlglot
            if found_by == 1 and t in sqlglot_tables:
                filtered.add(t)
                continue
        
        return filtered
    
    def _filter_column_noise(self, candidates, sqlglot_columns, metadata_columns):
        """Filter columns using parser consensus."""
        filtered = set()
        for col in candidates:
            if len(col) == 0:
                continue
            
            # Parser consensus: count how many parsers found it
            found_by = sum([col in sqlglot_columns, col in metadata_columns])
            
            # If both parsers agree, it's real
            if found_by >= 2:
                filtered.add(col)
                continue
            
            # If only 1 parser found it, trust sqlglot
            if found_by == 1 and col in sqlglot_columns:
                filtered.add(col)
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
