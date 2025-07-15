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

conn_ibm_cloud_iam = http.client.HTTPSConnection(ibm_cloud_iam_url)
payload = "grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey="+watsonx_api_key
headers = { 'Content-Type': "application/x-www-form-urlencoded" }
conn_ibm_cloud_iam.request("POST", "/identity/token", payload, headers)
res = conn_ibm_cloud_iam.getresponse()
data = res.read()
decoded_json=json.loads(data.decode("utf-8"))
access_token=decoded_json["access_token"]



### input and descripe input image
image_path = "fish-pictures/fish-1.png"

def convert_image_to_base64(image_path):
    pic = open(image_path,"rb").read()
    pic_base64 = base64.b64encode(pic)
    pic_string = pic_base64.decode("utf-8")
    return pic_string


def get_fish_description_from_watsonxai(pic_string):
    system_content ="""You always answer the questions with markdown formatting using GitHub syntax. The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, and blockquotes. You must omit that you answer the questions with markdown.\n\nAny HTML tags must be wrapped in block quotes, for example ```<html>```. You will be penalized for not rendering code in block quotes.\n\nWhen returning code blocks, specify language.\n\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. \nYour answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don'\''t know the answer to a question, please don'\''t share false information."""
    user_message = """Please provide a detailed description of the fish in the image focusing on the following aspects:
    1. Body shape and size
    2. Coloration patterns and markings
    3. Distinctive features (fins, scales, head shape, etc.)
    4. Any unique identifying characteristics
    Return your answer only in JSON format as follows, do not provide any additional text or explanation:
    {
        'body': 'description of body shape and approximate size',
        'colors': 'detailed description of colors and patterns',
        'features': 'description of distinctive features',
        'unique_marks': 'any unique identifying characteristics'
    }"""

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



