import requests
import json

BASE_URL = "http://127.0.0.1:8080"
# BASE_URL = "https://fish-image-classify.1xlkl2nudnhu.us-south.codeengine.appdomain.cloud"

def test_search_tropical_fish_query():
    """Test search endpoint with general tropical fish query"""
    url = f"{BASE_URL}/search"
    payload = {"text":
            """
                "body": "The fish has an oval-shaped body with a rounded head and a relatively small size, approximately 3-5 inches in length.", 
                "colors": "It features vibrant orange coloration with white stripes and black outlines, creating a striking pattern.", 
                "features": "The fish has large dorsal and anal fins, with a distinctive rounded tail fin and small scales.", 
                "unique_marks": "A prominent black stripe runs across the eyes, and the fish has a small mouth with a pointed snout."
            """
    }
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
    payload = {"image": "user-upload/1753251768437-clownfish.jpg"}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Error response text:", response.text)
    # Assertions
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    response_data = response.json()
    assert isinstance(response_data, dict), "Response should be a dictionary"
    # Assuming the response contains a caption or description
    assert len(str(response_data)) > 0, "Response should not be empty"
    print("/image_captioning Indian mackerel response:", response.status_code)
    print(response_data)

def test_image_identification_clownfish():
    """Test image identification endpoint with a clownfish image"""
    url = f"{BASE_URL}/image_identification"
    # Use a real COS object key for testing
    payload = {"image": "user-upload/1753251768437-clownfish.jpg"}
    response = requests.post(url, json=payload)

    # Print error response if status code is not 200
    if response.status_code != 200:
        print("Error response text:", response.text)

    # Assertions
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    response_data = response.json()
    assert isinstance(response_data, dict), "Response should be a dictionary"

    # Validate the response structure
    assert "image_contains_fish" in response_data, "Key 'image_contains_fish' missing in response"
    assert "fish_details" in response_data, "Key 'fish_details' missing in response"

    # If the image contains a fish, ensure fish_details is not empty
    if response_data["image_contains_fish"]:
        assert isinstance(response_data["fish_details"], dict), "'fish_details' should be a dictionary"
        assert len(response_data["fish_details"]) > 0, "'fish_details' should not be empty if 'image_contains_fish' is true"

    print("/image_identification clownfish response:", response.status_code)
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

def test_image_identification():
    """Test image cap endpoint with specific image and search pipeline"""
    # Step 1: Caption the image
    caption_url = f"{BASE_URL}/image_captioning"
    payload = {"image": "user-upload/1753849543267-17538495276807584572416837090045.jpg"}
    caption_response = requests.post(caption_url, json=payload)
    assert caption_response.status_code == 200, f"Expected status 200, got {caption_response.status_code}"
    caption_data = caption_response.json()
    assert isinstance(caption_data, dict), "Caption response should be a dictionary"
    assert "caption" in caption_data, "Caption key missing in response"
    caption_text = caption_data["caption"]
    print("Image caption:", caption_text)

    # Step 2: Use the caption to search for fish
    search_url = f"{BASE_URL}/search"
    search_payload = {"text": caption_text}
    search_response = requests.post(search_url, json=search_payload)
    assert search_response.status_code == 200, f"Expected status 200, got {search_response.status_code}"
    search_data = search_response.json()
    assert isinstance(search_data, dict), "Search response should be a dictionary"
    assert "results" in search_data, "Results key missing in search response"
    assert len(search_data["results"]) > 0, "Search results should not be empty"
    print("/search clownfish search response:", search_response.status_code)
    print(search_data)

def test_search_with_scientific_name(fish_name="Arothron hispidus"):
    """Test /search_with_sciencetific_name endpoint for single fish result"""
    url = f"{BASE_URL}/search_with_sciencetific_name"
    payload = {"scientific_name": fish_name}
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    response_data = response.json()
    assert isinstance(response_data, dict), "Response should be a dictionary"
    assert "scientific_name" in response_data, "scientific_name key missing in response"
    assert "fish_data" in response_data, "fish_data key missing in response"
    assert "message" in response_data, "message key missing in response"
    # Check that only 1 result is returned (or 0 if not found)
    assert isinstance(response_data["fish_data"], list), "fish_data should be a list"
    assert len(response_data["fish_data"]) <= 1, "Should return at most 1 fish"
    # Check all expected fields except embedding and score
    if response_data["fish_data"]:
        fish = response_data["fish_data"][0]
        expected_fields = [
            "fish_name", "thai_fish_name", "scientific_name", "order_name",
            "general_description", "physical_description", "habitat",
            "avg_length_cm", "avg_age_years", "avg_depthlevel_m", "avg_weight_kg"
        ]
        for field in expected_fields:
            assert field in fish, f"{field} missing in fish_data"
        assert "embedding" not in fish, "embedding field should not be present"
        assert "score" not in fish, "score field should not be present"
    print("/search_with_sciencetific_name response:", response.status_code)
    print(response_data)




if __name__ == "__main__":
    # print("Testing /search with tropical fish query...")
    # test_search_tropical_fish_query()
    # print("\nTesting /search with Clark's anemonefish appearance query...")
    # test_search_clarks_anemonefish_appearance()
    # print("\nTesting /image_captioning with Indian mackerel...")
    # test_image_captioning_indian_mackerel()
    # print("\nTesting /generation with lionfish appearance and chat history...")
    # test_generation_lionfish_appearance_with_chat_history()
    # print("\nTesting /image_identification with image...")
    # test_image_identification()
    # print("\nTesting /search_with_sciencetific_name with fish context...")
    # test_search_with_scientific_name("Arothron hispidus")
    print("\nTesting /image_identification with clownfish image...")
    test_image_identification_clownfish()

