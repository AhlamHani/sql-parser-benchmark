/*
tables = ['users']
columns = ['age', 'name']
expected-parsers = ['sql_metadata', 'sqlglot']
engine = 'mysql'
*/


UPDATE users SET age = age + 1 WHERE name = 'John'