import chromadb
from chromadb.config import Settings
from embedding import *
from fileparser import *
from dotenv import load_dotenv
import os

# Load environment variables from .env file if it exists
load_dotenv()


chroma_client = chromadb.Client(Settings(persist_directory="./chroma_db"))
collection = chroma_client.get_or_create_collection(name="fragments_on_machines")

file_path = os.getenv("FILE_PATH")  # Get the file path from the environment variable
text = read_pdf(file_path)  # Read the PDF file
chunks = chunk_text(text)  # Chunk the text into smaller pieces
ids = [f"doc_id_{i}" for i in range(len(chunks))]  # Create unique IDs for each chunk
embeddings =[create_embedding(c) for c in chunks]  # Create embeddings for each chunk
metadata = [{"source":file_path , "chunk_index": i} for i in range(len(chunks))]  # Create metadata for each chunk
collection.upsert(
    documents=chunks,  # The text chunks to be added to the collection
    embeddings=embeddings,  # The embeddings for the text chunks
    ids=ids,  # Unique IDs for each chunk
    metadatas=metadata  # Metadata for each chunk
)   


