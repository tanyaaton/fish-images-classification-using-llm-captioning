from elasticsearch_manager import ElasticsearchManager
from embedding_service import EmbeddingService
import pandas as pd
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))


load_dotenv()
print("Loading environment variables...")

es_endpoint = os.environ["es_endpoint"]
es_cert_path = os.environ["es_cert_path"]
es_username = os.environ["es_username"]
es_password = os.environ["es_password"]

#--------ingestion to elasticsearch----------------
index_name = 'fish_index_v3'

# csv file must have at least 2 columns: fish_name, general_description
df = pd.read_csv("../EXTRACTION/DATA/fish-description-files/Marine_Fish_Species_Full_Description_test.csv")


# Generate description embeddings using online service
import requests
def get_online_embedding(text):
    url = "https://snowflake-embedding.1xlkl2nudnhu.us-south.codeengine.appdomain.cloud/extract_text"
    payload = {"sentence": text}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    embedding = [item[1] for item in data["predictions"][0]["values"]]
    return embedding

print('Embedding fish descriptions using online service...')
embeddings = [get_online_embedding(desc) for desc in df['Summary Description']]
df['embedding'] = embeddings
print('---------------------')
print(embeddings)
print("Embedding length:", len(embeddings))
print(len(embeddings[0]))
print(df.head())

print(df.head())


esm = ElasticsearchManager(es_endpoint, es_username, es_password)
# Delete index if it exists
if esm.es.indices.exists(index=index_name):
    print(f"Index '{index_name}' already exists. Deleting it...")
    esm.es.indices.delete(index=index_name)
esm.ingest_df_to_elasticsearch(df, index_name)






