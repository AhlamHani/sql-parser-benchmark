"""Tests for HybridParser methods not covered by the fixture-driven suite.

extract_table_schemas() was ported over from the storage-shared-workflows
sibling copy of this parser -- it maps a table name to the schema it's
explicitly qualified with in the query (e.g. `partman.part_config`), which
callers use to distinguish that from the migration's own declared schema.
"""
from parsers import HybridParser


class TestExtractTableSchemas:
    def test_maps_explicitly_qualified_table_to_its_schema(self):
        parser = HybridParser(engine="postgres")

        schemas = parser.extract_table_schemas(
            "DELETE FROM partman.part_config WHERE parent_table = 'case_management.interaction'"
        )

        assert schemas == {"part_config": "partman"}

    def test_omits_tables_referenced_without_a_schema_qualifier(self):
        parser = HybridParser(engine="postgres")

        schemas = parser.extract_table_schemas("SELECT * FROM orders")

        assert schemas == {}

    def test_returns_empty_mapping_on_unparseable_input(self):
        parser = HybridParser(engine="postgres")

        schemas = parser.extract_table_schemas("not valid sql (((")

        assert schemas == {}
