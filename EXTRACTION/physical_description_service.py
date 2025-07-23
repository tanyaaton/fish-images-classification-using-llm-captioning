# watsonx_physical_description_service.py
"""
This script provides a service to generate physical descriptions of fish using IBM watsonx AI.
"""

import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()

WATSONX_API_KEY = os.getenv("WATSONX_APIKEY")
WATSONX_PROJECT_ID = os.getenv("PROJECT_ID")
WATSONX_URL = os.getenv("WATSONXAI_URL")

if not WATSONX_API_KEY or not WATSONX_PROJECT_ID or not WATSONX_URL:
    raise ValueError("WATSONX_APIKEY, PROJECT_ID, and WATSONXAI_URL must be set in .env")


credentials = Credentials(
    api_key=WATSONX_API_KEY,
    url=WATSONX_URL
)
model_id = "meta-llama/llama-3-70b-instruct"
model = ModelInference(
    model_id=model_id,
    params=None,  # We'll pass parameters per request
    credentials=credentials,
    project_id=WATSONX_PROJECT_ID
)


def get_physical_description(fish_name, max_tokens=128):
    """
    Calls watsonx AI to generate a physical description for the given fish name using the SDK.
    """
    prompt = (
        f"Describe the physical appearance of the fish species: {fish_name}. "
        "Focus on: typical body shape and size, possible coloration patterns and markings, "
        "distinctive features (such as fins, scales, head shape), and any unique identifying characteristics."
    )
    chat_messages = [
        {"role": "user", "content": prompt}
    ]
    parameters = {
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    response = model.chat(messages=chat_messages, params=parameters)
    # The SDK returns a dict with 'results' key containing a list of responses
    return response['results'][0]['generated_text'] if response.get('results') else ""

if __name__ == "__main__":
    # Example usage
    fish = "Scrawled filefish"
    print(get_physical_description(fish))
