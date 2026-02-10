/*
tables = ['master_product_domain']
columns = ['brand_id', 'domain', 'gtins']
engine = 'postgres'
*/

CREATE INDEX CONCURRENTLY IF NOT EXISTS master_product_domain_gtin_brand_id_domain_idx ON master_product_domain
    USING GIN (brand_id, domain, gtins jsonb_path_ops) WHERE gtins IS NOT NULL AND gtins <> 'null'::jsonb;
