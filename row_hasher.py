"""
Row Hasher

This script reads a CSV or TSV file and appends an MD5 hash of each row's
contents as a new column. Rows are streamed one at a time, so it handles
large files without loading them entirely into memory.

Usage:
    python row_hasher.py <input_file> <output_file>
    python row_hasher.py <input_file> <output_file> -d tab
    python row_hasher.py <input_file> <output_file> --column-name id

Example:
    python row_hasher.py data.csv hashed.csv
    python row_hasher.py data.tsv hashed.tsv -d tab
    python row_hasher.py data.csv hashed.csv --column-name row_hash

Dependencies:
    - csv
    - hashlib

### Additional Notes ###
- The delimiter defaults to comma. Use `-d tab` for TSV files.
- The hash column name defaults to "row_id" but can be changed with --column-name.
- Each hash is computed from the concatenated cell values of the row, joined
  by the file's delimiter, and encoded as UTF-8 before hashing.
- Rows are streamed, so this works well with large files.

Author: @jordyarms, claude-opus-4-5
"""

import csv
import hashlib
import argparse


def hash_row(values, delimiter):
    """
    Generate an MD5 hex digest from a row's cell values.

    Args:
        values (list): The cell values for a single row.
        delimiter (str): The delimiter used to join values before hashing.

    Returns:
        str: The MD5 hex digest of the joined row.
    """
    joined = delimiter.join(values)
    return hashlib.md5(joined.encode('utf-8')).hexdigest()


def row_hasher(input_file, output_file, delimiter=',', column_name='row_id'):
    """
    Read a delimited file, compute an MD5 hash for each row, and write
    the result with the hash appended as a new column.

    Args:
        input_file (str): Path to the input CSV/TSV file.
        output_file (str): Path to the output file.
        delimiter (str): Column delimiter (',' or '\\t').
        column_name (str): Name of the appended hash column.
    """
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
             open(output_file, 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.reader(infile, delimiter=delimiter)
            writer = csv.writer(outfile, delimiter=delimiter)

            # Write header with new column
            header = next(reader)
            writer.writerow(header + [column_name])

            # Stream rows
            for row in reader:
                row_hash = hash_row(row, delimiter)
                writer.writerow(row + [row_hash])

        print(f"Hashed file created at {output_file}")
    except FileNotFoundError:
        print(f"File not found: {input_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Append an MD5 row hash to each row of a CSV or TSV file.'
    )
    parser.add_argument('input_file', type=str, help='Path to the input CSV/TSV file')
    parser.add_argument('output_file', type=str, help='Path to the output file')
    parser.add_argument(
        '-d', '--delimiter', type=str, default=',',
        choices=[',', 'tab'],
        help="Column delimiter: ',' (default) or 'tab' for TSV"
    )
    parser.add_argument(
        '--column-name', type=str, default='row_id',
        help="Name of the hash column (default: row_id)"
    )

    args = parser.parse_args()

    delim = '\t' if args.delimiter == 'tab' else args.delimiter
    row_hasher(args.input_file, args.output_file, delimiter=delim, column_name=args.column_name)
