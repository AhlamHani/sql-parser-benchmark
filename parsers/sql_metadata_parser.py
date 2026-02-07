"""sql_metadata parser wrapper."""
from sql_metadata import Parser


class SQLMetadataParser:
    def __init__(self, engine='postgres'):
        self.engine = engine  # Not used, sql_metadata is engine-agnostic
    
    def extract_tables(self, query):
        try:
            parser = Parser(query)
            tables = [table.split('.')[-1] for table in parser.tables]
            return sorted(set(tables))
        except Exception:
            return []
    
    def extract_columns(self, query):
        try:
            parser = Parser(query)
            columns = [col.split('.')[-1] for col in parser.columns]
            return sorted(set(columns))
        except Exception:
            return []
