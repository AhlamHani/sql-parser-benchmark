/*
tables = ['campaign_request']
columns = ['requested_by', 'status']
engine = 'postgres'
*/

CREATE TYPE campaign_request_type AS ENUM ('create_campaign', 'update_campaign'); CREATE TYPE campaign_request_status AS ENUM ('PENDING', 'APPROVED', 'REJECTED', 'CLOSED'); CREATE TABLE IF NOT EXISTS campaign_request ( id BIGSERIAL PRIMARY KEY, type campaign_request_type NOT NULL, payload JSONB NOT NULL, status campaign_request_status NOT NULL DEFAULT 'PENDING', target_campaign_id BIGINT, requested_by BIGINT NOT NULL, reviewed_by BIGINT, reviewed_at TIMESTAMP, rejection_reason TEXT, result_campaign_id BIGINT, created_at TIMESTAMP NOT NULL DEFAULT clock_timestamp(), updated_at TIMESTAMP NOT NULL DEFAULT clock_timestamp() ); CREATE INDEX idx_campaign_request_status ON campaign_request (status); CREATE INDEX idx_campaign_request_requested_by ON campaign_request (requested_by);
