import chromadb
client = chromadb.PersistentClient(path="chroma_db")
try:
    collection = client.get_collection("vedas")
    print(f"Collection count: {collection.count()}")
    # Peek to see what sources we have
    peek = collection.peek()
    sources = set()
    if peek['metadatas']:
         for m in peek['metadatas']:
             sources.add(m['source'])
    print(f"Sources found: {sources}")
except Exception as e:
    print(f"Error reading DB: {e}")
