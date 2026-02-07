"""sqlparse parser wrapper."""
import sqlparse


class SQLParseParser:
    def __init__(self, engine='postgres'):
        self.engine = engine
    
    def extract_tables(self, query):
        try:
            tables = set()
            parsed = sqlparse.parse(query)[0]
            
            from_seen = False
            for token in parsed.tokens:
                if token.ttype is sqlparse.tokens.Keyword and token.value.upper() in ('FROM', 'JOIN', 'INTO', 'TABLE', 'UPDATE'):
                    from_seen = True
                elif from_seen and isinstance(token, sqlparse.sql.Identifier):
                    tables.add(token.get_real_name())
                    from_seen = False
                elif from_seen and token.ttype is sqlparse.tokens.Name:
                    tables.add(token.value)
                    from_seen = False
            
            return sorted(tables)
        except Exception:
            return []
