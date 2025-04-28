import chromadb
from chromadb.config import Settings
from embedding import *
from fileparser import *
from dotenv import load_dotenv
import os

# Load environment variables from .env file if it exists
load_dotenv()

chroma_client = chromadb.PersistentClient(path="chroma_db")

collections = chroma_client.list_collections()
collection = chroma_client.get_or_create_collection(name="fragments_on_machines")



def query(query_text, K=3):
    """
    Queries the ChromaDB collection for similar documents based on the provided text.
        Args:
        query_text (str): The text to query against the collection.
        n_results (int): The number of results to return.
        
    Returns:
        list: A list of documents that are similar to the query text.
    """
    results = collection.query(
        query_embeddings=[create_embedding(query_text)],  # Create an embedding for the query text
        n_results=K  # Number of results to return
    )
    return results  # Return the query results




file_path = os.getenv("FILE_PATH")  # Get the file path from the environment variable
text = read_pdf(file_path)  # Read the PDF file
logging.info(f"PDF file {file_path} read successfully.")
chunks = chunk_text(text)  # Chunk the text into smaller pieces
logging.info(f"Text chunked into {len(chunks)} chunks.")
ids = [f"doc_id_{i}" for i in range(len(chunks))]  # Create unique IDs for each chunk4
logging.info(f"Unique IDs created for {len(chunks)} chunks.")
embeddings =[create_embedding(c) for c in chunks]  # Create embeddings for each chunk
logging.info(f"Embeddings created for {len(chunks)} chunks.")
metadata = [{"source":file_path , "chunk_index": i} for i in range(len(chunks))]  # Create metadata for each chunk
logging.info(f"Metadata created for {len(chunks)} chunks.")
collection.upsert(
    documents=chunks,  # The text chunks to be added to the collection
    embeddings=embeddings,  # The embeddings for the text chunks
    ids=ids,  # Unique IDs for each chunk
    metadatas=metadata  # Metadata for each chunk
)   
logging.info(f"Upserted {len(chunks)} chunks into the collection.")

# Persist the collection to disk
chroma_client.heartbeat()
logging.info("Collection persisted to disk for future use.")


revelation = query("What will be the impact of automation?", K=3)  # Query the collection with a sample text
print(revelation)  # Print the query results