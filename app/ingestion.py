import pandas as pd
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from elasticsearch.helpers import bulk

load_dotenv()

# --------------- change to tech zone connection ----------------
elastic_url = os.getenv("ELASTIC_URL", None)
elastic_api_key = os.getenv("ELASTIC_APIKEY", None)

es = Elasticsearch(
    elastic_url,
    api_key=elastic_api_key
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

    # Upload to Elasticsearch
    success, errors = bulk(es, actions)
    print(f"Success: {success}, Errors: {errors}")

