import os
from dotenv import load_dotenv


BASE_PATH = os.path.dirname(os.path.abspath(__name__))
dotenv_path = os.path.join(BASE_PATH, "../.env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Tokens
SCRAPEOPS_TOKEN = os.getenv("SCRAPEOPS_API_KEY", "")

# URL's
INDEED_URL = ""
