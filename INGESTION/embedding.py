import os
import string
import random
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300,
        length_function=len,
        is_separator_regex=False,
        )

def embedding_and_store_data(chunks_list, collection_name, filename, model_emb):
    vector_list  = model_emb.embed_documents(chunks_list)
    if not has_collection(collection_name):
        collection = create_milvus_db(collection_name)
    else:
        collection = Collection(name=collection_name)
    collection.insert([chunks_list,vector_list,[filename]* len(chunks_list) ])
    collection.create_index(field_name="embeddings",
                            index_params={"metric_type":"IP","index_type":"IVF_FLAT","params":{"nlist":16384}})
    return collection