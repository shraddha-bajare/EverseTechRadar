import json
import os
from pathlib import Path
from datetime import datetime

def get_items(field):
    """
    Extract items from a field that can be:
    field e.g applicationCategory, hasQualityDimension 
    - a dict with '@id' e.g { "@id": "dim:Maintainability", "@type": "@id" }
    - a list of dicts with '@id' e.g. [
        { "@id": "dim:Maintainability", "@type": "@id" },
        { "@id": "dim:Sustainability", "@type": "@id" },
        { "@id": "dim:Reliability", "@type": "@id" }
      ]
    - a list of strings e.g [ "Maintainability", "Sustainability"]
    - a single string  e.g "Maintainability"
    Returns a list of strings.
    """
    items = []
    if isinstance(field, dict):
        if '@id' in field:
            raw_id = field['@id'].split('/')[-1]
            items.append(raw_id.split(':')[-1])
        else:
            pass
    elif isinstance(field, list):
        for item in field:
            if isinstance(item, dict) and '@id' in item:
                raw_id = item['@id'].split('/')[-1]
                items.append(raw_id.split(':')[-1])
            elif isinstance(item, str):
                items.append(item)
    elif isinstance(field, str):
        items.append(field)
    return items


def generate_markdown(json_ld_file, output_dir, quality_dimension=None):
    """Generates tools markdown for techradar dashboard from a JSON-LD file."""
    with open(json_ld_file, 'r') as file:
        json_ld = json.load(file)

    # Fetch title, description, URL
    title = json_ld.get('name', 'Unknown Title')
    url = json_ld.get('url', '')
    description = json_ld.get('description', "No description available")

    # Application Category (for tag)
    application_category_field = json_ld.get('applicationCategory', [])
    application_categories = get_items(application_category_field)
    application_category = application_categories[0] if application_categories else "Unknown"

    # Ring
    ring = json_ld.get('ring', 'Unknown')

    # Segment
    segment_field = json_ld.get('segment', [])
    segments = get_items(segment_field)
    segment = segments[0] if segments else "Unknown"


    # Tags
    tags = []
    tags.extend(application_categories)

    # Prepare markdown content
    markdown_content = f"""---
title: "{title}"
ring: {ring}
quadrant: {segment}
tags: {tags}
---
{description}
"""

    # Output directory
    os.makedirs(output_dir, exist_ok=True)

    # Filename
    markdown_file_name = f"{title.replace(' ', '_').lower()}.md"
    markdown_path = os.path.join(output_dir, markdown_file_name)

    # Write the file
    with open(markdown_path, 'w') as md_file:
        md_file.write(markdown_content)

    print(f"✅ Generated markdown: {markdown_path}")


def process_json_ld_files(input_dir, output_dir):
    """Process all JSON-LD files in the input directory."""
    for json_file in os.listdir(input_dir):
        if json_file.endswith('.json'):
            json_ld_path = os.path.join(input_dir, json_file)
            generate_markdown(json_ld_path, output_dir)


outdir = Path(f'../radar/{datetime.today().strftime("%Y-%m-%d")}')
outdir.mkdir(parents=True, exist_ok=True)

input_dir = '../data/software-tools'  # Directory where JSON-LD files are stored
output_dir = outdir # Directory where markdown files are stored

process_json_ld_files(input_dir, output_dir)
