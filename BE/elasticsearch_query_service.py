import pandas as pd
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from elasticsearch.helpers import bulk
import os

class ElasticsearchQuery:
    def __init__(self, es_endpoint, es_username, es_password):
        self.es = Elasticsearch(
        [es_endpoint],
        http_auth=(es_username, es_password),
        verify_certs=False
    )
    def list_all_index(self, creator="user"):
        """
        Args:
            creator (str):
                - "user": indices not starting with '.'
                - "system": indices starting with '.'
                - "all": all indices categorized
        """
        try:
            # Fixed: Use keyword argument
            user_index = []
            system_index = []
            indices = self.es.indices.get_alias()
            for index_name in indices.keys():
                count = self.get_document_count(index_name, silent=True)
                if not(index_name.startswith('.')):
                    # print(f"  - {index_name} ({count} documents)")
                    user_index.append(index_name)
                else:
                    system_index.append(index_name)
            print(f"User Indices: {user_index}")
            if creator == "user":
                return user_index
            elif creator == "system":
                return system_index
            elif creator == "all":
                return indices.keys()
        except Exception as e:
            print(f"✗ Error listing indices: {e}")
    
    def get_document_count_from_index(self, index_name, silent=False):
        try:
            response = self.es.count(index=index_name)
            count = response['count']
            if not silent:
                print(f"📊 Index '{index_name}' contains {count} documents")
            return count
        except Exception as e:
            if not silent:
                print(f"✗ Error getting document count: {e}")
            return 0
  
    def search_text(self, index_name, field, text, size=10):
        """Search text in specific field"""
        try:
            response = self.es.search(
                index=index_name,
                body={
                    "query": {"match": {field: text}},
                    "size": size
                }
            )
            docs = [hit['_source'] for hit in response['hits']['hits']]
            print(f"📄 Found {len(docs)} matches for '{text}' in {field}")
            return docs
        except Exception as e:
            print(f"✗ Search error: {e}")
    
    def search_exact(self, index_name, field, value, size=10):
        """Search exact match"""
        try:
            response = self.es.search(
                index=index_name,
                body={
                    "query": {"term": {field: value}},
                    "size": size
                }
            )
            docs = [hit['_source'] for hit in response['hits']['hits']]
            print(f"📄 Found {len(docs)} exact matches")
            return docs
        except Exception as e:
            print(f"✗ Search error: {e}")
    
    # def search_range(self, index_name, field, min_val=None, max_val=None, size=10):
    #     """Search numeric/date range"""
    #     try:
    #         range_query = {}
    #         if min_val is not None:
    #             range_query["gte"] = min_val
    #         if max_val is not None:
    #             range_query["lte"] = max_val
            
    #         response = self.es.search(
    #             index=index_name,
    #             body={
    #                 "query": {"range": {field: range_query}},
    #                 "size": size
    #             }
    #         )
    #         docs = [hit['_source'] for hit in response['hits']['hits']]
    #         print(f"📄 Found {len(docs)} in range")
    #         return docs
    #     except Exception as e:
    #         print(f"✗ Range error: {e}")
    
    def search_embedding(self, index_name, embedding_field, query_vector, size=10):
        """Search similar vectors using kNN"""
        try:
            response = self.es.search(
                index=index_name,
                body={
                    "knn": {
                        "field": embedding_field,
                        "query_vector": query_vector,
                        "k": size,
                        "num_candidates": size * 2
                    },
                    "_source": True
                }
            )
            return response
            
            # results = []
            # for hit in response['hits']['hits']:
            #     results.append({
            #         'score': hit['_score'],
            #         'data': hit['_source']
            #     })
            
            # print(f"🎯 Found {len(results)} similar embeddings")
            # for i, result in enumerate(results):
            #     print(f"  #{i+1}: Score {result['score']:.4f}")
            
            # return results
        except Exception as e:
            print(f"✗ Embedding search error: {e}")
    
    def count_docs(self, index_name, query=None):
        """Count documents matching query"""
        try:
            body = {"query": query} if query else {"query": {"match_all": {}}}
            response = self.es.count(index=index_name, body=body)
            count = response['count']
            print(f"📊 Count: {count}")
            return count
        except Exception as e:
            print(f"✗ Count error: {e}")
        
    def get_index_info(self, index_name):
        try:
            if not self.es.indices.exists(index=index_name):
                print(f"❌ Index '{index_name}' not found")
                return None
            
            # Get mapping and count
            mapping = self.es.indices.get_mapping(index=index_name)[index_name]['mappings']
            count = self.es.count(index=index_name)['count']
            
            # Get sample document
            sample = self.es.search(index=index_name, body={"size": 1})
            sample_doc = sample['hits']['hits'][0]['_source'] if sample['hits']['hits'] else {}
            
            print(f"📊 {index_name}: {count} rows")
            print("Columns:")
            for field, value in sample_doc.items():
                field_type = type(value).__name__
                print(f"  {field}: {field_type}")
            
            return {'rows': count, 'columns': list(sample_doc.keys()), 'sample': sample_doc}
            
        except Exception as e:
            print(f"✗ Info error: {e}")
