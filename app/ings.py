import pandas as pd
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from elasticsearch.helpers import bulk

load_dotenv()

# --------------- change to tech zone connection ----------------

es_endpoint = os.environ["es_endpoint"]
es_cert_path = os.environ["es_cert_path"]
es_username = os.environ["es_username"]
es_password = os.environ["es_password"]

print("es_endpoint:", es_endpoint)
print("es_cert_path:", es_cert_path)
print("es_username:", es_username)
print("es_password:", es_password)

es = Elasticsearch(
    [es_endpoint],
    http_auth=(es_username, es_password),
    verify_certs=False
)
# ----------------------------------------------------------------

def create_index_name(index_name):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        mappings = {
                "properties": {
                    "fish_name": {
                        "type": "text"
                    },
                    "general_description": {
                        "type": "semantic_text"
                    },
                    "image_links": {
                        "type": "text"
                    },
                    # "embedding": {
                    #     "type": "dense_vector",
                    #     "dims": 768  # Adjust the dimension based on your model's output
                    # }
                }
            }

        mapping_response = es.indices.put_mapping(index=index_name, body=mappings)
        print(mapping_response)
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists.")
    return index_name
    


def ingest_df_to_elasticsearch(df, index_name):
    print("creating index name...")
    index_name = create_index_name(index_name)

    # Prepare bulk actions
    actions = [
        {
            "_index": index_name,
            "_source": {
                "fish_name": row["Fish Name"],
                "general_description": row["Summary Description"],
                "image_links": row["Image Links"]
            }
        }
        for _, row in df.iterrows()
    ]
    print("finish actions...")  # Debugging line to check actions

    # Upload to Elasticsearch

    print(actions)
    success, errors = bulk(es, actions)
    print(f"Success: {success}, Errors: {errors}")

