import chromadb
chroma = chromadb.HttpClient(host="localhost", port=8000)
collection = chroma.get_collection("fragments_on_machines")  # Get the collection by name
chroma.heartbeat()
print("ChromaDB is running and the collection is accessible.")