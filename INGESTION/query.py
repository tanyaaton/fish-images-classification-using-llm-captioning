from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()


# --------------- change to tech zone connection ----------------
# elastic_url = os.getenv("ELASTIC_URL", None)
# elastic_api_key = os.getenv("ELASTIC_APIKEY", None)

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

print('Info:',es.info())

def semantic_text_search_fish_description(input_image_description, index_name):
    # Direct semantic query approach for Elasticsearch 8.12
    search_body = {
        "query": {
            "semantic": {
                "field": "general_description",
                "query": input_image_description
            }
        }
    }
    
    print('search_body:', search_body)

    search_response = es.search(
        index=index_name,
        body=search_body
    )
    print(search_response['hits']['hits'])
    return search_response


def text_search_fish_description_match(input_image_description, index_name):
    """
    Simple match query - good for general text searching
    """
    search_body = {
        "query": {
            "match": {
                "general_description": {
                    "query": input_image_description,
                    "fuzziness": "AUTO"  # Handles typos and variations
                }
            }
        }
    }
    
    print('search_body:', search_body)
    
    search_response = es.search(
        index=index_name,
        body=search_body
    )
    print(search_response['hits']['hits'])
    return search_response

def return_top_n_fish(elastic_hits,n=5):
    top_n_fish = []
    for i in range(n):
        fish_name = elastic_hits['hits']['hits'][i]['_source']['fish_name']
        fish_description = elastic_hits['hits']['hits'][i]['_source']['general_description']
        fish_score = elastic_hits['hits']['hits'][i]['_score']
        top_n_fish.append({
                    # "rank": fish_rank,
                    "fish_name": fish_name,
                    "description": fish_description,
                    "score": fish_score
                })
    return top_n_fish
