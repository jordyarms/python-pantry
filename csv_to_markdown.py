"""
Convert CSV to Markdown Frontmatter

This script takes a CSV file and converts each row into a Markdown file with YAML front matter.

Usage:
    python csv_to_markdown.py <csv_path> <output_folder>

Example:
    python csv_to_markdown.py data.csv markdown_files

Dependencies:
    - pandas
    - pyyaml

Install dependencies:
    pip install pandas pyyaml

### Instructions for Novice Users ###
- Ensure your CSV file has column headers.
- The first column is used as the filename.
- Markdown files are named based on the first column, with spaces replaced by underscores and all letters converted to lowercase.
- Special characters in filenames will be replaced with underscores for compatibility.

### Warnings ###
- Avoid using special characters (e.g., `*`, `?`, `:`, `/`, `\\`) in the first column, as these will be replaced.
- If filenames are duplicated, later files may overwrite earlier ones.
- Ensure the output directory exists and is writable.

Author: @jordyarms, gpt-4o
"""

import pandas as pd
import os
import yaml
import argparse
import re

# Function to sanitize filenames
def sanitize_filename(name):
    """Replace special characters and spaces to ensure valid filenames."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name).lower()

# Function to convert 'checked' to True
def convert_to_boolean(value):
    return True if value == 'checked' else False if pd.notnull(value) else None

def csv_to_markdown(csv_path, output_folder):
    """
    Convert a CSV file into Markdown files with YAML front matter.
    
    Args:
        csv_path (str): Path to the CSV file.
        output_folder (str): Directory to store the generated Markdown files.
    """
    # Load the CSV data
    csv_data = pd.read_csv(csv_path)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate through each row in the DataFrame and create a Markdown file
    for _, row in csv_data.iterrows():
        # Use the first column as the filename
        filename_base = sanitize_filename(str(row.iloc[0]))
        filename = f"{filename_base}.md"
        filepath = os.path.join(output_folder, filename)
        
        # Build YAML data dictionary dynamically
        yaml_data = {}
        for col in csv_data.columns:
            value = row[col]
            if pd.notna(value):
                yaml_data[col.lower().replace(' ', '_')] = convert_to_boolean(value) if isinstance(value, str) and value.lower() == 'checked' else value
        
        # Write the Markdown file with YAML front matter
        with open(filepath, 'w', encoding='utf-8') as md_file:
            md_file.write('---\n')
            yaml.dump(yaml_data, md_file, default_flow_style=False)
            md_file.write('---\n\n')
        
    print(f"Markdown files with YAML front matter have been created in '{output_folder}'!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert CSV to Markdown with YAML front matter.')
    parser.add_argument('csv_path', type=str, help='Path to the input CSV file')
    parser.add_argument('output_folder', type=str, help='Path to the output directory')
    
    args = parser.parse_args()
    csv_to_markdown(args.csv_path, args.output_folder)
