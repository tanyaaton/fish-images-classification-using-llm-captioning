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

from embedding_service import EmbeddingService
from elasticsearch_query import ElasticsearchQuery
from function import return_top_n_fish

# Initialize embedding and elasticsearch services
es_endpoint = os.environ["es_endpoint"]
es_username = os.environ["es_username"]
es_password = os.environ["es_password"]
index_name = 'fish_index_v3'
esq = ElasticsearchQuery(es_endpoint, es_username, es_password)
emb = EmbeddingService('watsonx')

def get_generated_response(question: str, chat_history: list = None):
    """
    Generates a response using watsonx.ai based on a question, reference context, and chat history.
    Uses embedding search for reference only for fish identification questions.
    """
    if chat_history is None:
        chat_history = []

    # Always generate reference using embedding search (use online embedding service)
    caption_embedding = emb.embed_text(question)
    hits = esq.search_embedding(index_name=index_name, embedding_field='embedding', query_vector=caption_embedding, size=5)
    top_n_fish = return_top_n_fish(hits, n=5)
    reference = "\n".join([
        f"{fish.get('fish_name', 'Unknown')}: {fish.get('description', '')} (score: {fish.get('score', '')})"
        for fish in top_n_fish
    ])

    print("Reference for question:", reference)

    system_prompt = (
        "You are a helpful marine biology assistant specializing in fish identification and information. "
        "You will always be provided with reference information about similar fish species, including their names, descriptions, and similarity scores. "
        "For fish identification or fish information questions, use the reference to check if the fish mentioned by the user appears in the reference list. "
        "If the fish is found in the reference, use its information to answer the question. "
        "If the question is about the fish and it is not found in the reference, inform the user that it does not appear to be one of the 91 species in our database. "
        "If the user's question is generic or unclear (such as 'yes', 'okay', 'please', etc.), answer based on the previous conversation context. "
        "When answering, include details about fish characteristics, habitat, behavior, distinguishing features, size ranges, coloration patterns, and behavioral traits when available. "
        "If multiple species are possible matches, explain the differences between them. "
        "Keep your tone informative and friendly, and maintain conversation continuity from chat history. "
        "If there isn't enough information to answer, say 'I don't know.' "
        "Always answer in the language of the question."
    )

    user_prompt = (
        f"Reference information about similar fish species (names, descriptions, similarity scores):\n{reference}\n\n"
        f"Question: {question}\n\n"
        "If the question is about a specific fish, check if it is present in the reference list above. If so, use its information to answer. If not, inform the user that it does not appear to be one of the 91 species in our database. For other questions, answer naturally based on our previous conversation."
    )

    # Build chat messages with history
    chat_messages = [{"role": "system", "content": system_prompt}]
    if chat_history:
        recent_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
        chat_messages.extend(recent_history)
    chat_messages.append({"role": "user", "content": user_prompt})

    response = model.chat(messages=chat_messages)
    print("Raw model response:", response)

    if response and "choices" in response and len(response["choices"]) > 0:
        return response["choices"][0]["message"].get("content", "Error: Could not extract generated text.")
    else:
        return "Error: Invalid response from model."
