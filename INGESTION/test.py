from elasticsearch_manager import ElasticsearchManager
from embedding_hg import embed_text
import pandas as pd
import os
import sys

es_endpoint = os.environ["es_endpoint"]
es_cert_path = os.environ["es_cert_path"]
es_username = os.environ["es_username"]
es_password = os.environ["es_password"]

#--------ingestion to elasticsearch----------------
index_name = 'thai_fish_descriptions'

# csv file must have at least 2 columns: fish_name, general_description
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
df = pd.read_csv("EXTRACTION/DATA/fish-description-files/Marine_Fish_Species_Full_Description_test.csv")

# generate description embeddings
embeddings = embed_text(df['Summary Description'])
df['embedding'] = list(embeddings)

esm = ElasticsearchManager(es_endpoint, es_username, es_password)
esm.ingest_df_to_elasticsearch(df, index_name)




