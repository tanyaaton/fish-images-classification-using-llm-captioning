# This script will be used to create a formatted CSV for embedding purposes.

import pandas as pd

# Placeholder for CSV creation logic

def create_embedding_csv(output_path):
    # Read fish names from the provided CSV
    import csv
    input_csv = "./DATA/fish-description-files/Marine_Fish_Species_Full_Description_test.csv"
    fish_names = []
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fish_names.append(row["Fish Name"])

    # Prepare new rows
    rows = []
    for fish in fish_names:
        # Format for COS object names
        fish_folder = fish.replace(" ", "-")
        fish_file = fish.lower().replace(" ", "-")
        object_names = [
            f"fish_images/{fish_folder}/{fish_file}-{i:03d}.png" for i in range(1, 4)
        ]
        rows.append({
            "Fish Name": fish,
            "Physical Description": "",  # Placeholder, to be filled later
            "Object Names": ", ".join(object_names)
        })

    # Write to new CSV
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    # Example usage (to be updated with actual logic)
    create_embedding_csv("embedding_format.csv")


