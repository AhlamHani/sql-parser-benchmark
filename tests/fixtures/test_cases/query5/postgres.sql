/*
tables = ['users']
columns = ['age']
expected-parsers = ['sql_metadata', 'sqlglot']
engine = 'postgres'
*/


DELETE FROM users WHERE age < 18;