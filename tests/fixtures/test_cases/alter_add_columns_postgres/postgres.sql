/*
tables = ['communications']
columns = []
engine = 'postgres'
*/

ALTER TABLE "communications"
    ADD COLUMN IF NOT EXISTS label_type VARCHAR(255) NULL,
    ADD COLUMN IF NOT EXISTS label_url VARCHAR(255) NULL,
    ADD COLUMN IF NOT EXISTS label_text VARCHAR(255) NULL;
