/*
tables = ['config_templates']
columns = []
expected-parsers = ['sqlglot']
engine = 'postgres'
*/

create unique index if not exists config_template_partner_id_internal_name_unique_index
    on config_templates (partner_id, internal_name) where status != 'DELETED'
