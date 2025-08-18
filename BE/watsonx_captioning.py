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


### input and descripe input image

def convert_image_to_base64(image_path):
    pic = open(image_path,"rb").read()
    pic_base64 = base64.b64encode(pic)
    pic_string = pic_base64.decode("utf-8")
    return pic_string


def get_fish_description_from_watsonxai(pic_string):
    conn_ibm_cloud_iam = http.client.HTTPSConnection(ibm_cloud_iam_url)
    payload = "grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey="+watsonx_api_key
    headers = { 'Content-Type': "application/x-www-form-urlencoded" }
    conn_ibm_cloud_iam.request("POST", "/identity/token", payload, headers)
    res = conn_ibm_cloud_iam.getresponse()
    data = res.read()
    decoded_json=json.loads(data.decode("utf-8"))
    access_token=decoded_json["access_token"]

    system_content = """
    You always answer the questions with markdown formatting using GitHub syntax. 
    The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, and blockquotes. 
    You must omit that you answer the questions with markdown.

    Any HTML tags must be wrapped in block quotes, for example:
    ```<html>```. 
    You will be penalized for not rendering code in block quotes.

    When returning code blocks, specify the language.

    You are a helpful, respectful, and honest assistant. Always answer as helpfully as possible, while being safe. 
    Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
    Please ensure that your responses are socially unbiased and positive in nature.

    If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. 
    If you don't know the answer to a question, please don't share false information.
    """
    user_message = """Please provide a detailed description of what the image depicts and what you think it"""

    body = {
    "messages": [
        {
            "role": "system",
            "content": system_content
        },
        {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": user_message,
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64, {pic_string}"
                }
                }
            ]
        }
    ],
    "project_id": project_id,
    # "model_id": "meta-llama/llama3-llava-next-8b-hf",
    # "model_id": "meta-llama/llama-3-2-11b-vision-instruct",
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

def get_json_generated_image_details(pic_string):
    conn_ibm_cloud_iam = http.client.HTTPSConnection(ibm_cloud_iam_url)
    payload = "grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey="+watsonx_api_key
    headers = { 'Content-Type': "application/x-www-form-urlencoded" }
    conn_ibm_cloud_iam.request("POST", "/identity/token", payload, headers)
    res = conn_ibm_cloud_iam.getresponse()
    data = res.read()
    decoded_json=json.loads(data.decode("utf-8"))
    access_token=decoded_json["access_token"]

    system_content = """
    You are an AI assistant designed to analyze images and generate structured JSON responses. 
    Your task is to identify whether the image contains a fish and, if so, provide detailed information about it.

    The JSON response must include:
    - `image_contains_fish`: (true/false) - Indicates whether the image contains a fish.
    - `fish_details`: An object containing:
    - `fish_name`: The name of the fish.
    - `scientific_name`: The scientific name of the fish.
    - `order_name`: The order name of the fish.
    - `physical_description`: A detailed physical description of the fish.
    - `habitat`: The habitat where the fish is typically found.

    If the image does not contain a fish, set `image_contains_fish` to `false` and `fish_details` to an empty object.
    Ensure the response is accurate, concise, and formatted as valid JSON and only JSON and nothing else.
    """
    
    user_message = """
    Generate a JSON object describing the fish in the image. The JSON should include:
    - `image_contains_fish`: (true/false) - Indicates whether the image contains a fish.
    - `fish_details`: An object containing:
    - `fish_name`: The name of the fish.
    - `scientific_name`: The scientific name of the fish.
    - `order_name`: The order name of the fish.
    - `physical_description`: A detailed physical description of the fish.

    If the image does not contain a fish, set `image_contains_fish` to `false` and `fish_details` to an empty object.
    """

    body = {
    "messages": [
        {
            "role": "system",
            "content": system_content
        },
        {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": user_message,
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64, {pic_string}"
                }
                }
            ]
        }
    ],
    "project_id": project_id,
    # "model_id": "meta-llama/llama3-llava-next-8b-hf",
    # "model_id": "meta-llama/llama-3-2-11b-vision-instruct",
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

    json_string = data['choices'][0]['message']['content']

    # Validate and parse the JSON response
    try:
        json_data = json.loads(json_string)
        if not isinstance(json_data, dict):
            raise ValueError("Response is not a valid JSON object")
        if "image_contains_fish" not in json_data or "fish_details" not in json_data:
            raise ValueError("Response JSON is missing required keys")
        if json_data["image_contains_fish"] and not json_data["fish_details"]:
            raise ValueError("Fish details should not be empty if image_contains_fish is true")
        return json_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}")

