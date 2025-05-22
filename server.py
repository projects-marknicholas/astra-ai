# import google.generativeai as genai
# from google.generativeai import types
# import PIL.Image
# import base64
# from PIL import Image
# import matplotlib.pyplot as plt
# import requests
# from io import BytesIO
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os

# app = Flask(__name__)
# CORS(app, resources={r"/generate": {"origins": "*"}})

# # Configuration
# MODULE_NAME = 'gemini-1.5-flash'

# # Secure your API key (DO NOT hardcode in production)
# genai.configure(api_key="AIzaSyD-8j8CCw8SDwF8XV2g1kSYZeTHGvoz7bA")

# # Initialize the model
# model = genai.GenerativeModel(MODULE_NAME) 
# chat = model.start_chat()

# # Introduction
# INTRODUCTION = """You are Astra, an AI developed and trained by JMJ DeepMind. When asked about yourself, introduce yourself as Astra, an AI created by JMJ DeepMind. 
#                   Explain your capabilities, including your ability to generate and analyze images. 
#                   Additionally, you may share this link to your profile: https://web.facebook.com/profile.php?id=61565424895382.
#                   For all other inquiries, respond comprehensively and accurately based solely on the user's question, without mentioning your identity.
#                   Here is the user's current question: """

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Function to classify intent
# def classify_intent(prompt):
#     classification_prompt = f"""
#     Analyze the user's intent and return ONLY one word:
#     - "text" if the user wants text generation.
#     - "image" if the user wants image generation.
    
#     User input: "{prompt}"
    
#     ONLY return one of these words: "text" or "image".
#     """
#     response = model.generate_content(classification_prompt)
#     return response.text.strip().lower()  

# def generate_text(prompt):
#     response = chat.send_message(prompt)
#     # response = model.generate_content(prompt)
#     return response.text

# def generate_image(prompt, width=1024, height=1024, seed=42, model="flux", enhance=False):
#     encoded_prompt = requests.utils.quote(prompt)
#     url = f"https://pollinations.ai/p/{encoded_prompt} without pollination.ai mark/tag?width={width}&height={height}&seed={seed}&model={model}&nologo=true"
    
#     if enhance:
#         url += "&enhance=true"

#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             image_blob = BytesIO(response.content)
#             image = Image.open(image_blob)

#             # Convert image to Base64
#             buffered = BytesIO()
#             image.save(buffered, format="PNG")
#             base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

#             return base64_image
#         else:
#             return f"Error: Failed to fetch image. Status Code: {response.status_code}"

#     except Exception as e:
#         return f"Error: {str(e)}"
    
# def analyze_image(file_path, prompt="Describe this image"):
#     try:
#         with open(file_path, "rb") as image_file:
#             image = Image.open(image_file)
#             image.load() 

#         response = model.generate_content([prompt, image])
#         return response.text
#     except Exception as e:
#         return f"Error: {str(e)}"
    
# def analyze_audio(file_path, prompt="Describe this Audio"):
#     try:
#         with open(file_path, "rb") as f:
#             audio_data = f.read()

#         response = model.generate_content([
#             prompt,
#             {"mime_type": "audio/mpeg", "data": audio_data}
#         ])
#         return response.text
#     except Exception as e:
#         return f"Error: {str(e)}"

# def analyze_file(file_path, prompt):
#     try:
#         # Upload file
#         uploaded_file = genai.upload_file(file_path)

#         # Generate content
#         response = model.generate_content([prompt, uploaded_file])

#         return response.text if response else "No response generated."
#     except Exception as e:
#         return f"Error: {str(e)}"

# @app.route("/generate", methods=["POST"])
# def process_request():
#     prompt = request.form.get("prompt", "").strip()
#     user_prompt = INTRODUCTION + " " + prompt
#     file = request.files.get("file")
    
#     if not prompt:
#         return jsonify({"status": "error", "message": "Prompt is required"}), 400
    
#     if file:
#         file_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, file.filename))
#         file_extension = os.path.splitext(file_path)[-1].lower()
#         file.save(file_path)  # Save the uploaded file

#         if file_extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]:
#             return jsonify({"status": "success", "intent": "analyze-image", "result": analyze_image(file_path, user_prompt)})
#         elif file_extension in [".mp3", ".wav", ".ogg", ".flac", ".aac"]:
#             return jsonify({"status": "success", "intent": "analyze-audio", "result": analyze_audio(file_path, user_prompt)})
#         elif file_extension in [".pdf"]:
#             return jsonify({"status": "success", "intent": "analyze-file", "result": analyze_file(file_path, user_prompt)})
#     else:
#       # If no file is uploaded, classify the intent
#       intent = classify_intent(user_prompt)
#       if intent == "text":
#           return jsonify({"status": "success", "intent": "text", "result": generate_text(user_prompt)})
#       elif intent == "image":
#           return jsonify({"status": "success", "intent": "image", "result": generate_image(prompt=user_prompt, width=1024, height=1024, seed=123, model="flux", enhance=True)})

#       return jsonify({"status": "error", "message": "Could not determine intent."}), 400

# if __name__ == "__main__":
#     app.run(debug=True)
