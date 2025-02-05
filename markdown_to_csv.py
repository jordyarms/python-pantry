"""
Convert Markdown Frontmatter to CSV

This script reads the YAML front matter from a folder of Markdown files and converts it into a CSV file.

Usage:
    python markdown_to_csv.py <markdown_folder> <output_csv>

Example:
    python markdown_to_csv.py markdown_files output.csv

Dependencies:
    - pyyaml
    - csv

Install dependencies:
    pip install pyyaml

Author: @jordyarms, gpt-4o
"""

import os
import csv
import yaml
import argparse

def markdown_to_csv(markdown_folder, output_csv):
    """
    Convert YAML front matter from Markdown files to a CSV file.
    
    Args:
        markdown_folder (str): Path to the folder containing Markdown files.
        output_csv (str): Path to the output CSV file.
    """
    rows = []
    
    # Loop through each markdown file in the folder
    for filename in os.listdir(markdown_folder):
        if filename.endswith('.md'):
            file_path = os.path.join(markdown_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                # Read the YAML front matter from each markdown file
                content = file.read().split('---')
                if len(content) > 1:
                    yaml_data = yaml.safe_load(content[1])
                    if isinstance(yaml_data, dict):
                        rows.append(yaml_data)
    
    if rows:
        # Extract headers dynamically from all YAML keys
        headers = set()
        for row in rows:
            headers.update(row.keys())
        headers = sorted(headers)
        
        # Write data to CSV
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerows(rows)
        
        print(f"CSV file created at {output_csv}")
    else:
        print("No valid YAML front matter found in Markdown files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Markdown Frontmatter to CSV.')
    parser.add_argument('markdown_folder', type=str, help='Path to the folder containing Markdown files')
    parser.add_argument('output_csv', type=str, help='Path to the output CSV file')
    
    args = parser.parse_args()
    markdown_to_csv(args.markdown_folder, args.output_csv)
