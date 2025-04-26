from google import genai 
import os 
from dotenv import load_dotenv
# Load environment variables from .env file if it exists
load_dotenv()
api_key= os.getenv("API_KEY")
client = genai.Client(api_key=api_key)
result = client.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents="What is the meaning of life?")

print(result)