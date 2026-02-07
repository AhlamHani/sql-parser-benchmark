"""sqlglot parser wrapper."""
import sqlglot


class SQLGlotParser:
    def __init__(self, engine='postgres'):
        self.engine = engine
    
    def extract_tables(self, query):
        try:
            parsed = sqlglot.parse_one(query, read=self.engine)
            tables = [table.name for table in parsed.find_all(sqlglot.exp.Table) if table.name]
            return sorted(set(tables))
        except Exception:
            return []
    
    def extract_columns(self, query):
        try:
            parsed = sqlglot.parse_one(query, read=self.engine)
            columns = set()
            
            # For INSERT with column list, get from Schema node
            for schema in parsed.find_all(sqlglot.exp.Schema):
                for expr in schema.expressions:
                    if isinstance(expr, sqlglot.exp.Identifier):
                        columns.add(expr.name)
            
            # For other queries, get from Column nodes
            for col in parsed.find_all(sqlglot.exp.Column):
                if col.name:
                    columns.add(col.name)
            
            return sorted(columns)
        except Exception:
            return []
