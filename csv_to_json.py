"""
CSV to JSON Converter

This script converts a CSV file into a JSON file.

Usage:
    python csv_to_json.py <input_csv> <output_json>

Example:
    python csv_to_json.py data.csv output.json

Dependencies:
    - pandas

Install dependencies:
    pip install pandas

### Instructions for Novice Users ###
- Ensure the input CSV file is properly formatted with a header row.
- The script reads the CSV file and converts each row into a JSON object.
- The output JSON file will be structured as a list of dictionaries, each representing a row in the CSV file.

### Warnings ###
- Ensure the CSV file does not contain duplicate column names.
- If the CSV contains numeric values, they will be automatically converted to numbers in JSON.
- Special characters in column names will be preserved but may affect JSON parsing in certain applications.

Author: @jordyarms, gpt-4o
"""

import pandas as pd
import argparse

def csv_to_json(input_csv, output_json):
    """
    Convert a CSV file into a JSON file.
    
    Args:
        input_csv (str): Path to the input CSV file.
        output_json (str): Path to the output JSON file.
    """
    try:
        df = pd.read_csv(input_csv)
        df.to_json(output_json, orient='records', indent=4)
        print(f"JSON file created at {output_json}")
    except Exception as e:
        print(f"Error converting CSV to JSON: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a CSV file to JSON format.')
    parser.add_argument('input_csv', type=str, help='Path to the input CSV file')
    parser.add_argument('output_json', type=str, help='Path to the output JSON file')
    
    args = parser.parse_args()
    csv_to_json(args.input_csv, args.output_json)
