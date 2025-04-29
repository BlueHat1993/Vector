from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
import os 
from dotenv import load_dotenv
import chromadb
from embedding import *

chroma = chromadb.HttpClient(host="localhost", port=9010)
collection = chroma.get_collection("fragments_on_machines")

load_dotenv()

# rag pipeline tool for retrieving documents from the vector database
def rag_pipeline_tool(query: str)-> dict:
    """
    Queries the ChromaDB collection for similar documents based on the provided query.
    
    Args:
        query (str): The query text to search for similar documents.
        
    Returns:
        dict: A dictionary containing the query and a list of results with documents and their scores.
    """
    results = collection.query(
        query_embeddings=[create_embedding(query)],  # Create an embedding for the query text
        n_results=3  # Number of results to return
    )
    return {
        "query": query,
        "results": [
            {
                "document": result
            } for result in results["documents"]
        ]
    }

root_agent = Agent(
    name=os.getenv("AGENT_NAME"),
    model=os.getenv("MODEL_NAME"),
    description=(
        "Agent to answer questions based on documents retrieved from a vector database."
    ),
    instruction=(
        """
        You are an intelligent assistant helping a user based on retrieved documents from vector database.
        You will be provided with a question and a set of documents.
        Your task is to answer the question based on the provided documents.
        """
    ),
    tools=[rag_pipeline_tool]
)
