import os
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv

# --- Initialization (can be done once) ---
load_dotenv()

credentials = Credentials(
    url=os.getenv("WATSONXAI_URL"),
    api_key=os.getenv("WATSONXAI_APIKEY"),
)

model_id = "meta-llama/llama-3-3-70b-instruct"

parameters = {
    "frequency_penalty": 0,
    "max_tokens": 2000,
    "presence_penalty": 0,
    "temperature": 0,
    "top_p": 1
}

project_id = os.getenv("PROJECT_ID")
space_id = os.getenv("SPACE_ID")

model = ModelInference(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=project_id,
    space_id=space_id
)
# --- End Initialization ---

def get_generated_response(question: str, reference: str):
    """
    Generates a response using watsonx.ai based on a question and reference context.
    """
    # This system prompt is taken from your example to ensure consistency
    system_prompt = (
        "You are a helpful customer service assistant. Answer the user’s question based only on the provided product information. "
        "Recommend general dress styles that might suit the user’s need, without mentioning specific product names. "
        "Keep your tone warm and human-like, and avoid bullet points or numbered lists. "
        "Suggest the user explore the search results for specific items. "
        "If there isn’t enough information to answer, say ‘I don’t know.’"
    )

    user_prompt = (
        f"Based on this product information: {reference}\n\n"
        f"And this question: {question}\n\n"
        f"Please give a short, natural-sounding response following the instructions."
    )

    chat_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response = model.chat(messages=chat_messages)
    
    # Extract the generated text from the watsonx.ai response format
    if response and "results" in response and len(response["results"]) > 0:
        return response["results"][0].get("generated_text", "Error: Could not extract generated text.")
    else:
        return "Error: Invalid response from model."