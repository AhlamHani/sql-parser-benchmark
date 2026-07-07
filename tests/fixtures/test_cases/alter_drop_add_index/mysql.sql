/*
tables = ['plan']
columns = []
engine = 'mysql'
*/

ALTER TABLE plan DROP INDEX `idx__plan__city_id`;

ALTER TABLE plan DROP INDEX `idx__plan__captain_id`;

ALTER TABLE plan DROP INDEX `idx__plan__created_at`;

ALTER TABLE plan DROP INDEX `idx__plan__status`;

ALTER TABLE plan
    ADD INDEX `idx__plan__city__status__assignment__fulfillat` (city_id, status, assignment_cycle_id, fulfill_at);

ALTER TABLE plan
    ADD INDEX `idx__plan__city__status__expiry` (city_id, status, expires_at);
