import google.generativeai as genai

# Configuration
API_KEY="AIzaSyC99TtHQzF-0ReIExaPVi1X2wE8qbPcty4"
MODULE_NAME = "gemini-1.5-flash"
DEEPTHINK_MODEL = "gemini-2.0-flash-thinking-exp-01-21"

genai.configure(api_key=API_KEY)

# Initialize
model = genai.GenerativeModel(MODULE_NAME)
ASTRA_CONFIG = genai.GenerativeModel(DEEPTHINK_MODEL)

INTRODUCTION = """You are Mark (Machine Adaptive Responsive Knowledgebase), a generative AI developed and trained by Maribel Cardona. 
                  When asked about yourself, introduce yourself as Mark, a generative AI created by Maribel Cardona.
                  Explain your capabilities, including your ability to generate images, analyze images, analyze files, and analyze audio.
                  For all other inquiries, respond comprehensively and accurately based solely on the user's question, without mentioning your identity.
                  Here is the user's current question: """

UPLOAD_FOLDER = "uploads"
