from flask import Flask, request, jsonify
import base64
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
model_name = 'Snowflake/snowflake-arctic-embed-l-v2.0'
 
cache_directory = "/tmp/huggingface_models" # You can choose a sub-directory in /tmp

# Ensure the directory exists
import os
os.makedirs(cache_directory, exist_ok=True)
model = SentenceTransformer(model_name, cache_folder=cache_directory)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        data = request.get_json()
        sentences = data['sentence']
        embeddings = model.encode(sentences)
        return {
            'predictions': [
                {
                    'fields': ['sentence', 'embedding'],
                    'values': [[sentence, embedding.tolist()] for sentence, embedding in zip(sentences, embeddings)]
                }
            ]
        }

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
