from flask import Flask, request, jsonify
from watsonx_captioning import convert_image_to_base64, get_fish_description_from_watsonxai
from elasticsearch_query import ElasticsearchQuery
from embedding_service import EmbeddingService
from function import return_top_n_fish
from generation import get_generated_response
import os
from dotenv import load_dotenv
import ibm_boto3
from ibm_botocore.client import Config
import io


load_dotenv()
es_endpoint = os.environ["es_endpoint"]
es_username = os.environ["es_username"]
es_password = os.environ["es_password"]
index_name = 'fish_index_v3'
esq = ElasticsearchQuery(es_endpoint, es_username, es_password)
emb = EmbeddingService('watsonx')

app = Flask(__name__)

# Dummy fallback response
def fallback_response(service_name):
    return {"error": f"{service_name} service unavailable", "fallback": True}

@app.route("/live", methods=["GET"])
def live():
    return jsonify(status="ok"), 200


@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json()
        text_input = data.get("text", "")
        if not text_input:
            return jsonify({"error": "No text input provided"}), 400

        caption_embedding = emb.embed_text(text_input)
        hits = esq.search_embedding(index_name=index_name, embedding_field='embedding', query_vector=caption_embedding, size=5)
        top_n_fish = return_top_n_fish(hits, n=5)
        return jsonify({"input": text_input, "results": top_n_fish})
    except Exception as e:
        return jsonify(fallback_response("search")), 503

# This service might take a while to respond due to image processing
@app.route("/image_captioning", methods=["POST"])
def image_captioning():
    try:
        data = request.get_json()
        image = data.get("image", "")
        if image:
            # Try to fetch from COS if image is an object key
            try:
                api_key = os.environ.get('IBM_COS_API_KEY')
                resource_instance_id = os.environ.get('IBM_COS_RESOURCE_INSTANCE_ID')
                endpoint_url = os.environ.get('IBM_COS_ENDPOINT')
                cos = ibm_boto3.client(
                    's3',
                    ibm_api_key_id=api_key,
                    ibm_service_instance_id=resource_instance_id,
                    config=Config(signature_version='oauth'),
                    endpoint_url=endpoint_url
                )
                response = cos.get_object(Bucket='fish-image-bucket', Key=image)
                image_bytes = response['Body'].read()
                # Convert bytes to base64 string
                import base64
                pic_string = base64.b64encode(image_bytes).decode('utf-8')
            except Exception as cos_e:
                # fallback to local path if not found in COS
                image_path = image
                pic_string = convert_image_to_base64(image_path)
        else:
            # no image provided, return error
            return jsonify({"error": "No image provided"}), 400
        caption = get_fish_description_from_watsonxai(pic_string)
        return jsonify({"caption": caption})
    except Exception as e:
        print(f"Error in image_captioning: {e}")
        return jsonify(fallback_response("image_captioning")), 503

@app.route("/generation", methods=["POST"])
def generation():
    try:
        data = request.get_json()
        question = data.get("question", "")
        chat_history = data.get("chat_history", [])  # List of previous messages

        response_text = get_generated_response(question, chat_history)
        return jsonify({"response": response_text})
    except Exception as e:
        import logging
        logging.error(f"Error in generation: {e}")
        return jsonify(fallback_response("generation")), 503
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
