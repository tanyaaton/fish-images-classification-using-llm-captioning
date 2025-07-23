import pandas as pd
import requests

# Load the CSV file
df = pd.read_csv("../EXTRACTION/DATA/fish-description-files/Marine_Fish_Species_Full_Description_test.csv")

# Embedding function
def get_online_embedding(text):
    url = "https://snowflake-embedding.1xlkl2nudnhu.us-south.codeengine.appdomain.cloud/extract_text"
    payload = {"sentence": [text]}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    print("RAW API RESPONSE:", data)  # Debug: print the raw response
    # Extract the dense embedding vector (should be a list of floats)
    embedding = data["predictions"][0]["values"][0][1]
    return embedding

print('Checking embedding lengths for each description...')
for idx, row in df.iterrows():
    desc = row['Summary Description']
    fish_name = row['Fish Name']
    emb = get_online_embedding(desc)
    print(f"Row {idx}: Fish Name: {fish_name}")
    print(f"Description: {desc}")
    print(f"Embedding length: {len(emb)}\n---\n")
print('Done checking all rows.')
