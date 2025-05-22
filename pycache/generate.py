import requests
import urllib.parse
import base64
from io import BytesIO
from PIL import Image
import time
from modules.config import *
from modules.db import LocalStorageDB

chat = model.start_chat()
storage = LocalStorageDB()

def classify_intent(prompt):
    classification_prompt = f"""
    Analyze the user's intent and return ONLY one word:
    - "text" if the user is asking for information, facts, or an explanation (e.g., questions about events, descriptions, or facts).
    - "image" if the user is asking for image generation (e.g., creating or modifying images).
    - "analyze-code" if the user is asking to analyze or debug a piece of code.
    - "map" if the user is asking for a location or a map visualization (e.g., requesting directions or a location on a map).

    User input: "{prompt}"

    ONLY return one of these words: "text", "image", "analyze-code", or "map".
    """

    response = model.generate_content(classification_prompt)
    return response.text.strip().lower()

def generate_text(prompt, question):
    response = chat.send_message(prompt)

    # Store conversation in local storage
    storage.set_item(question, response=response.text, file_path="", intent="text")

    return response.text

def generate_image(prompt, question, width=1024, height=1024, seed=42, model="flux", enhance=False):
    encoded_prompt = requests.utils.quote(prompt)
    url = f"https://pollinations.ai/p/{encoded_prompt} without pollination.ai mark/tag?width={width}&height={height}&seed={seed}&model={model}&nologo=true"
    
    if enhance:
        url += "&enhance=true"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_blob = BytesIO(response.content)
            image = Image.open(image_blob)

            # Convert image to Base64
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # Store conversation in local storage
            storage.set_item(question, image=base64_image, file_path="", intent="image")

            return base64_image
        else:
            return f"Error: Failed to fetch image. Status Code: {response.status_code}"

    except Exception as e:
        return f"Error: {str(e)}"

def generate_deepthink(prompt, question):
    try:
        response = ASTRA_CONFIG.generate_content(prompt)

        # Store conversation in local storage
        storage.set_item(question, response=response.text, file_path="", intent="deepthink")

        return response.text

    except Exception as e:
        print(f"Error: {str(e)}")

def generate_map(prompt, question):
    extract_place_prompt = f"""
    Extract only the place or location from the following prompt.
    Return ONLY the name of the place, without any explanation, extra text, or punctuation.

    User prompt: "{prompt}"
    """
    response = model.generate_content(extract_place_prompt)
    place_name = response.text.strip()

    place_query = urllib.parse.quote(place_name)

    link = f"https://www.openstreetmap.org/search?query={place_query}"

    # Store and return the link
    storage.set_item(question, response=link, file_path="", intent="map")
    return link

def generate_text_embedding(prompt):
    try:
        response = genai.embed_content(
            model='models/text-embedding-004',
            content=prompt
        )

        return response
    except Exception as e:
        print(f"Error: {str(e)}")