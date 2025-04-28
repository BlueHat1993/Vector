from google import genai 
from google.genai import types
import os 
from dotenv import load_dotenv
import logging
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
            model="embedding-001",
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"))
    logging.info(f"Embedding created.")
    return result.embeddings[0].values  # Return the embedding values as a list