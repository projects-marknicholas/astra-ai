from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from modules.config import UPLOAD_FOLDER, INTRODUCTION
from pycache.generate import *
from pycache.analyze import *
from modules.db import LocalStorageDB

app = Flask(__name__)
CORS(app)
storage = LocalStorageDB()

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/generate", methods=["POST"])
def process_request():
    prompt = request.form.get("prompt", "").strip()
    user_prompt = INTRODUCTION + " " + prompt
    file = request.files.get("file")

    if not prompt:
        return jsonify({"status": "error", "message": "Prompt is required"}), 400

    if file:
        file_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, file.filename))
        file_extension = os.path.splitext(file_path)[-1].lower()
        file.save(file_path) 

        if file_extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]:
            return jsonify({"status": "success", "intent": "analyze-image", "result": analyze_image(file_path, user_prompt, prompt)})
        elif file_extension in [".mp3", ".wav", ".ogg", ".flac", ".aac"]:
            return jsonify({"status": "success", "intent": "analyze-audio", "result": analyze_audio(file_path, user_prompt, prompt)})
        elif file_extension == ".pdf":
            return jsonify({"status": "success", "intent": "analyze-file", "result": analyze_file(file_path, user_prompt, prompt)})
    else:
        intent = classify_intent(user_prompt)
        if intent == "text":
            return jsonify({"status": "success", "intent": "text", "result": generate_text(user_prompt, prompt)})
        elif intent == "image":
            return jsonify({"status": "success", "intent": "image", "result": generate_image(prompt=user_prompt, question=prompt, width=1024, height=1024, seed=123, model="flux", enhance=True)})
        elif intent == "analyze-code":
            return jsonify({"status": "success", "intent": "analyze-code", "result": analyze_code(user_prompt, prompt)})
        elif intent == "map":
            return jsonify({"status": "success", "intent": "map", "result": generate_map(user_prompt, prompt)})
        return jsonify({"status": "error", "message": "Could not determine intent."}), 400
    
@app.route("/deepthink", methods=["POST"])
def process_deepthink():
    prompt = request.form.get("prompt", "").strip()
    user_prompt = INTRODUCTION + " " + prompt

    if not prompt:
        return jsonify({"status": "error", "message": "Prompt is required"}), 400

    return jsonify({"status": "success", "intent": "deepthink", "result": generate_deepthink(user_prompt, prompt)})

@app.route("/text-embedding", methods=["POST"])
def text_embedding():
    prompt = request.form.get("prompt", "").strip()

    if not prompt:
        return jsonify({"status": "error", "message": "Prompt is required"}), 400

    return jsonify({"status": "success", "intent": "text-embedding", "result": generate_text_embedding(prompt)})
    
@app.route("/history", methods=["GET"]) 
def get_history():
    """Retrieve stored prompt-response pairs from SQLite"""
    history = storage.get_all()
    formatted_history = [{"prompt": item["prompt"],"image": item["image"], "file_path": item["file_path"], "response": item["response"]} for item in history]
    return jsonify({"status": "success", "history": formatted_history})

@app.route("/delete", methods=["DELETE"])
def delete_history():
    try:
        history = storage.cleanup()
        return jsonify({"status": "success", "message": "Deleted successfully!"})
    except Exception as e:
        print(f"Error during deletion: {e}")
        return jsonify({"status": "error", "message": "Deletion failed."}), 500

if __name__ == "__main__":
    app.run(debug=True)
