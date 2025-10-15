import csv
import json

# Load JSON data
with open('fish_descriptions_checkpoint.json', 'r', encoding='utf-8') as f_json:
    fish_desc = json.load(f_json)

# Read CSV and update Physical Description
input_csv = 'DATA/fish-description-files/Marine_Fish_Species_Formatted.csv'
output_csv = 'DATA/fish-description-files/Marine_Fish_Species_Formatted_updated.csv'

with open(input_csv, 'r', encoding='utf-8') as f_in, open(output_csv, 'w', encoding='utf-8', newline='') as f_out:
    reader = csv.DictReader(f_in)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        fish_name = row['Fish Name']
        if fish_name in fish_desc:
            row['Physical Description'] = fish_desc[fish_name]
        writer.writerow(row)

print("Physical Description column updated. Output saved to:", output_csv)
