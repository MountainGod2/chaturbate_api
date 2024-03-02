import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    EVENTS_API_URL = os.getenv("EVENTS_API_URL")
