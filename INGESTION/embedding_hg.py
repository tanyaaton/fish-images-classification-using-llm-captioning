import base64
from sentence_transformers import SentenceTransformer
import pandas as pd

model_name = 'Snowflake/snowflake-arctic-embed-l-v2.0'
model = SentenceTransformer(model_name)

def embed_text(sentences):
        embeddings = model.encode(sentences)
        # return {
        #     'predictions': [
        #         {
        #             'fields': ['sentence', 'embedding'],
        #             'values': [[sentence, embedding.tolist()] for sentence, embedding in zip(sentences, embeddings)]
        #         }
        #     ]
        # }
        return embeddings
