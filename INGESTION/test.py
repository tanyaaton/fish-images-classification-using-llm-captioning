from captioning import convert_image_to_base64, get_fish_description_from_watsonxai
from query import semantic_text_search_fish_description, return_top_n_fish
from ings import ingest_df_to_elasticsearch
import pandas as pd

#--------ingestion to elasticsearch----------------
index_name = 'thai_fish_descriptions'
# df = pd.read_csv("EXTRACTION/DATA/fish-description-files/Marine_Fish_Species_Full_Description_test.csv")
# ingest_df_to_elasticsearch(df, index_name)

# # #--------captioning and querying-------------------
image_path = "app/fish-random/fish-2.jpg"
pic_string = convert_image_to_base64(image_path)
caption = get_fish_description_from_watsonxai(pic_string)

print("Caption:", caption)

hits = semantic_text_search_fish_description(caption, index_name)
top_n_fish = return_top_n_fish(hits,n=1)
print("Top N Fish:", top_n_fish)

