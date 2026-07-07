/*
tables = ['adherence_records']
columns = []
expected-parsers = ['sqlglot']
engine = 'mysql'
*/

DELETE sar
FROM performance.adherence_records sar
JOIN (
    SELECT id
    FROM (
        SELECT 
            id,
            ROW_NUMBER() OVER (
                PARTITION BY shift_adherence_id, period_start_timestamp
                ORDER BY TIMESTAMPDIFF(SECOND, period_start_timestamp, period_end_timestamp) DESC
            ) AS row_num
        FROM performance.adherence_records
    ) ranked
    WHERE row_num > 1
) duplicates ON sar.id = duplicates.id
