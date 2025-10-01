import os
import json

# Directory containing the JSON files
directory = "../data/software-tools"

# Loop over all JSON files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        file_path = os.path.join(directory, filename)
        
        # Load the existing JSON content
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Add or update the "ring" field
        data["ring"] = "Adopt"

        # Save the updated JSON back to the file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        print(f"Updated: {filename}")
