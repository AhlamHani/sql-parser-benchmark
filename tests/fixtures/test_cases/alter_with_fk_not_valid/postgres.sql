/*
tables = ['customization_group', 'customization_group_template']
columns = []
expected-parsers = ['sqlglot']
engine = 'postgres'
*/

ALTER TABLE customization_group
    ADD CONSTRAINT customization_group_template_id_fk
        FOREIGN KEY (customization_group_template_id)
            REFERENCES customization_group_template
            ON UPDATE RESTRICT ON DELETE RESTRICT
            NOT VALID
