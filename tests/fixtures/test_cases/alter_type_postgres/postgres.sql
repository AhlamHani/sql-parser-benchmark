/*
tables = ['taxonomy_category']
columns = []
engine = 'postgres'
*/

ALTER TABLE taxonomy_category 
  ALTER COLUMN id TYPE uuid USING category_uuid,
  ALTER COLUMN parent_id TYPE uuid USING NULL,
  DROP COLUMN IF EXISTS category_uuid;
