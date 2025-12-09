#!/usr/bin/env python3
"""
Fix the DATA_DICTIONARY_ENRICHED.md file to correct column alignment.
Specifically, ensure S/T/C values appear in the correct column.
"""

import re
from pathlib import Path

# Paths
project_root = Path(__file__).parent.parent
web_scrape_path = project_root / "docs" / "data_dictionary_web_scrape.md"
output_path = project_root / "docs" / "DATA_DICTIONARY_ENRICHED.md"

def parse_web_scrape():
    """Parse the web scrape file to extract table information."""
    tables = {}
    current_table = None
    current_columns = []

    with open(web_scrape_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')

        # Look for "Table columns" marker
        if 'Table columns' in line:
            # Next line should be the header
            i += 1
            if i >= len(lines):
                break

            header_line = lines[i].rstrip('\n')

            # Verify this is the header
            if 'Name' in header_line and 'Datatype' in header_line:
                # Start parsing column rows
                i += 1
                col_count = 0
                while i < len(lines):
                    col_line = lines[i].rstrip('\n')

                    # Stop at empty line, URL, or new section
                    if (not col_line.strip() or
                        col_line.strip().startswith('http') or
                        col_line.strip().startswith('Detailed') or
                        col_line.strip().startswith('Purpose:')):
                        break

                    # Split by tabs first, if that gives us only 1 part, try splitting by multiple spaces
                    parts = col_line.split('\t')
                    non_empty_parts = [p.strip() for p in parts if p.strip()]

                    # If tab-split didn't work, try splitting by multiple spaces (4+ spaces)
                    if len(non_empty_parts) <= 1:
                        parts = re.split(r'\s{4,}', col_line)
                        non_empty_parts = [p.strip() for p in parts if p.strip()]

                    if len(non_empty_parts) >= 4:
                        col_name = non_empty_parts[0]
                        col_type = non_empty_parts[1]
                        null_option = non_empty_parts[2]
                        comment = non_empty_parts[3]

                        # Is Key (PK, FK, or empty)
                        is_key = non_empty_parts[4] if len(non_empty_parts) > 4 else ''

                        # S/T/C (Stored/Transformed/Created)
                        stc = non_empty_parts[5] if len(non_empty_parts) > 5 else ''

                        # If is_key looks like S/T/C value and stc is empty, swap them
                        if is_key in ['S', 'T', 'C', 'All'] and not stc:
                            is_key, stc = '', is_key

                        current_columns.append({
                            'name': col_name,
                            'type': col_type,
                            'null': null_option,
                            'comment': comment,
                            'key': is_key,
                            'stc': stc
                        })
                        col_count += 1

                    i += 1

                # Save the table with its columns
                if current_table and current_columns:
                    tables[current_table] = current_columns
                    current_columns = []
                    # Don't reset current_table - it might be updated before next "Table columns"

                continue

        # Check for table name - single line followed by empty or Purpose
        if (line.strip() and
            not line.startswith(' ') and
            not line.startswith('http') and
            not line.startswith('Purpose:') and
            not line.startswith('Links to:') and
            not line.startswith('Important considerations') and
            not line.startswith('Table columns') and
            not line.startswith('Detailed description') and
            not line.startswith('#') and
            len(line.strip().split()) <= 3):  # Table names are usually 1-3 words

            # Check next line
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line == '' or next_line.startswith('Purpose:'):
                    # This is likely a table name
                    current_table = line.strip()

        i += 1

    # Save last table if any
    if current_table and current_columns:
        tables[current_table] = current_columns

    return tables

def generate_markdown_table(table_name, columns):
    """Generate markdown table for a given table."""
    lines = []

    # Add table header
    lines.append(f"### {table_name}")
    lines.append("")

    # Add column table header
    lines.append("| Column Name | Data Type | Null | Key | S/T/C | Description |")
    lines.append("|-------------|-----------|------|-----|-------|-------------|")

    # Add column rows
    for col in columns:
        name = col['name']
        dtype = col['type']
        null = col['null']
        key = col['key']
        stc = col['stc']
        desc = col['comment']

        lines.append(f"| {name} | {dtype} | {null} | {key} | {stc} | {desc} |")

    lines.append("")
    return '\n'.join(lines)

def main():
    """Main function to regenerate the enriched data dictionary."""
    print("Parsing web scrape file...")
    tables = parse_web_scrape()

    print(f"Found {len(tables)} tables")
    for table_name in sorted(tables.keys()):
        print(f"  - {table_name}: {len(tables[table_name])} columns")

    # Generate the markdown file
    print("\nGenerating enriched data dictionary...")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# eICU-CRD Data Dictionary (Enriched)\n\n")
        f.write("This data dictionary combines database schema information with detailed descriptions from the eICU-CRD documentation.\n\n")
        f.write("## Column Legend\n\n")
        f.write("- **Null**: Indicates if the column can contain NULL values\n")
        f.write("- **Key**: Indicates if the column is a Primary Key (PK) or Foreign Key (FK)\n")
        f.write("- **S/T/C**: Indicates if the data is:\n")
        f.write("  - **S** = Stored: Data stored directly as entered\n")
        f.write("  - **T** = Transformed: Data transformed from entered values\n")
        f.write("  - **C** = Created: Data created by the system (e.g., IDs, calculated values)\n")
        f.write("\n---\n\n")

        # Write tables in alphabetical order
        for table_name in sorted(tables.keys()):
            columns = tables[table_name]
            table_md = generate_markdown_table(table_name, columns)
            f.write(table_md)
            f.write("\n")

    print(f"\nEnriched data dictionary written to: {output_path}")

if __name__ == "__main__":
    main()
