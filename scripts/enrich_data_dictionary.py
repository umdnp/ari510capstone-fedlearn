#!/usr/bin/env python3
"""
Enrich DATA_DICTIONARY.md with additional column information from web scrape.
New column order: Column Name | Data Type | Null | Description | Key
"""

import re
from pathlib import Path
from collections import defaultdict

# Paths
project_root = Path(__file__).parent.parent
base_dict_path = project_root / "docs" / "DATA_DICTIONARY.md"
web_scrape_path = project_root / "docs" / "data_dictionary_web_scrape.md"
output_path = project_root / "docs" / "DATA_DICTIONARY_ENRICHED.md"


def parse_base_dictionary():
    """Parse DATA_DICTIONARY.md to get base table structure."""
    tables = {}
    current_table = None
    current_section = None
    in_table_def = False

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
                'row_count': '',
                'columns': []
            }
            in_table_def = False
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

        # Look for column table header
        if current_table and '| Column Name | Data Type |' in line:
            in_table_def = True
            i += 2  # Skip header separator line
            continue

        # Parse column rows
        if current_table and in_table_def and line.startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            # parts[0] is empty, parts[1] is column name, parts[2] is data type, parts[3] is empty
            if len(parts) >= 3 and parts[1] and parts[2]:
                col_name = parts[1]
                col_type = parts[2]
                if col_name != 'Column Name':  # Skip header row if we hit it again
                    tables[current_table]['columns'].append({
                        'name': col_name,
                        'type': col_type
                    })
            i += 1
            continue

        # Stop reading columns when we hit a non-table line
        if in_table_def and not line.startswith('|'):
            in_table_def = False

        i += 1

    return tables


def parse_web_scrape():
    """Parse web scrape to extract Null, Description, and Key for each column."""
    # Structure: table_name -> column_name -> {null, description, key}
    enrichment_data = defaultdict(dict)
    current_table = None

    with open(web_scrape_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')

        # Look for table name (single line followed by empty or "Purpose:")
        if (line.strip() and
            not line.startswith(' ') and
            not line.startswith('http') and
            not line.startswith('Purpose:') and
            not line.startswith('Links to:') and
            not line.startswith('Important') and
            not line.startswith('Table columns') and
            not line.startswith('Detailed') and
            len(line.strip().split()) <= 3):

            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line == '' or next_line.startswith('Purpose:'):
                    current_table = line.strip().lower()

        # Look for "Table columns" section
        if 'Table columns' in line and current_table:
            i += 1
            if i >= len(lines):
                break

            # Next line should be header
            header_line = lines[i].rstrip('\n')
            if 'Name' in header_line and 'Datatype' in header_line:
                i += 1
                # Parse column rows
                while i < len(lines):
                    col_line = lines[i].rstrip('\n')

                    # Stop at empty line or new section
                    if (not col_line.strip() or
                        col_line.strip().startswith('http') or
                        col_line.strip().startswith('Detailed') or
                        col_line.strip().startswith('Purpose:')):
                        break

                    # Try tab split first, then space split
                    parts = col_line.split('\t')
                    non_empty = [p.strip() for p in parts if p.strip()]

                    if len(non_empty) <= 1:
                        parts = re.split(r'\s{4,}', col_line)
                        non_empty = [p.strip() for p in parts if p.strip()]

                    if len(non_empty) >= 3:
                        # Column name might have embedded datatype or spaces - extract just the name
                        raw_col_name = non_empty[0]
                        # Split by multiple spaces or tabs to get just the column name
                        col_name_parts = re.split(r'\s{2,}', raw_col_name)
                        col_name = col_name_parts[0].strip().lower()

                        # Correct index mapping based on debug output:
                        # [0]: Name, [1]: Null Option, [2]: Description, [3]: Is Key + S/T/C
                        null_option = non_empty[1] if len(non_empty) > 1 else ''
                        description = non_empty[2] if len(non_empty) > 2 else ''
                        key_and_stc = non_empty[3] if len(non_empty) > 3 else ''

                        # Extract just PK or FK from the key_and_stc field
                        is_key = ''
                        if 'PK' in key_and_stc:
                            is_key = 'PK'
                        elif 'FK' in key_and_stc:
                            is_key = 'FK'

                        enrichment_data[current_table][col_name] = {
                            'null': null_option,
                            'description': description,
                            'key': is_key
                        }

                    i += 1
                continue

        i += 1

    return enrichment_data


def generate_enriched_markdown(base_tables, enrichment):
    """Generate enriched markdown with merged data."""
    lines = []

    # Header
    lines.append("# eICU-CRD Data Dictionary (Enriched)\n")
    lines.append("This data dictionary combines schema information with detailed descriptions from eICU-CRD documentation.\n")
    lines.append("## Column Legend\n")
    lines.append("- **Null**: Indicates if the column can contain NULL values")
    lines.append("- **Description**: Detailed description of the column's purpose and content")
    lines.append("- **Key**: Indicates if the column is a Primary Key (PK) or Foreign Key (FK)\n")
    lines.append("---\n")

    # Process tables in order from base dictionary
    for table_name, table_info in base_tables.items():
        if not table_info['columns']:
            continue

        # Table header
        lines.append(f"### {table_name}\n")

        if table_info['description']:
            lines.append(f"**Description:** {table_info['description']}\n")

        if table_info['row_count']:
            lines.append(f"**Row Count:** {table_info['row_count']}\n")

        # Column table
        lines.append("| Column Name | Data Type | Null | Description | Key |")
        lines.append("|-------------|-----------|------|-------------|-----|")

        for col in table_info['columns']:
            col_name = col['name']
            col_type = col['type']

            # Look up enrichment data
            enrich = enrichment.get(table_name, {}).get(col_name.lower(), {})
            null_val = enrich.get('null', '')
            desc_val = enrich.get('description', '')
            key_val = enrich.get('key', '')

            lines.append(f"| {col_name} | {col_type} | {null_val} | {desc_val} | {key_val} |")

        lines.append("")

    return '\n'.join(lines)


def main():
    print("Parsing base dictionary (DATA_DICTIONARY.md)...")
    base_tables = parse_base_dictionary()
    print(f"Found {len(base_tables)} tables in base dictionary")

    print("\nParsing web scrape for enrichment data...")
    enrichment = parse_web_scrape()
    print(f"Found enrichment data for {len(enrichment)} tables")

    print("\nGenerating enriched data dictionary...")
    output = generate_enriched_markdown(base_tables, enrichment)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"\nEnriched data dictionary written to: {output_path}")

    # Show sample statistics
    total_cols = sum(len(t['columns']) for t in base_tables.values())
    enriched_cols = sum(
        sum(1 for col in table_info['columns']
            if col['name'].lower() in enrichment.get(table_name, {}))
        for table_name, table_info in base_tables.items()
    )
    print(f"\nStatistics:")
    print(f"  Total columns: {total_cols}")
    print(f"  Enriched columns: {enriched_cols}")
    if total_cols > 0:
        print(f"  Coverage: {enriched_cols/total_cols*100:.1f}%")
    else:
        print(f"  Coverage: N/A (no columns found in base dictionary)")


if __name__ == "__main__":
    main()
