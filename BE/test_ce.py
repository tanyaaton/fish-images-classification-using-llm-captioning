import requests

url = "https://snowflake-embedding.1xlkl2nudnhu.us-south.codeengine.appdomain.cloud/extract_text"
payload = {"sentence": "hello world"}
response = requests.post(url, json=payload)

print(response.json())