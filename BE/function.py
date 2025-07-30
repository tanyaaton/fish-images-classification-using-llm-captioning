from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

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

print('Info:',es.info())


# -------------------------------- query -------------------------------------
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
                "physical_description": {
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
        hit = elastic_hits['hits']['hits'][i]['_source']
        fish_score = elastic_hits['hits']['hits'][i]['_score']
        top_n_fish.append({
            "fish_name": hit.get('fish_name'),
            "thai_fish_name": hit.get('thai_fish_name'),
            "scientific_name": hit.get('scientific_name'),
            "order_name": hit.get('order_name'),
            "general_description": hit.get('general_description'),
            "physical_description": hit.get('physical_description'),
            "habitat": hit.get('habitat'),
            "avg_length_cm": hit.get('avg_length_cm'),
            "avg_age_years": hit.get('avg_age_years'),
            "avg_depthlevel_m": hit.get('avg_depthlevel_m'),
            "avg_weight_kg": hit.get('avg_weight_kg'),
            "score": fish_score
        })
    return top_n_fish

def return_top_n_fish_simple(elastic_hits, n=5):
    """
    Returns top N fish from Elasticsearch hits with basic fields
    """
    top_n_fish = []
    for i in range(n):
        hit = elastic_hits['hits']['hits'][i]['_source']
        fish_score = elastic_hits['hits']['hits'][i]['_score']
        top_n_fish.append({
            "fish_name": hit.get('fish_name'),
            "thai_fish_name": hit.get('thai_fish_name'),
            "scientific_name": hit.get('scientific_name'),
            "order_name": hit.get('order_name'),
            "score": fish_score
        })
    return top_n_fish
