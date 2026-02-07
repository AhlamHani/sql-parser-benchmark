/*
tables = ['customization_group_template']
columns = []
expected-parsers = ['sqlglot']
engine = 'postgres'
*/

create unique index if not exists customization_group_template_merchant_id_internal_name_unique_index
    on customization_group_template (merchant_id, internal_name) where status != 'DELETED'
