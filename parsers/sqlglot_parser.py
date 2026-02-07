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
            columns = [col.name for col in parsed.find_all(sqlglot.exp.Column) if col.name]
            return sorted(set(columns))
        except Exception:
            return []
