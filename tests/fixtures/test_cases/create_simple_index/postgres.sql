/*
tables = ['options_template']
columns = []
expected-parsers = ['sqlglot']
engine = 'postgres'
*/

create index if not exists options_template_group_template_id_index
    on options_template (group_template_id)
