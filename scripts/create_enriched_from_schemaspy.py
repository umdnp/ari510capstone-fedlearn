#!/usr/bin/env python3
"""
Create enriched data dictionary using schemaspy.csv data.
Merges with DATA_DICTIONARY.md for descriptions and row counts.
"""

import csv
from pathlib import Path
from collections import defaultdict

# Paths
project_root = Path(__file__).parent.parent
base_dict_path = project_root / "docs" / "DATA_DICTIONARY.md"
schemaspy_path = project_root / "docs" / "schemaspy.csv"
output_path = project_root / "docs" / "DATA_DICTIONARY_ENRICHED.md"


def parse_base_dictionary():
    """Parse DATA_DICTIONARY.md to get descriptions and row counts."""
    tables = {}
    current_table = None

    with open(base_dict_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')

        # Look for table headers like "### patient"
        if line.startswith('### '):
            table_name = line[4:].strip().lower()
            current_table = table_name
            tables[current_table] = {
                'description': '',
                'row_count': ''
            }
            i += 1
            continue

        # Look for Description line
        if current_table and line.startswith('**Description:**'):
            desc = line.replace('**Description:**', '').strip()
            tables[current_table]['description'] = desc
            i += 1
            continue

        # Look for Row Count line
        if current_table and line.startswith('**Row Count:**'):
            count = line.replace('**Row Count:**', '').strip()
            tables[current_table]['row_count'] = count
            i += 1
            continue

        i += 1

    return tables


def parse_schemaspy_csv():
    """Parse schemaspy.csv to extract table and column information."""
    # Structure: table_name -> [{column_info}, ...]
    tables = defaultdict(list)
    current_table = None

    with open(schemaspy_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            # Skip empty rows
            if not any(row):
                continue

            # Check if this is a table header row
            if row[0].startswith('Table '):
                # Extract table name from "Table eicu.eicu_crd.tablename"
                table_full = row[0].replace('Table ', '').strip()
                if 'eicu_crd.' in table_full:
                    current_table = table_full.split('eicu_crd.')[1].lower()
                continue

            # Check if this is the column header row
            if row[0] == 'Column':
                continue

            # This is a data row
            if current_table and row[0]:  # row[0] is the column name
                col_name = row[0].strip().lower()
                col_type = row[1].strip() if len(row) > 1 else ''
                col_size = row[2].strip() if len(row) > 2 else ''
                col_nulls = row[3].strip() if len(row) > 3 else ''
                col_parents = row[7].strip() if len(row) > 7 else ''

                # Determine nullable
                nullable = 'NULL' if col_nulls == '√' else 'NOT NULL'

                # Determine if FK
                is_fk = 'FK' if col_parents else ''

                # Determine if PK (typically the first column ending in 'id' without a parent)
                is_pk = ''
                if not is_fk and col_name.endswith('id'):
                    # Likely a PK - we'll mark the first id column as PK
                    if not tables[current_table]:  # First column for this table
                        is_pk = 'PK'

                # Build full type name
                if col_size:
                    full_type = f"{col_type}({col_size})"
                else:
                    full_type = col_type

                # Determine key value
                key = is_pk if is_pk else is_fk

                tables[current_table].append({
                    'name': col_name,
                    'type': full_type,
                    'nullable': nullable,
                    'key': key
                })

    return dict(tables)


def generate_enriched_markdown(base_tables, schemaspy_tables):
    """Generate enriched markdown combining both sources."""
    lines = []

    # Header
    lines.append("# eICU-CRD Data Dictionary (Enriched)\n")
    lines.append("This data dictionary combines schema information with detailed metadata from the eICU-CRD database.\n")
    lines.append("## Column Legend\n")
    lines.append("- **Nullable**: Indicates if the column can contain NULL values (NULL or NOT NULL)")
    lines.append("- **Description**: Detailed description of the column's purpose and content")
    lines.append("- **Key**: Indicates if the column is a Primary Key (PK) or Foreign Key (FK)\n")
    lines.append("---\n")

    # Process tables - use order from base dictionary
    for table_name in sorted(base_tables.keys()):
        table_info = base_tables[table_name]

        # Get columns from schemaspy
        columns = schemaspy_tables.get(table_name, [])
        if not columns:
            continue

        # Table header
        lines.append(f"### {table_name}\n")

        if table_info['description']:
            lines.append(f"**Description:** {table_info['description']}\n")

        if table_info['row_count']:
            lines.append(f"**Row Count:** {table_info['row_count']}\n")

        lines.append(f"**Columns:** {len(columns)}\n")

        # Column table
        lines.append("| Column Name | Data Type | Nullable | Key |")
        lines.append("|-------------|-----------|----------|-----|")

        for col in columns:
            col_name = col['name']
            col_type = col['type']
            nullable = col['nullable']
            key = col['key']

            lines.append(f"| {col_name} | {col_type} | {nullable} | {key} |")

        lines.append("")

    return '\n'.join(lines)


def main():
    print("Parsing base dictionary (DATA_DICTIONARY.md)...")
    base_tables = parse_base_dictionary()
    print(f"Found {len(base_tables)} tables in base dictionary")

    print("\nParsing schemaspy.csv...")
    schemaspy_tables = parse_schemaspy_csv()
    print(f"Found {len(schemaspy_tables)} tables in schemaspy.csv")

    # Show which tables match
    matching = set(base_tables.keys()) & set(schemaspy_tables.keys())
    print(f"Matching tables: {len(matching)}")

    print("\nGenerating enriched data dictionary...")
    output = generate_enriched_markdown(base_tables, schemaspy_tables)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"\nEnriched data dictionary written to: {output_path}")

    # Show statistics
    total_cols = sum(len(cols) for cols in schemaspy_tables.values())
    fk_count = sum(
        sum(1 for col in cols if col['key'] == 'FK')
        for cols in schemaspy_tables.values()
    )
    pk_count = sum(
        sum(1 for col in cols if col['key'] == 'PK')
        for cols in schemaspy_tables.values()
    )

    print(f"\nStatistics:")
    print(f"  Total columns: {total_cols}")
    print(f"  Primary keys: {pk_count}")
    print(f"  Foreign keys: {fk_count}")


if __name__ == "__main__":
    main()
