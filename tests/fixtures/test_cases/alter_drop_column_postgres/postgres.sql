/*
tables = ['user_communications']
columns = []
engine = 'postgres'
*/

ALTER TABLE "user_communications" DROP COLUMN IF EXISTS sender_id;
