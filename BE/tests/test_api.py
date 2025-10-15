"""
Test examples for the updated API with chat history support

The API now accepts chat history in the generation endpoint.
"""

# Example 1: Testing /generation endpoint with chat history
import requests
import json

# Example chat history format
chat_history_example = [
    {"role": "user", "content": "What type of fish is this?"},
    {"role": "assistant", "content": "Based on the information provided, this appears to be a Grouper fish, specifically from the Serranidae family."},
    {"role": "user", "content": "What does it eat?"}
]

# Test the generation endpoint with chat history
def test_generation_with_history():
    url = "http://localhost:5000/generation"
    
    payload = {
        "question": "Where can I find this fish?",
        "reference": "Grouper fish (Serranidae family): Large predatory fish found in warm coastal waters. They typically inhabit coral reefs, rocky bottoms, and underwater structures. Diet consists of smaller fish, crustaceans, and squid.",
        "chat_history": chat_history_example
    }
    
    response = requests.post(url, json=payload)
    print("Response:", response.json())

# Test the generation endpoint without chat history (backward compatibility)
def test_generation_without_history():
    url = "http://localhost:5000/generation"
    
    payload = {
        "question": "What type of fish is this?",
        "reference": "Clownfish (Amphiprioninae): Small, brightly colored fish with orange and white stripes. They live in sea anemones in coral reefs."
    }
    
    response = requests.post(url, json=payload)
    print("Response:", response.json())

# Test the search endpoint
def test_search():
    url = "http://localhost:5000/search"
    
    payload = {
        "text": "orange fish with white stripes living in coral reef"
    }
    
    response = requests.post(url, json=payload)
    print("Response:", response.json())

# Test the image captioning endpoint
def test_image_captioning():
    url = "http://localhost:5000/image_captioning"
    
    payload = {
        "link_s3": "path/to/fish/image.jpg"  # Replace with actual image path
    }
    
    response = requests.post(url, json=payload)
    print("Response:", response.json())

if __name__ == "__main__":
    print("Testing API endpoints...")
    
    # Make sure your Flask app is running first
    print("\n1. Testing generation with chat history:")
    test_generation_with_history()
    
    print("\n2. Testing generation without chat history:")
    test_generation_without_history()
    
    print("\n3. Testing search:")
    test_search()
    
    print("\n4. Testing image captioning:")
    test_image_captioning()
