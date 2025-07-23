import os
from ibm_watsonx_ai import APIClient, Credentials
import getpass

credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com",
    api_key=getpass.getpass("Please enter your api key (hit enter): ")
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

print(project_id)

from ibm_watsonx_ai.foundation_models import ModelInference

model = ModelInference(
	model_id = model_id,
	params = parameters,
	credentials = credentials,
	project_id = project_id,
	space_id = space_id
	)


import ibm_watsonx_ai
print(ibm_watsonx_ai.__version__)


from ibm_watsonx_ai.foundation_models.utils import Toolkit

vector_index_id = "da27e903-5807-4897-b20a-1946195c00fe"

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

chat_messages = []

question = input("Question: ")
grounding = proximity_search(question)
chat_messages.append({
    "role": f"system",
    "content": f"""You always answer the questions with markdown formatting. The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, and blockquotes. You must omit that you answer the questions with markdown.

Please answer in the same language as the user's query.

Any HTML tags must be wrapped in block quotes, for example ```<html>```. You will be penalized for not rendering code in block quotes.

When returning code blocks, specify language.

Given the document and the current conversation between a user and an assistant, your task is as follows: answer any user query by using information from the document. Always answer as helpfully as possible, while being safe. When the question cannot be answered using the context or document, output the following response: "I cannot answer that question based on the provided document.".

Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.

### Context:
{grounding}

"""
})
chat_messages.append({"role": "user", "content": question})
generated_response = model.chat(messages=chat_messages)
print(generated_response)
