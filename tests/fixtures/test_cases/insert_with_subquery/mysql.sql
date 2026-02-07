/*
tables = ['requests', 'payments', 'stale_requests']
columns = []
expected-parsers = ['sqlglot']
engine = 'mysql'
*/

INSERT INTO stale_requests
SELECT i.transaction_id
FROM requests i
WHERE i.created_at < now() - interval '6 months'
  AND NOT EXISTS (
    SELECT 1
    FROM payments p
    WHERE p.request_id = i.transaction_id
    )
