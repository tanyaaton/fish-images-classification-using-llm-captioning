from transformers import AutoTokenizer, AutoModel

model_id = "Snowflake/snowflake-arctic-embed-l-v2.0"
# Download and cache the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id)
