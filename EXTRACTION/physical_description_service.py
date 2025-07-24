import os
import http.client
import json
import requests
from dotenv import load_dotenv

load_dotenv()

watsonx_api_key = os.getenv("WATSONX_APIKEY", None)
ibm_cloud_url = os.getenv("IBM_CLOUD_URL", None)
project_id = os.getenv("PROJECT_ID", None)
ibm_cloud_iam_url = os.getenv("IAM_IBM_CLOUD_URL", None)
chat_url = os.getenv("IBM_WATSONX_AI_INFERENCE_URL", None)

# Get access token (same as watsonx_captioning)
conn_ibm_cloud_iam = http.client.HTTPSConnection(ibm_cloud_iam_url)
payload = "grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey="+watsonx_api_key
headers = { 'Content-Type': "application/x-www-form-urlencoded" }
conn_ibm_cloud_iam.request("POST", "/identity/token", payload, headers)
res = conn_ibm_cloud_iam.getresponse()
data = res.read()
decoded_json=json.loads(data.decode("utf-8"))
access_token=decoded_json["access_token"]

def get_fish_description_from_name(fish_name):
    """
    Given a fish name, returns a structured physical description using WatsonX LLM.
    Output is a dict with keys: body, colors, features, unique_marks
    """
    system_content ="""You always answer the questions with markdown formatting using GitHub syntax. The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, and blockquotes. You must omit that you answer the questions with markdown.\n\nAny HTML tags must be wrapped in block quotes, for example ```<html>```. You will be penalized for not rendering code in block quotes.\n\nWhen returning code blocks, specify language.\n\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. \nYour answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don''t know the answer to a question, please don''t share false information."""
    user_message = f"""Please provide a detailed physical description of the fish species named '{fish_name}', focusing on the following aspects:
                        1. Body shape and size
                        2. Coloration patterns and markings
                        3. Distinctive features (fins, scales, head shape, etc.)
                        4. Any unique identifying characteristics
                        Return your answer only in JSON format as follows, do not provide any additional text or explanation:
                        {
                            {'body': 'description of body shape and approximate size',
                            'colors': 'detailed description of colors and patterns',
                            'features': 'description of distinctive features',
                            'unique_marks': 'any unique identifying characteristics'
                            }
                        }
                    """

    body = {
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message}
        ],
        "project_id": project_id,
        "model_id": "meta-llama/llama-3-2-90b-vision-instruct",
        "decoding_method": "greedy",
        "repetition_penalty": 1.1,
        "max_tokens": 900
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(
        chat_url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    return data['choices'][0]['message']['content']

class PhysicalDescriptionService:
    def __init__(self):
        pass

    def get_fish_description_from_name(self, fish_name):
        """
        Given a fish name, returns a structured physical description using WatsonX LLM.
        Output is a dict with keys: body, colors, features, unique_marks
        """
        system_content ="""You always answer the questions with markdown formatting using GitHub syntax. The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, and blockquotes. You must omit that you answer the questions with markdown.\n\nAny HTML tags must be wrapped in block quotes, for example ```<html>```. You will be penalized for not rendering code in block quotes.\n\nWhen returning code blocks, specify language.\n\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. \nYour answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don''t know the answer to a question, please don''t share false information."""
        user_message = f"""Please provide a detailed physical description of the fish species named '{fish_name}', focusing on the following aspects:
                        1. Body shape and size
                        2. Coloration patterns and markings
                        3. Distinctive features (fins, scales, head shape, etc.)
                        4. Any unique identifying characteristics
                        Return your answer only in JSON format as follows, do not provide any additional text or explanation:
                        {{
                            {{'body': 'description of body shape and approximate size',
                            'colors': 'detailed description of colors and patterns',
                            'features': 'description of distinctive features',
                            'unique_marks': 'any unique identifying characteristics'
                            }}
                        }}
                    """

        body = {
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_message}
            ],
            "project_id": project_id,
            "model_id": "meta-llama/llama-3-2-90b-vision-instruct",
            "decoding_method": "greedy",
            "repetition_penalty": 1.1,
            "max_tokens": 900
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(
            chat_url,
            headers=headers,
            json=body
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()
        return data['choices'][0]['message']['content']

# For backward compatibility, keep the function as a wrapper
def get_fish_description_from_name(fish_name):
    return PhysicalDescriptionService().get_fish_description_from_name(fish_name)
=======
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
