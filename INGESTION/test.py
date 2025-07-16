from BE.captioning import convert_image_to_base64, get_fish_description_from_watsonxai
from BE.function import semantic_text_search_fish_description, return_top_n_fish, text_search_fish_description_match
from ingestion import ingest_df_to_elasticsearch
import pandas as pd

#--------ingestion to elasticsearch----------------
index_name = 'thai_fish_descriptions'
# df = pd.read_csv("EXTRACTION/DATA/fish-description-files/Marine_Fish_Species_Full_Description_test.csv")
# ingest_df_to_elasticsearch(df, index_name)




