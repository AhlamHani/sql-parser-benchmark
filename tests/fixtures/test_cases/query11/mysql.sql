/*
tables = ['sample_delete_table']
columns = ['expiration']
expected-parsers = ['sql_metadata']
engine = 'mysql'
*/

DELETE FROM sample_delete_table
  FORCE INDEX (idx_expiration)
WHERE expiration <= (now() - INTERVAL 30 MINUTE)
ORDER BY expiration;
