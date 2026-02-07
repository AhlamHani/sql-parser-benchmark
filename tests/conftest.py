"""Pytest configuration and utilities."""
import os


def parse_query_file(file_path):
    """Parse SQL test file with metadata."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        parsed_data = {}
        query_lines = []
        in_comment_block = False

        for line in lines:
            line = line.strip()
            if line.startswith('/*'):
                in_comment_block = True
            elif line.endswith('*/'):
                in_comment_block = False
            elif in_comment_block:
                if '=' in line:
                    key, value = line.split('=', 1)
                    parsed_data[key.strip()] = eval(value.strip())
            else:
                query_lines.append(line.strip())

        parsed_data["query"] = ' '.join(query_lines).strip()
        return parsed_data
