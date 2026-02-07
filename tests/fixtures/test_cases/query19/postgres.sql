/*
tables = ['inquiry_inputs_value', 'tmp_stale_inquiries']
columns = []
expected-parsers = ['sqlglot']
engine = 'postgres'
*/

DELETE FROM inquiry_inputs_value iv
    USING tmp_stale_inquiries t
WHERE iv.inquiry_transaction_id = t.transaction_id
