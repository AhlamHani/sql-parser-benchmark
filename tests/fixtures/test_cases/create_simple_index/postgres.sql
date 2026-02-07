/*
tables = ['option_templates']
columns = []
expected-parsers = ['sqlglot']
engine = 'postgres'
*/

create index if not exists option_template_config_template_id_index
    on option_templates (config_template_id)
