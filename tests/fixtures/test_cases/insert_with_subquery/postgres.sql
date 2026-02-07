/*
tables = ['inquiries', 'payments', 'tmp_stale_inquiries']
columns = []
expected-parsers = ['sqlglot']
engine = 'postgres'
*/

INSERT INTO tmp_stale_inquiries
SELECT i.transaction_id
FROM inquiries i
WHERE i.created_at < now() - interval '6 months'
  AND NOT EXISTS (
    SELECT 1
    FROM payments p
    WHERE p.inquiry_id = i.transaction_id
    )
