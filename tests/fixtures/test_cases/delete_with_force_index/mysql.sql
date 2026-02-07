/*
tables = ['events']
columns = ['expiration']
expected-parsers = ['sql_metadata']
engine = 'mysql'
*/

DELETE FROM events
  FORCE INDEX (idx_expiration)
WHERE expiration <= (now() - INTERVAL 30 MINUTE)
ORDER BY expiration;
