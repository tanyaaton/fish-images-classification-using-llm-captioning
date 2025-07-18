import os
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.utils import Toolkit

# --- Initialization (can be done once) ---
load_dotenv()

credentials = Credentials(
    url=os.getenv("WATSONXAI_URL"),
    api_key=os.getenv("WATSONX_APIKEY"),
)

model_id = "meta-llama/llama-3-3-70b-instruct"

parameters = {
    "frequency_penalty": 0,
    "max_tokens": 2000,
    "presence_penalty": 0,
    "temperature": 0,
    "top_p": 1
}

project_id = os.getenv("PROJECT_ID")
space_id = os.getenv("SPACE_ID")

model = ModelInference(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=project_id,
    space_id=space_id
)
# --- End Initialization ---


vector_index_id = os.getenv("VECTOR_INDEX_ID")

def proximity_search( query ):

    api_client = APIClient(
        project_id=project_id,
        credentials=credentials,
    )

    document_search_tool = Toolkit(
        api_client=api_client
    ).get_tool("RAGQuery")

    config = {
        "vectorIndexId": vector_index_id,
        "projectId": project_id
    }

    results = document_search_tool.run(
        input=query,
        config=config
    )

    return results.get("output")

def get_generated_response(question: str, chat_history: list = None):
    """
    Generates a response using watsonx.ai based on a question, grounding context, and chat history.
    
    Args:
        question (str): The current user question
        chat_history (list): List of previous chat messages in format [{"role": "user"|"assistant", "content": "..."}]
    """
    if chat_history is None:
        chat_history = []
    grounding = proximity_search(question)

    system_prompt = (
        "You are a helpful marine biology assistant specializing in fish identification and information. "
        "Answer the user's question based only on the provided fish species information and previous conversation context. "
        "When asked to identify a fish, provide information about the fish and other possible fish species based on the provided grounding information. "
        "Include details about fish characteristics, habitat, behavior, distinguishing features, size ranges, coloration patterns, and behavioral traits when available. "
        "If multiple species are possible matches, explain the differences between them. "
        "Keep your tone informative and friendly, and maintain conversation continuity from chat history. "
        "If there isn't enough information to answer, say 'I don't know.' "
        "Answer in the language of the question."
    )

    user_prompt = (
        f"Based on this fish information from grounding search: {grounding}\n\n"
        f"And this question: {question}\n\n"
        f"Please give a natural-sounding response considering our previous conversation."
    )

    # Build chat messages with history
    chat_messages = [{"role": "system", "content": system_prompt}]
    
    # Add chat history (limit to last 10 messages to avoid token limits)
    if chat_history:
        recent_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
        chat_messages.extend(recent_history)
    
    # Add current user question
    chat_messages.append({"role": "user", "content": user_prompt})
    
    response = model.chat(messages=chat_messages)
    
    print("Raw model response:", response)

    # Extract the generated text from the watsonx.ai response format
    if response and "choices" in response and len(response["choices"]) > 0:
        return response["choices"][0]["message"].get("content", "Error: Could not extract generated text.")
    else:
        return "Error: Invalid response from model."
    
# Example usage
if __name__ == "__main__":  
    # Test the function with a sample question and reference, simulating a multi-turn chat
    reference = "Clownfish: lives in sea anemones in coral reefs."
    chat_history = [
        {"role": "user", "content": "What type of fish is this?"},
        {"role": "assistant", "content": "This is a clownfish."},
        {"role": "user", "content": "What does it eat?"},
        {"role": "assistant", "content": "Clownfish eat small invertebrates and algae."}
    ]
    question = "I encounter a dark tone triggerfish with a red teeth what kind of fish is it?"
    response = get_generated_response(question, chat_history)
    print("Generated Response:", response)