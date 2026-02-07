/*
tables = ['order_events']
columns = []
engine = 'mysql'
*/

ALTER TABLE `order_events`
    MODIFY COLUMN `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '[NOT-PII]',
    MODIFY COLUMN `order_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '[NOT-PII]';
