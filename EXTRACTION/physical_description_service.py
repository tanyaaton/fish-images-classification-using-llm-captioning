from dotenv import load_dotenv
import base64
import os
import http.client
import json
import requests
import pandas as pd

load_dotenv()

watsonx_api_key = os.getenv("WATSONX_APIKEY", None)
ibm_cloud_url = os.getenv("IBM_CLOUD_URL", None)
project_id = os.getenv("PROJECT_ID", None)
ibm_cloud_iam_url = os.getenv("IAM_IBM_CLOUD_URL", None)
chat_url = os.getenv("IBM_WATSONX_AI_INFERENCE_URL", None)

def get_fish_description_from_watsonxai(fish_name):
    conn_ibm_cloud_iam = http.client.HTTPSConnection(ibm_cloud_iam_url)
    payload = "grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey=" + watsonx_api_key
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    conn_ibm_cloud_iam.request("POST", "/identity/token", payload, headers)
    res = conn_ibm_cloud_iam.getresponse()
    data = res.read()
    decoded_json = json.loads(data.decode("utf-8"))
    access_token = decoded_json["access_token"]

    system_content = """You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. Do not use markdown formatting in your response."""
    user_message = f"""Please provide a detailed description of the fish species named '{fish_name}' focusing on the following aspects:\n    1. Body shape and size\n    2. Coloration patterns and markings\n    3. Distinctive features (fins, scales, head shape, etc.)\n    4. Any unique identifying characteristics\n\nReturn your answer as a single string in the following format (do not use JSON, do not add extra text):\nbody: ...; colors: ...; features: ...; unique_marks: ...\n"""

    body = {
        "messages": [
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": user_message
            }
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

# Simple test/demo
if __name__ == "__main__":
    fish_name = "Yellow Boxfish"
    print(get_fish_description_from_watsonxai(fish_name))
