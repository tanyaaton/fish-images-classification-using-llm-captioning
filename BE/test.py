from function import semantic_text_search_fish_description, return_top_n_fish, text_search_fish_description_match
from BE.elasticsearch_query import ElasticsearchQuery
from watsonx_captioning import convert_image_to_base64, get_fish_description_from_watsonxai
from embedding_service import EmbeddingService
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
print("Loading environment variables...")

es_endpoint = os.environ["es_endpoint"]
es_cert_path = os.environ["es_cert_path"]
es_username = os.environ["es_username"]
es_password = os.environ["es_password"]


index_name = 'testesttt'
esq = ElasticsearchQuery(es_endpoint, es_username, es_password)
print('-------------')
esq.list_all_index(creator="user")

print('-------------')

image_path = "EXTRACTION/DATA/fish-random/fish-2.jpg"
pic_string = convert_image_to_base64(image_path)
caption = get_fish_description_from_watsonxai(pic_string)
print("Caption:", caption)

# embedding caption
emb = EmbeddingService('watsonx') # watsonx or sentence_transformer
caption_embedding = emb.embed_text(caption)




# ------- search using text match ------- 
# hits = text_search_fish_description_match(caption, index_name)
# top_n_fish = return_top_n_fish(hits,n=1)
# print("Top N Fish:", top_n_fish)

# ------- search using embedding ------- 
hits = esq.search_embedding(index_name=index_name, embedding_field='embedding',query_vector=caption_embedding, size=1)
print("🔥 Hits:", hits)
print("🔥 Hits Type:", type(hits))
top_n_fish = return_top_n_fish(hits,n=1)
print("Top N Fish:", top_n_fish)