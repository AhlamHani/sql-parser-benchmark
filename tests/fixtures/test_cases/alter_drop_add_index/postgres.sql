/*
tables = ['plan']
columns = []
engine = 'postgres'
*/

DROP INDEX IF EXISTS idx__plan__city_id;

DROP INDEX IF EXISTS idx__plan__captain_id;

DROP INDEX IF EXISTS idx__plan__created_at;

DROP INDEX IF EXISTS idx__plan__status;

CREATE INDEX idx__plan__city__status__assignment__fulfillat ON plan (city_id, status, assignment_cycle_id, fulfill_at);

CREATE INDEX idx__plan__city__status__expiry ON plan (city_id, status, expires_at);
