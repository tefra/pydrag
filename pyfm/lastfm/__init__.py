import os

from dotenv import load_dotenv

load_dotenv()

api_root_url = "http://ws.audioscrobbler.com/2.0/"
api_key = os.getenv("LASTFM_API_KEY")
