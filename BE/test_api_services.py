import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_search():
    url = f"{BASE_URL}/search"
    payload = {"text": "colorful tropical fish"}
    response = requests.post(url, json=payload)
    print("/search response:", response.status_code)
    print(response.json())

def test_image_captioning():
    url = f"{BASE_URL}/image_captioning"
    payload = {"link_s3": "fish-pictures/fish-1.png"}  # Use local path for demo
    response = requests.post(url, json=payload)
    print("/image_captioning response:", response.status_code)
    print(response.json())

def test_generation():
    url = f"{BASE_URL}/generation"
    payload = {
        "question": "What is the most common fish in Thailand?",
        "chat_history": []
    }
    response = requests.post(url, json=payload)
    print("/generation response:", response.status_code)
    print(response.json())

if __name__ == "__main__":
    print("Testing /search...")
    test_search()
    print("\nTesting /image_captioning...")
    test_image_captioning()
    print("\nTesting /generation...")
    test_generation()
