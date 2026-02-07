/*
tables = ['captain_performance', 'shift_adherence_period']
columns = []
expected-parsers = ['sqlglot']
engine = 'mysql'
*/

DELETE sap
FROM captain_performance.shift_adherence_period sap
JOIN (
    SELECT id
    FROM (
        SELECT 
            id,
            ROW_NUMBER() OVER (
                PARTITION BY captain_shift_adherence_id, period_start_timestamp
                ORDER BY TIMESTAMPDIFF(SECOND, period_start_timestamp, period_end_timestamp) DESC
            ) AS row_num
        FROM captain_performance.shift_adherence_period
    ) ranked
    WHERE row_num > 1
) duplicates ON sap.id = duplicates.id
