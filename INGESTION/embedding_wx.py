import os
import string
import random
from dotenv import load_dotenv
from ibm_watsonx_ai.client import APIClient
from ibm_watsonx_ai.foundation_models import Embeddings


embedding_dimension = 384 #adjust the value according to your choice of embedding

load_dotenv()
api_key = os.getenv("WATSONX_APIKEY", None)
ibm_cloud_url = os.getenv("IBM_CLOUD_URL", None)
project_id = os.getenv("PROJECT_ID", None)

print("WATSONX_APIKEY:", api_key)
print("IBM_CLOUD_URL:", ibm_cloud_url)
print("PROJECT_ID:", project_id)


if api_key is None or ibm_cloud_url is None or project_id is None:
    print("Ensure you copied the .env file that you created earlier into the same directory as this notebook")
else:
    creds = {
        "url": ibm_cloud_url,
        "apikey": api_key 
    }


#----------embedding data + store in milvus
def connect_watsonx_embedding(model_id_emb):
    emb = Embeddings(
        model_id=model_id_emb,
        credentials=creds,
        project_id=project_id,
        params={
            "truncate_input_tokens": 512
        }
    )
    wml_credentials = creds
    client = APIClient(credentials=wml_credentials, project_id=project_id)
    return client, emb

def embed_text(text_to_embed, emb_model):
    embedded_vector  = emb_model.embed_documents([text_to_embed])
    return embedded_vector

client, emb = connect_watsonx_embedding('multilingual-e5-large')
print("Connected to WatsonX embedding service.")
print(embed_text("This is a test sentence.", emb))