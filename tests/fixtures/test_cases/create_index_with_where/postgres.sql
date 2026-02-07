/*
tables = ['products']
columns = ['provider_name']
expected-parsers = []
engine = 'postgres'
*/

CREATE INDEX IF NOT EXISTS idx_product_provider_prefix
    ON products (provider_name text_pattern_ops)
    WHERE provider_name IS NOT NULL AND provider_name <> '';
