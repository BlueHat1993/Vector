from google import genai 
import os 
from dotenv import load_dotenv
# Load environment variables from .env file if it exists
load_dotenv()


def create_embedding(text):
    """
    Creates an embedding using the Google GenAI API.
    
    Args:
        api_key (str): The API key for authentication.
        
    Returns:
        dict: The response from the API containing the embedding.
    """
    # Initialize the GenAI client with the provided API key
    api_key= os.getenv("API_KEY")
    client = genai.Client(api_key=api_key)
    result = client.models.embed_content(
            model="gemini-embedding-exp-03-07",
            contents=text)
    
    return result.embeddings