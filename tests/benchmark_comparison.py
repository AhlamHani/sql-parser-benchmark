#!/usr/bin/env python3
"""
Benchmark comparison script that generates RESULTS.md
"""
import os
from conftest import parse_query_file
from parsers import SQLGlotParser, SQLMetadataParser, SQLParseParser, HybridParser
import sqlglot
import sqlparse
import importlib.metadata


def load_test_cases():
    """Load all test cases."""
    base = os.path.join(os.path.dirname(__file__), "fixtures", "test_cases")
    cases = []
    
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
            data['test_id'] = f"{query_folder}_{engine}"
            
            cases.append(data)
    
    return cases


def run_benchmark():
    """Run benchmark and collect results."""
    cases = load_test_cases()
    
    parsers = {
        'hybrid': HybridParser,
        'sqlglot': SQLGlotParser,
        'sql_metadata': SQLMetadataParser,
        'sqlparse': SQLParseParser,
    }
    
    results = {name: {
        'tables_correct': 0, 'tables_total': 0,
        'columns_correct': 0, 'columns_total': 0,
        'mysql': 0, 'postgres': 0,
        'mysql_correct': 0, 'postgres_correct': 0,
        'table_failures': [], 'column_failures': []
    } for name in parsers}
    
    for case in cases:
        expected_tables = sorted(case['tables'])
        expected_columns = sorted(case['columns'])
        engine = case['engine']
        
        for parser_name, ParserClass in parsers.items():
            parser = ParserClass(engine=engine)
            
            # Test tables
            try:
                result_tables = parser.extract_tables(case['query'])
                results[parser_name]['tables_total'] += 1
                
                if engine == 'mysql':
                    results[parser_name]['mysql'] += 1
                    if result_tables == expected_tables:
                        results[parser_name]['mysql_correct'] += 1
                else:
                    results[parser_name]['postgres'] += 1
                    if result_tables == expected_tables:
                        results[parser_name]['postgres_correct'] += 1
                
                if result_tables == expected_tables:
                    results[parser_name]['tables_correct'] += 1
                else:
                    results[parser_name]['table_failures'].append(case['test_id'])
            except Exception as e:
                results[parser_name]['tables_total'] += 1
                results[parser_name]['table_failures'].append(f"{case['test_id']} (error)")
            
            # Test columns (only for parsers that support it)
            if hasattr(parser, 'extract_columns'):
                try:
                    result_columns = parser.extract_columns(case['query'])
                    results[parser_name]['columns_total'] += 1
                    
                    if result_columns == expected_columns:
                        results[parser_name]['columns_correct'] += 1
                    else:
                        results[parser_name]['column_failures'].append(case['test_id'])
                except Exception as e:
                    results[parser_name]['columns_total'] += 1
                    results[parser_name]['column_failures'].append(f"{case['test_id']} (error)")
    
    return results


def generate_markdown(results):
    """Generate RESULTS.md file."""
    md = f"""# SQL Parser Benchmark Results

## Library Versions

| Library | Version |
|---------|----------|
| sqlglot | {sqlglot.__version__} |
| sql-metadata | {importlib.metadata.version('sql-metadata')} |
| sqlparse | {sqlparse.__version__} |

## Table Extraction Accuracy

| Parser | Overall | MySQL | PostgreSQL | Failures |
|--------|---------|-------|------------|----------|
"""
    
    # Sort by table accuracy
    sorted_results = sorted(results.items(), key=lambda x: x[1]['tables_correct'], reverse=True)
    
    for parser_name, stats in sorted_results:
        overall_pct = (stats['tables_correct'] / stats['tables_total'] * 100) if stats['tables_total'] > 0 else 0
        mysql_pct = (stats['mysql_correct'] / stats['mysql'] * 100) if stats['mysql'] > 0 else 0
        postgres_pct = (stats['postgres_correct'] / stats['postgres'] * 100) if stats['postgres'] > 0 else 0
        
        md += f"| **{parser_name}** | **{stats['tables_correct']}/{stats['tables_total']} ({overall_pct:.1f}%)** | "
        md += f"{stats['mysql_correct']}/{stats['mysql']} ({mysql_pct:.1f}%) | "
        md += f"{stats['postgres_correct']}/{stats['postgres']} ({postgres_pct:.1f}%) | "
        md += f"{len(stats['table_failures'])} |\n"
    
    md += "\n## Column Extraction Accuracy\n\n| Parser | Overall | Failures |\n|--------|---------|----------|\n"
    
    # Sort by column accuracy
    sorted_by_columns = sorted(results.items(), key=lambda x: x[1]['columns_correct'], reverse=True)
    
    for parser_name, stats in sorted_by_columns:
        if stats['columns_total'] > 0:
            col_pct = (stats['columns_correct'] / stats['columns_total'] * 100)
            md += f"| **{parser_name}** | **{stats['columns_correct']}/{stats['columns_total']} ({col_pct:.1f}%)** | "
            md += f"{len(stats['column_failures'])} |\n"
    
    md += "\n## Detailed Failures\n\n### Table Extraction\n\n"
    
    for parser_name, stats in sorted_results:
        if stats['table_failures']:
            md += f"#### {parser_name}\n\n"
            for failure in stats['table_failures']:
                md += f"- `{failure}`\n"
            md += "\n"
    
    md += "### Column Extraction\n\n"
    
    for parser_name, stats in sorted_by_columns:
        if stats['column_failures']:
            md += f"#### {parser_name}\n\n"
            for failure in stats['column_failures']:
                md += f"- `{failure}`\n"
            md += "\n"
    
    md += "\n---\n\n*Auto-generated by CI*"
    
    return md


def main():
    """Main entry point."""
    print("Running SQL Parser Benchmark...")
    print("=" * 80)
    
    results = run_benchmark()
    
    # Print to console
    print("\nTable Extraction Results:")
    for parser_name, stats in sorted(results.items(), key=lambda x: x[1]['tables_correct'], reverse=True):
        accuracy = (stats['tables_correct'] / stats['tables_total'] * 100) if stats['tables_total'] > 0 else 0
        print(f"  {parser_name:15s}: {stats['tables_correct']:2d}/{stats['tables_total']:2d} ({accuracy:5.1f}%)")
    
    print("\nColumn Extraction Results:")
    for parser_name, stats in sorted(results.items(), key=lambda x: x[1]['columns_correct'], reverse=True):
        if stats['columns_total'] > 0:
            accuracy = (stats['columns_correct'] / stats['columns_total'] * 100)
            print(f"  {parser_name:15s}: {stats['columns_correct']:2d}/{stats['columns_total']:2d} ({accuracy:5.1f}%)")
    
    # Generate markdown
    md_content = generate_markdown(results)
    
    # Write to RESULTS.md
    output_path = os.path.join(os.path.dirname(__file__), "..", "RESULTS.md")
    with open(output_path, 'w') as f:
        f.write(md_content)
    
    print(f"\n✅ Results written to {output_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
