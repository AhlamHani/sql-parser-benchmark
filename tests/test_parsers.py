"""Main test suite for SQL parser benchmarking."""
import os
import pytest
from conftest import parse_query_file
from parsers import HybridParser, SQLGlotParser, SQLMetadataParser, SQLParseParser


def load_test_cases():
    """Load all test cases from fixtures."""
    base = os.path.join(os.path.dirname(__file__), "fixtures", "test_cases")
    cases = []
    ids = []
    
    for query_folder in sorted(os.listdir(base)):
        query_path = os.path.join(base, query_folder)
        if not os.path.isdir(query_path):
            continue
        
        for engine_file in sorted(os.listdir(query_path)):
            if not engine_file.endswith('.sql'):
                continue
            
            engine = os.path.splitext(engine_file)[0]
            filepath = os.path.join(query_path, engine_file)
            
            data = parse_query_file(filepath)
            data['engine'] = engine
            
            cases.append(data)
            ids.append(f"{query_folder}_{engine}")
    
    return ids, cases


TEST_IDS, TEST_CASES = load_test_cases()


@pytest.mark.parametrize("case", TEST_CASES, ids=TEST_IDS)
def test_hybrid_parser(case):
    """Test hybrid parser."""
    parser = HybridParser(engine=case['engine'])
    result = parser.extract_tables(case['query'])
    assert result == sorted(case['tables']), f"Expected {case['tables']}, got {result}"


@pytest.mark.parametrize("case", TEST_CASES, ids=TEST_IDS)
def test_sqlglot_parser(case):
    """Test sqlglot parser."""
    parser = SQLGlotParser(engine=case['engine'])
    result = parser.extract_tables(case['query'])
    # Don't assert, just collect results for benchmark


@pytest.mark.parametrize("case", TEST_CASES, ids=TEST_IDS)
def test_sql_metadata_parser(case):
    """Test sql_metadata parser."""
    parser = SQLMetadataParser(engine=case['engine'])
    result = parser.extract_tables(case['query'])
    # Don't assert, just collect results for benchmark


@pytest.mark.parametrize("case", TEST_CASES, ids=TEST_IDS)
def test_sqlparse_parser(case):
    """Test sqlparse parser."""
    parser = SQLParseParser(engine=case['engine'])
    result = parser.extract_tables(case['query'])
    # Don't assert, just collect results for benchmark
