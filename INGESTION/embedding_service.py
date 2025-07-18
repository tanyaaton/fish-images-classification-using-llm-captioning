import os
import requests
from typing import List, Union
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv


class EmbeddingService:
    def __init__(self, embedding_type: str = "watsonx", model_name: str = None):
        self.embedding_type = embedding_type.lower()
        print(f"Using embedding type: {self.embedding_type}")
        if self.embedding_type == "sentence_transformer":
            self.model = SentenceTransformer(model_name or 'Snowflake/snowflake-arctic-embed-l-v2.0')
        elif self.embedding_type == "watsonx":
            load_dotenv()
            self.emb_url = os.getenv("EMBEDDING_SERVICE_URL")
            if not self.emb_url:
                raise ValueError("EMBEDDING_SERVICE_URL environment variable required")
        else:
            raise ValueError("embedding_type must be 'sentence_transformer' or 'watsonx'")
    
    def embed_text(self, sentences: Union[str, List[str]]):
        single_input = isinstance(sentences, str)
        print(f"Embedding input: {sentences}")
        if single_input:
            sentences = [sentences]
        
        if self.embedding_type == "sentence_transformer":
            embeddings = self.model.encode(sentences)
        else:  # watsonx
            print("Using WatsonX for embedding...")
            embeddings = []
            for sentence in sentences:
                response = requests.post(self.emb_url, json={"sentence": [sentence]})
                embeddings.append(response.json()["predictions"][0]["values"][0][1])
        
        return embeddings[0] if single_input else embeddings