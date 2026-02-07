/*
tables = ['product']
columns = ['manufacturer_name']
expected-parsers = []
engine = 'postgres'
*/

CREATE INDEX IF NOT EXISTS idx_product_manufacturer_prefix
    ON product (manufacturer_name text_pattern_ops)
    WHERE manufacturer_name IS NOT NULL AND manufacturer_name <> '';
