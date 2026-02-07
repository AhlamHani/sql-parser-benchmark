#!/usr/bin/env python3
"""
Benchmark comparison script that generates RESULTS.md
"""
import os
from datetime import datetime
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
    
    results = {name: {'correct': 0, 'total': 0, 'mysql': 0, 'postgres': 0, 'mysql_correct': 0, 'postgres_correct': 0, 'failures': []} 
               for name in parsers}
    
    for case in cases:
        expected = sorted(case['tables'])
        engine = case['engine']
        
        for parser_name, ParserClass in parsers.items():
            parser = ParserClass(engine=engine)
            try:
                result = parser.extract_tables(case['query'])
                results[parser_name]['total'] += 1
                
                if engine == 'mysql':
                    results[parser_name]['mysql'] += 1
                    if result == expected:
                        results[parser_name]['mysql_correct'] += 1
                else:
                    results[parser_name]['postgres'] += 1
                    if result == expected:
                        results[parser_name]['postgres_correct'] += 1
                
                if result == expected:
                    results[parser_name]['correct'] += 1
                else:
                    results[parser_name]['failures'].append(case['test_id'])
            except Exception as e:
                results[parser_name]['total'] += 1
                results[parser_name]['failures'].append(f"{case['test_id']} (error: {str(e)[:50]})")
    
    return results


def generate_markdown(results):
    """Generate RESULTS.md file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    md = f"""# SQL Parser Benchmark Results

**Last Updated**: {timestamp}

## Library Versions

| Library | Version |
|---------|----------|
| sqlglot | {sqlglot.__version__} |
| sql-metadata | {importlib.metadata.version('sql-metadata')} |
| sqlparse | {sqlparse.__version__} |

## Overall Accuracy

| Parser | Overall | MySQL | PostgreSQL | Failures |
|--------|---------|-------|------------|----------|
"""
    
    # Sort by overall accuracy
    sorted_results = sorted(results.items(), key=lambda x: x[1]['correct'], reverse=True)
    
    for parser_name, stats in sorted_results:
        overall_pct = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        mysql_pct = (stats['mysql_correct'] / stats['mysql'] * 100) if stats['mysql'] > 0 else 0
        postgres_pct = (stats['postgres_correct'] / stats['postgres'] * 100) if stats['postgres'] > 0 else 0
        
        md += f"| **{parser_name}** | **{stats['correct']}/{stats['total']} ({overall_pct:.1f}%)** | "
        md += f"{stats['mysql_correct']}/{stats['mysql']} ({mysql_pct:.1f}%) | "
        md += f"{stats['postgres_correct']}/{stats['postgres']} ({postgres_pct:.1f}%) | "
        md += f"{len(stats['failures'])} |\n"
    
    md += "\n## Detailed Failures\n\n"
    
    for parser_name, stats in sorted_results:
        if stats['failures']:
            md += f"### {parser_name}\n\n"
            for failure in stats['failures']:
                md += f"- `{failure}`\n"
            md += "\n"
    
    md += """
## Test Coverage

- **Total Test Cases**: {total}
- **MySQL Tests**: {mysql}
- **PostgreSQL Tests**: {postgres}

## Parser Details

### hybrid
- **Approach**: Combined strategies with filtering
- **Strengths**: Handles edge cases
- **Weaknesses**: More complex

### sqlglot
- **Approach**: AST-based parsing with engine awareness
- **Strengths**: Best single parser, handles complex queries
- **Weaknesses**: Fails on some MySQL-specific syntax

### sql_metadata
- **Approach**: Regex-based parsing, engine-agnostic
- **Strengths**: Fast, handles MySQL hints
- **Weaknesses**: Misses FK references, limited CREATE INDEX support

### sqlparse
- **Approach**: Tokenization-based parsing
- **Strengths**: Lightweight, pure Python
- **Weaknesses**: Limited table extraction capabilities

---

*This file is auto-generated by CI. Do not edit manually.*
""".format(
        total=results['sqlglot']['total'],
        mysql=results['sqlglot']['mysql'],
        postgres=results['sqlglot']['postgres']
    )
    
    return md


def main():
    """Main entry point."""
    print("Running SQL Parser Benchmark...")
    print("=" * 80)
    
    results = run_benchmark()
    
    # Print to console
    print("\nResults:")
    for parser_name, stats in sorted(results.items(), key=lambda x: x[1]['correct'], reverse=True):
        accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"  {parser_name:15s}: {stats['correct']:2d}/{stats['total']:2d} ({accuracy:5.1f}%)")
    
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
