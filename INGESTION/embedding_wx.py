import requests
from dotenv import load_dotenv
import os

load_dotenv()
emb_url = os.getenv("EMBEDDING_SERVICE_URL")


def watsonx_embedder(sentence):
    payload = {
        "sentence": [sentence]
    }
    response = requests.post(emb_url, json=payload)
    response_json = response.json()
    return response_json["predictions"][0]["values"][0][1]