/*
tables = ['items']
columns = []
engine = 'mysql'
*/

CREATE INDEX IF NOT EXISTS idx_items_uuid ON items (uuid) ALGORITHM=INSTANT;
