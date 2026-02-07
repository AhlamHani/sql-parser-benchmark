/*
tables = ['request_values', 'stale_requests']
columns = []
expected-parsers = ['sqlglot']
engine = 'postgres'
*/

DELETE FROM request_values iv
    USING stale_requests t
WHERE iv.request_transaction_id = t.transaction_id
