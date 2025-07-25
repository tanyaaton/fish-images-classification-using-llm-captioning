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
import logging
import base64


load_dotenv()
es_endpoint = os.environ["es_endpoint"]
es_username = os.environ["es_username"]
es_password = os.environ["es_password"]
index_name = 'fish_index_v3'
esq = ElasticsearchQuery(es_endpoint, es_username, es_password)
emb = EmbeddingService('watsonx')

app = Flask(__name__)

# Dummy fallback response
def fallback_response(service_name, error_msg=None):
    resp = {"error": f"{service_name} service unavailable", "fallback": True}
    if error_msg:
        resp["details"] = error_msg
    return resp

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
        print(f"Error in search: {e}")
        app.logger.error(f"Error in generation: {e}")

# This service might take a while to respond due to image processing
@app.route("/image_captioning", methods=["POST"])
def image_captioning():
    try:
        data = request.get_json()
        image = data.get("image", "")
        app.logger.info(f"Received image: {image}")
        if not image:
            app.logger.error("No image provided in request")
            return jsonify({"error": "No image provided"}), 400

        # COS fetch block
        try:
            app.logger.info("loading COS credentials")
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
            app.logger.info(f"Fetching image from COS: {image}")
            response = cos.get_object(Bucket='fish-image-bucket', Key=image)
            image_bytes = response['Body'].read()
        except Exception as cos_e:
            app.logger.error(f"COS fetch error: {cos_e}")
            return jsonify(fallback_response("image_captioning", f"COS fetch error: {cos_e}")), 503

        # Base64 conversion block
        try:
            app.logger.info("Converting image to base64")
            pic_string = base64.b64encode(image_bytes).decode('utf-8')
        except Exception as b64_e:
            app.logger.error(f"Base64 conversion error: {b64_e}")
            return jsonify(fallback_response("image_captioning", f"Base64 error: {b64_e}")), 503

        # WatsonX call block
        try:
            app.logger.info("Calling WatsonX for image captioning")
            caption = get_fish_description_from_watsonxai(pic_string)
        except Exception as ai_e:
            app.logger.error(f"WatsonX error: {ai_e}")
            return jsonify(fallback_response("image_captioning", f"WatsonX error: {ai_e}")), 503

        return jsonify({"caption": caption})
    except Exception as e:
        app.logger.error(f"Unknown error in image_captioning: {e}")
        return jsonify(fallback_response("image_captioning", str(e))), 503

@app.route("/generation", methods=["POST"])
def generation():
    try:
        data = request.get_json()
        question = data.get("question", "")
        chat_history = data.get("chat_history", [])  # List of previous messages

        response_text = get_generated_response(question, chat_history)
        return jsonify({"response": response_text})
    except Exception as e:
        print(f"Error in image_captioning: {e}")
        app.logger.error(f"Error in generation: {e}")
        return jsonify(fallback_response("generation", str(e))), 503
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
