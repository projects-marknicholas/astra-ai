import os
import base64
from PIL import Image
from io import BytesIO
from modules.config import model
import google.generativeai as genai
from modules.db import LocalStorageDB

storage = LocalStorageDB()

def analyze_image(file_path, prompt, question):
    try:
        with open(file_path, "rb") as image_file:
            image = Image.open(image_file)
            image.load()

        response = model.generate_content([prompt, image])
        
        # Store conversation in local storage
        storage.set_item(question, response=response.text, file_path=file_path, intent="analyze-image")

        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_audio(file_path, prompt, question):
    try:
        with open(file_path, "rb") as f:
            audio_data = f.read()

        response = model.generate_content([
            prompt,
            {"mime_type": "audio/mpeg", "data": audio_data}
        ])
        
        # Store conversation in local storage
        storage.set_item(question, response=response.text, file_path=file_path, intent="analyze-audio")

        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_file(file_path, prompt, question):
    try:
        uploaded_file = genai.upload_file(file_path)
        response = model.generate_content([prompt, uploaded_file])
        
        # Store conversation in local storage
        storage.set_item(question, response=response.text, file_path=file_path, intent="analyze-file")

        return response.text if response else "No response generated."
    except Exception as e:
        return f"Error: {str(e)}"
    
def analyze_code(prompt, question):
    try:
        introduction = f"""
            Analyze the following code based on these rubrics:
            - Readability
            - Efficiency
            - Best practices
            - Code structure
            - Optimization suggestions
            
            Provide a score from 1-100 and give suggestions for improvement.
            
            Code:
            ```
            {prompt}
            ```
            """
        response = model.generate_content(introduction)

        # Store conversation in local storage
        storage.set_item(question, response=response.text, file_path=None, intent="analyze-code")
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

