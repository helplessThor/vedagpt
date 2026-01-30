import os
import requests
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

# Configuration
CHROMA_DB_DIR = "chroma_db"
COLLECTION_NAME = "vedas"

# Archive.org Text URLs (Corrected)
DATA_SOURCES = {
    "RigVeda_Vol1": "https://archive.org/stream/rigveda-tulsiram-vol-1-to-vol-4/Rigveda_Tulsiram_Vol_1_djvu.txt",
    "RigVeda_Vol2": "https://archive.org/stream/rigveda-tulsiram-vol-1-to-vol-4/Rigveda_Tulsiram_Vol_2_djvu.txt",
    "RigVeda_Vol3": "https://archive.org/stream/rigveda-tulsiram-vol-1-to-vol-4/Rigveda_Tulsiram_Vol_3_djvu.txt",
    "RigVeda_Vol4": "https://archive.org/stream/rigveda-tulsiram-vol-1-to-vol-4/Rigveda_Tulsiram_Vol_4_djvu.txt",
    "SamaVeda": "https://archive.org/stream/samaveda_202212/samaveda_djvu.txt",
    "YajurVeda": "https://archive.org/stream/yajurveda_202212/yajurveda_djvu.txt",
    "AtharvaVeda_Vol1": "https://archive.org/stream/atharvaved-vol-1/Atharvaved_Vol1_djvu.txt",
    "AtharvaVeda_Vol2": "https://archive.org/stream/atharvaved-vol-1/Atharvaved_Vol2_djvu.txt",
}

def setup_chroma():
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # Reset collection to remove old incorrect data
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"Deleted existing collection '{COLLECTION_NAME}' to ensure clean slate.")
    except Exception:
        pass # Collection didn't exist

    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)
    return collection

def download_text(url):
    print(f"Downloading from {url}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def chunk_text(text, chunk_size=1000, overlap=100):
    """Simple sliding window chunking."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

def process_and_ingest(text, veda_name, collection):
    print(f"Processing {veda_name} (Length: {len(text)} chars)...")
    
    # Remove header/footer junk from Project Gutenberg if possible
    # (Simple heuristic: start after *** START OF THE PROJECT GUTENBERG EBOOK... ***)
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx+100:] # Skip marker
    
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]
        
    chunks = chunk_text(text)
    
    documents = []
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(chunks):
        documents.append(chunk)
        metadatas.append({"source": veda_name, "chunk_id": i})
        ids.append(f"{veda_name}_{i}")
        
        if len(documents) >= 100:
            collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
            documents = []
            metadatas = []
            ids = []
            print(f"Ingested {i} chunks...")
            
    if documents:
        collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
        
    print(f"Finished {veda_name}: {len(chunks)} chunks.")

def main():
    print("Starting Ingestion (Strategy B: Text Files)...")
    collection = setup_chroma()
    
    for name, url in DATA_SOURCES.items():
        text = download_text(url)
        if text:
            process_and_ingest(text, name, collection)
        else:
            print(f"Skipping {name}.")

    print("Ingestion Complete.")

if __name__ == "__main__":
    main()
