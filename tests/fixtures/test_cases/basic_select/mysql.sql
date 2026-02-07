/*
tables = ['users']
columns = ['name', 'age']
expected-parsers = ['sqlglot', 'sql_metadata', 'jsqlparser']
engine = 'mysql'
*/

SELECT name, age FROM users WHERE age > 21