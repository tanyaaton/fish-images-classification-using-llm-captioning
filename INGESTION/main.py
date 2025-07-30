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
index_name = 'fish_index_v4'

# csv file must have at least 2 columns: fish_name, general_description, physical_description
df = pd.read_csv("../EXTRACTION/DATA/fish-description-files/Marine_Fish_Species_Formatted_updated.csv")

# generate embeddings for both general and physical description
emb = EmbeddingService('watsonx') # Use the online embedding service
general_embeddings = emb.embed_text(df['General Description'])
physical_embeddings = emb.embed_text(df['Physical Description'])
df['general_description_embedding'] = list(general_embeddings)
df['physical_description_embedding'] = list(physical_embeddings)

print('---------------------')
print("General Description Embeddings:", general_embeddings)
print("Physical Description Embeddings:", physical_embeddings)
print("Embedding length (general):", len(general_embeddings))
print("Embedding length (physical):", len(physical_embeddings))
print("Single embedding length (general):", len(general_embeddings[0]))
print("Single embedding length (physical):", len(physical_embeddings[0]))
print(df.head())

esm = ElasticsearchManager(es_endpoint, es_username, es_password)
# check if index exists, if exists ask for deletion
if esm.es.indices.exists(index=index_name):
    print(f"Index '{index_name}' already exists. Deleting it...")
    if input(f"Do you want to delete the index '{index_name}'? (y/n): ").strip().lower() == 'y':
        esm.es.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted.")
esm.ingest_df_to_elasticsearch(df, index_name)
