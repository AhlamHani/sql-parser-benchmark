/*
tables = []
columns = []
expected-parsers = []
engine = 'mysql'
*/

CREATE TABLE IF NOT EXISTS `rescheduled_evaluation_events` (
  `captain_id`             INT           NOT NULL,
  `last_ended_cycle`       INT           NOT NULL,
  `new_loyalty_cycle_id`   INT           NOT NULL,
  `scheduled_at`           TIMESTAMP     NOT NULL,
  `created_at`             TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `processed`              TINYINT(1)    NOT NULL DEFAULT 0,

  UNIQUE KEY `uk_rescheduled_evaluation_events` (
    `captain_id`,
    `last_ended_cycle`,
    `new_loyalty_cycle_id`
  ),

  KEY `idx_rescheduled_evaluation_events_processed` (`processed`),
  KEY `idx_rescheduled_evaluation_events_scheduled_at` (`scheduled_at`)
)
