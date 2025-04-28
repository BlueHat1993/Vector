import chromadb
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_collection")
collection.add(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ],
    ids=["id1", "id2"]
)
results = collection.query(
    query_texts=["find a me a bigger fruit"], # Chroma will embed this for you
    n_results=1 # how many results to return
)
print(results)
