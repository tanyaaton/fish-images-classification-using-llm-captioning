*** Settings ***
Library    RequestsLibrary

*** Variables ***
${BASE_URL}    http://127.0.0.1:8080
$

*** Test Cases ***
Search Tropical Fish Query
    [Documentation]    Test search endpoint with general tropical fish query
    Create Session    fish    ${BASE_URL}
    ${payload}=    Create Dictionary    text="body": "The fish has an oval-shaped body with a rounded head and a relatively small size, approximately 3-5 inches in length.", "colors": "It features vibrant orange coloration with white stripes and black outlines, creating a striking pattern.", "features": "The fish has large dorsal and anal fins, with a distinctive rounded tail fin and small scales.", "unique_marks": "A prominent black stripe runs across the eyes, and the fish has a small mouth with a pointed snout."
    ${response}=    Post Request    fish    /search    json=${payload}
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    To Json    ${response.content}
    Should Be True    ${data}    Response should be a dictionary

Search Clarks Anemonefish Appearance
    [Documentation]    Test search endpoint with specific Clark's anemonefish appearance query
    Create Session    fish    ${BASE_URL}
    ${payload}=    Create Dictionary    text=What is Clark's anemonefish appearance look like?
    ${response}=    Post Request    fish    /search    json=${payload}
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    To Json    ${response.content}
    Should Be True    ${data}    Response should be a dictionary

Image Captioning Indian Mackerel
    [Documentation]    Test image captioning endpoint with Indian mackerel image
    Create Session    fish    ${BASE_URL}
    ${payload}=    Create Dictionary    image=user-upload/1753251768437-clownfish.jpg
    ${response}=    Post Request    fish    /image_captioning    json=${payload}
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    To Json    ${response.content}
    Should Be True    ${data}    Response should be a dictionary

Image Identification Clownfish
    [Documentation]    Test image identification endpoint with a clownfish image
    Create Session    fish    ${BASE_URL}
    ${payload}=    Create Dictionary    image=user-upload/1753251768437-clownfish.jpg
    ${response}=    Post Request    fish    /image_identification    json=${payload}
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    To Json    ${response.content}
    Dictionary Should Contain Key    ${data}    image_contains_fish
    Dictionary Should Contain Key    ${data}    fish_details

Generation Lionfish Appearance With Chat History
    [Documentation]    Test generation endpoint asking about lionfish appearance with chat history context
    Create Session    fish    ${BASE_URL}
    ${chat_history}=    Create List
    ...    {"role": "user", "content": "Can you tell me about clownfish?"}
    ...    {"role": "assistant", "content": "Clownfish are known for their symbiosis with sea anemones."}
    ...    {"role": "user", "content": "What about Clark's anemonefish?"}
    ...    {"role": "assistant", "content": "Clark's anemonefish is a clownfish with distinctive white stripes and various color morphs. It lives in symbiosis with sea anemones throughout the Indo-Pacific."}
    ${payload}=    Create Dictionary    question=What does Lion fish look like?    chat_history=${chat_history}
    ${response}=    Post Request    fish    /generation    json=${payload}
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    To Json    ${response.content}
    Should Be True    ${data}    Response should be a dictionary

Search With Scientific Name
    [Documentation]    Test /search_with_scientific_name endpoint for single fish result
    Create Session    fish    ${BASE_URL}
    ${payload}=    Create Dictionary    scientific_name=Arothron hispidus
    ${response}=    Post Request    fish    /search_with_scientific_name    json=${payload}
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    To Json    ${response.content}
    Dictionary Should Contain Key    ${data}    scientific_name
    Dictionary Should Contain Key    ${data}    fish_data
    Dictionary Should Contain Key    ${data}    message
