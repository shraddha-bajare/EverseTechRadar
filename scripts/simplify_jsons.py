import os
import json
from collections import OrderedDict

directory = "../data/software-tools"

desired_order = [
    "type",
    "name",
    "description",
    "url",
    "applicationCategory",
    "hasQualityDimension",
    "Segment",
    "ring"
]

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Create a new OrderedDict with keys in desired order (if present)
        ordered_data = OrderedDict()
        for key in desired_order:
            if key in data:
                ordered_data[key] = data[key]

        # Add any other keys that were not in desired_order at the end (optional)
        for key in data:
            if key not in ordered_data:
                ordered_data[key] = data[key]

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(ordered_data, f, indent=2)

        print(f"✅ Reordered keys in: {filename}")
