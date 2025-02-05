"""
CSV Metadata Scraper

This script extracts metadata from a list of URLs provided in a CSV file.
It scrapes standard metadata (title, description, keywords, published date),
Open Graph metadata, and JSON-LD schema data.

Usage:
    python csv_meta_scraper.py <input_csv> <output_csv>

Example:
    python csv_meta_scraper.py urls.csv metadata_output.csv

Example CSV:
    url
    https://example.com/page1.html
    https://example.com/page2.html

Dependencies:
    - requests
    - beautifulsoup4
    - pandas

Install dependencies:
    pip install requests beautifulsoup4 pandas

### Instructions for Novice Users ###
- Ensure your input CSV file has a column named `url` containing valid website links.
- The script will attempt to fetch metadata from each URL and store it in the output CSV.
- If a website blocks scraping, it may return an error or fail to fetch certain metadata.
- JSON-LD data is stored as a string; you may need additional processing to extract meaningful values.

### Warnings ###
- Some websites may block automated requests; if you receive too many failures, consider adding delays.
- Ensure the URLs in the CSV file are correctly formatted (e.g., include `http://` or `https://`).
- Metadata structures vary; the script may not extract all data consistently across different sites.

Author: @jordyarms, gpt-4o
"""

import requests
import pandas as pd
import argparse
from bs4 import BeautifulSoup
import json

def fetch_metadata(url):
    """
    Fetch metadata, Open Graph properties, and JSON-LD schema data from a given URL.
    
    Args:
        url (str): The webpage URL to scrape metadata from.
    
    Returns:
        dict: A dictionary containing metadata.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        metadata = {
            'url': url,
            'title': soup.title.string if soup.title else "",
            'description': "",
            'keywords': "",
            'published_date': "",
            'og_title': "",
            'og_description': "",
            'og_image': "",
            'og_url': "",
            'json_ld': ""
        }
        
        # Extract meta description
        desc_tag = soup.find("meta", attrs={"name": "description"})
        if desc_tag and 'content' in desc_tag.attrs:
            metadata['description'] = desc_tag['content']
        
        # Extract keywords
        keywords_tag = soup.find("meta", attrs={"name": "keywords"})
        if keywords_tag and 'content' in keywords_tag.attrs:
            metadata['keywords'] = keywords_tag['content']
        
        # Extract published date
        date_tag = soup.find("meta", property="article:published_time")
        if date_tag and 'content' in date_tag.attrs:
            metadata['published_date'] = date_tag['content']
        
        # Extract Open Graph data
        og_tags = ["og:title", "og:description", "og:image", "og:url"]
        for tag in og_tags:
            og_tag = soup.find("meta", property=tag)
            if og_tag and 'content' in og_tag.attrs:
                metadata[tag.replace("og:", "og_")] = og_tag['content']
        
        # Extract JSON-LD schema data
        json_ld_tag = soup.find("script", type="application/ld+json")
        if json_ld_tag:
            try:
                json_ld_data = json.loads(json_ld_tag.string)
                metadata['json_ld'] = json.dumps(json_ld_data)  # Store as string
            except json.JSONDecodeError:
                pass
        
        return metadata
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return {'url': url, 'error': str(e)}


def scrape_csv(input_csv, output_csv):
    """
    Read URLs from a CSV file, scrape metadata, and save results to another CSV file.
    
    Args:
        input_csv (str): Path to input CSV file containing URLs.
        output_csv (str): Path to output CSV file to save extracted metadata.
    """
    df = pd.read_csv(input_csv)
    if 'url' not in df.columns:
        print("Error: Input CSV must contain a 'url' column.")
        return
    
    results = []
    for url in df['url']:
        metadata = fetch_metadata(url)
        results.append(metadata)
    
    output_df = pd.DataFrame(results)
    output_df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Metadata saved to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape metadata from a list of URLs in a CSV file.')
    parser.add_argument('input_csv', type=str, help='Path to input CSV file containing URLs')
    parser.add_argument('output_csv', type=str, help='Path to output CSV file for extracted metadata')
    
    args = parser.parse_args()
    scrape_csv(args.input_csv, args.output_csv)
