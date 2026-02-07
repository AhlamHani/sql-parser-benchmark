/*
tables = ['config_groups', 'config_templates']
columns = []
expected-parsers = ['sqlglot']
engine = 'postgres'
*/

ALTER TABLE config_groups
    ADD CONSTRAINT config_template_id_fk
        FOREIGN KEY (config_template_id)
            REFERENCES config_templates
            ON UPDATE RESTRICT ON DELETE RESTRICT
            NOT VALID
