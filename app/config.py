import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/images/generations"
DEFAULT_FALLBACK_IMAGE = "https://dummyimage.com/600x400/000/fff.png&text=Image+Unavailable"
