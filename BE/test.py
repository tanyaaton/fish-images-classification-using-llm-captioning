from function import semantic_text_search_fish_description, return_top_n_fish, text_search_fish_description_match
from captioning import convert_image_to_base64, get_fish_description_from_watsonxai
import pandas as pd

index_name = 'thai_fish_descriptions'

image_path = "EXTRACTION/DATA/fish-random/fish-2.jpg"
pic_string = convert_image_to_base64(image_path)
caption = get_fish_description_from_watsonxai(pic_string)

print("Caption:", caption)
# hits = semantic_text_search_fish_description(caption, index_name)
hits = text_search_fish_description_match(caption, index_name)
top_n_fish = return_top_n_fish(hits,n=1)
print("Top N Fish:", top_n_fish)