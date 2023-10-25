import os
from dotenv import load_dotenv

# load .env
load_dotenv(dotenv_path='./.env')

botToken = os.environ.get("TOKEN")