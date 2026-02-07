/*
tables = ['users']
columns = ['age']
expected-parsers = ['sql_metadata', 'sqlglot']
engine = 'mysql'
*/


DELETE FROM users WHERE age < 18;