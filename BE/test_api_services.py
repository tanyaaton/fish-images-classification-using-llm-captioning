import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_search():
    url = f"{BASE_URL}/search"
    payload = {"text": "colorful tropical fish"}
    response = requests.post(url, json=payload)
    print("/search response:", response.status_code)
    print(response.json())

def test_search2():
    url = f"{BASE_URL}/search"
    payload = {"text": "What is Clark's anemonefish appearance look like?"}
    response = requests.post(url, json=payload)
    print("/search response:", response.status_code)
    print(response.json())

def test_image_captioning():
    url = f"{BASE_URL}/image_captioning"
    # Use a real COS object key for testing
    payload = {"image": "indian-mackerel-003.png"}
    response = requests.post(url, json=payload)
    print("/image_captioning response:", response.status_code)
    print(response.json())

def test_generation():
    url = f"{BASE_URL}/generation"
    payload = {
        "question": "What does Lion fish look like?",
        "chat_history": [
            {"role": "user", "content": "Can you tell me about clownfish?"},
            {"role": "assistant", "content": "Clownfish are known for their symbiosis with sea anemones."},
            {"role": "user", "content": "What about Clark's anemonefish?"},
            {"role": "assistant", "content": "Clark's anemonefish is a clownfish with distinctive white stripes and various color morphs. It lives in symbiosis with sea anemones throughout the Indo-Pacific."}
        ]
    }
    response = requests.post(url, json=payload)
    print("/generation response:", response.status_code)
    print(response.json())

if __name__ == "__main__":
    print("Testing /search...")
    test_search()
    print("Testing /search2...")
    test_search2()
    print("\nTesting /image_captioning...")
    test_image_captioning()
    print("\nTesting /generation...")
    test_generation()
