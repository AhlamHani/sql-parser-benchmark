# SQL Parser Benchmark

[![Tests](https://github.com/AhlamHani/sql-parser-benchmark/actions/workflows/benchmark.yml/badge.svg)](https://github.com/AhlamHani/sql-parser-benchmark/actions/workflows/benchmark.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive benchmark comparing popular Python SQL parsers for table extraction accuracy across MySQL and PostgreSQL dialects.

## 🎯 Purpose

This benchmark evaluates how well different SQL parsers can extract table names from SQL queries, which is critical for:
- Query analysis and optimization tools
- Database migration utilities
- SQL linting and validation
- Dependency tracking systems

## 📊 Results

See [RESULTS.md](RESULTS.md) for detailed benchmark results and accuracy metrics.

## 🧪 Test Coverage

### Test Categories

- **Universal Queries** (18 tests): Work on both MySQL and PostgreSQL
  - SELECT, INSERT, UPDATE, DELETE
  - ALTER TABLE (basic operations)
  - CREATE INDEX (standard syntax)

- **MySQL-Specific** (14 tests):
  - `FORCE INDEX` hints
  - `ADD INDEX` syntax
  - `UNSIGNED` types
  - `AFTER column_name` positioning
  - Backtick identifiers

- **PostgreSQL-Specific** (15 tests):
  - `DELETE ... USING` syntax
  - Operator classes (`text_pattern_ops`)
  - `IF NOT EXISTS` with CREATE INDEX
  - `NOT VALID` constraints
  - Schema-qualified tables

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/AhlamHani/sql-parser-benchmark.git
cd sql-parser-benchmark

# Install with uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Or with pip
pip install .
```

### Run Benchmarks

```bash
# Run all benchmarks
pytest tests/ -v

# Run comparison report
python tests/benchmark_comparison.py

# Run specific engine tests
pytest tests/ -k mysql
pytest tests/ -k postgres
```

## 📁 Project Structure

```
sql-parser-benchmark/
├── tests/
│   ├── fixtures/
│   │   └── test_cases/
│   │       ├── basic_select/
│   │       │   ├── mysql.sql
│   │       │   └── postgres.sql
│   │       ├── alter_add_column/
│   │       │   ├── mysql.sql
│   │       │   └── postgres.sql
│   │       └── ...
│   ├── test_parsers.py           # Main test suite
│   ├── benchmark_comparison.py   # Comparison script
│   └── conftest.py               # Pytest configuration
├── parsers/
│   ├── __init__.py
│   ├── sqlglot_parser.py
│   ├── sql_metadata_parser.py
│   └── sqlparse_parser.py
├── .github/
│   └── workflows/
│       └── benchmark.yml         # CI/CD pipeline
├── pyproject.toml
├── uv.lock
├── README.md
└── RESULTS.md                    # Auto-generated results
```

## 🔬 Parsers Tested

- sqlglot
- sql_metadata
- sqlparse

## 🧩 Test Case Format

Each test case is organized by query type with engine-specific files:

```sql
/*
tables = ['users', 'orders']
columns = ['user_id', 'order_id']
engine = 'mysql'
*/

SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';
```

## 🤝 Contributing

Contributions are welcome! To add new test cases:

1. Create a new folder under `tests/fixtures/test_cases/`
2. Add `mysql.sql` and/or `postgres.sql` files
3. Include metadata comment block with expected tables
4. Run tests to verify: `pytest tests/ -v`
5. Submit a pull request

## 📈 CI/CD

GitHub Actions automatically:
- Runs all tests on every push
- Generates comparison report
- Updates `RESULTS.md` with latest benchmarks
- Publishes results as workflow artifacts

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [sqlglot](https://github.com/tobymao/sqlglot) - SQL parser and transpiler
- [sql-metadata](https://github.com/macbre/sql-metadata) - SQL query metadata parser
- [sqlparse](https://github.com/andialbrecht/sqlparse) - Non-validating SQL parser

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.
