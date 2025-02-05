"""
Download Bulk Images from CSV

This script downloads images from a CSV file containing image URLs and names.

CSV File Structure:
    The CSV file must have the following columns:
    - `title`: A descriptive title for the image (used for naming the file).
    - `image_url`: The direct URL to the image.

Example CSV:
    title,image_url
    Example Image,https://example.com/image1.jpg
    Another Image,https://example.com/image2.png

Warning:
    - If the image URL does not specify a file extension, the script defaults to .jpg.

Usage:
    python download_images.py <csv_file_path> <output_folder>

Example:
    python download_images.py images.csv downloaded_images

Dependencies:
    - requests
    - csv

Install dependencies:
    pip install requests

Author: @jordyarms, gpt-4o
"""

import csv
import os
import requests
import argparse
from urllib.parse import urlparse

def download_images_from_csv(csv_file_path, output_folder):
    """
    Download images from a CSV file containing image URLs and save them with appropriate names.
    
    Args:
        csv_file_path (str): Path to the CSV file containing image URLs.
        output_folder (str): Directory to store the downloaded images.
    """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Read the CSV file
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row.get('title', 'unknown')
            image_url = row.get('image_url', '').strip()
            
            # Validate the image URL
            if not image_url:
                print(f"Skipping: {title} (no URL provided)")
                continue
            
            try:
                # Download the image
                response = requests.get(image_url, stream=True)
                response.raise_for_status()
                
                # Determine file extension
                parsed_url = urlparse(image_url)
                file_extension = os.path.splitext(parsed_url.path)[1]
                if not file_extension:
                    file_extension = ".jpg"  # Default to .jpg if no extension
                
                # Create a valid filename
                sanitized_title = "".join(c if c.isalnum() else "_" for c in title)
                file_name = f"{sanitized_title}{file_extension}"
                file_path = os.path.join(output_folder, file_name)
                
                # Save the image
                with open(file_path, 'wb') as image_file:
                    for chunk in response.iter_content(1024):
                        image_file.write(chunk)
                
                print(f"Downloaded: {title} -> {file_name}")
            
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {image_url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download images from a CSV file.')
    parser.add_argument('csv_file_path', type=str, help='Path to the input CSV file')
    parser.add_argument('output_folder', type=str, help='Path to the output directory')
    
    args = parser.parse_args()
    download_images_from_csv(args.csv_file_path, args.output_folder)
