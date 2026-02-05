"""
Convert JSON to CSV

This script reads a JSON file and converts it into a CSV file.

Usage:
    python json_to_csv.py <input_json> <output_csv>

Example:
    python json_to_csv.py events.json output.csv

Dependencies:
    - json
    - csv

### Additional Notes ###
- Ensure that the JSON file contains a valid list of objects.
- If the JSON file does not contain a list of dictionaries, it will be skipped.

Author: @jordyarms, gpt-4o
"""

import json
import csv
import argparse

def json_to_csv(input_json, output_csv):
    """
    Convert a JSON file to a CSV file.
    
    Args:
        input_json (str): Path to the JSON file.
        output_csv (str): Path to the output CSV file.
    """
    try:
        with open(input_json, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            
            # Ensure JSON data is a list of dictionaries
            if isinstance(json_data, dict):
                json_data = [json_data]
            
            if isinstance(json_data, list) and all(isinstance(item, dict) for item in json_data):
                # Extract headers dynamically
                headers = set()
                for row in json_data:
                    headers.update(row.keys())
                headers = sorted(headers)
                
                # Write data to CSV
                with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.DictWriter(csvfile, fieldnames=headers)
                    csv_writer.writeheader()
                    csv_writer.writerows(json_data)
                
                print(f"CSV file created at {output_csv}")
            else:
                print("Invalid JSON structure. Expected a list of dictionaries.")
    except json.JSONDecodeError:
        print("Invalid JSON file format.")
    except FileNotFoundError:
        print(f"File not found: {input_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a JSON file to CSV.')
    parser.add_argument('input_json', type=str, help='Path to the input JSON file')
    parser.add_argument('output_csv', type=str, help='Path to the output CSV file')
    
    args = parser.parse_args()
    json_to_csv(args.input_json, args.output_csv)
