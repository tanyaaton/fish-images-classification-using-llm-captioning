import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_search_tropical_fish_query():
    """Test search endpoint with general tropical fish query"""
    url = f"{BASE_URL}/search"
    payload = {"text": "colorful tropical fish"}
    response = requests.post(url, json=payload)
    
    # Assertions
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    response_data = response.json()
    assert isinstance(response_data, dict), "Response should be a dictionary"
    print("/search tropical fish response:", response.status_code)
    print(response_data)

def test_search_clarks_anemonefish_appearance():
    """Test search endpoint with specific Clark's anemonefish appearance query"""
    url = f"{BASE_URL}/search"
    payload = {"text": "What is Clark's anemonefish appearance look like?"}
    response = requests.post(url, json=payload)
    
    # Assertions
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    response_data = response.json()
    assert isinstance(response_data, dict), "Response should be a dictionary"
    print("/search Clark's anemonefish response:", response.status_code)
    print(response_data)

def test_image_captioning_indian_mackerel():
    """Test image captioning endpoint with Indian mackerel image"""
    url = f"{BASE_URL}/image_captioning"
    # Use a real COS object key for testing
    payload = {"image": "indian-mackerel-003.png"}
    response = requests.post(url, json=payload)
    
    # Assertions
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    response_data = response.json()
    assert isinstance(response_data, dict), "Response should be a dictionary"
    # Assuming the response contains a caption or description
    assert len(str(response_data)) > 0, "Response should not be empty"
    print("/image_captioning Indian mackerel response:", response.status_code)
    print(response_data)

def test_generation_lionfish_appearance_with_chat_history():
    """Test generation endpoint asking about lionfish appearance with chat history context"""
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
    
    # Assertions
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    response_data = response.json()
    assert isinstance(response_data, dict), "Response should be a dictionary"
    # Assuming the response contains generated text about lionfish
    assert len(str(response_data)) > 0, "Response should not be empty"
    print("/generation lionfish appearance response:", response.status_code)
    print(response_data)

if __name__ == "__main__":
    print("Testing /search with tropical fish query...")
    test_search_tropical_fish_query()
    print("\nTesting /search with Clark's anemonefish appearance query...")
    test_search_clarks_anemonefish_appearance()
    print("\nTesting /image_captioning with Indian mackerel...")
    test_image_captioning_indian_mackerel()
    print("\nTesting /generation with lionfish appearance and chat history...")
    test_generation_lionfish_appearance_with_chat_history()
