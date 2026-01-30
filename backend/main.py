from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv

# Load .env from the same directory as this file
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="VedaGPT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for dev simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -- Configuration --
CHROMA_DB_DIR = "chroma_db"
COLLECTION_NAME = "vedas"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -- Init Clients --
if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY not found in env.")

groq_client = Groq(api_key=GROQ_API_KEY)

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "VedaGPT API is running"}

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    query = req.message
    print(f"Received Query: {query}")
    
    # 1. Retrieve Context from Vedas
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    
    context_list = results['documents'][0]
    sources_list = results['metadatas'][0]
    
    context_str = "\n\n".join(context_list)
    sources_str = ", ".join([s['source'] for s in sources_list])
    
    # 2. System Prompt
    system_prompt = f"""You are VedaGPT, a wise and enlightened AI assistant rooted in the knowledge of the 4 Vedas (Rig, Sama, Yajur, Atharva).
    
    CONTEXT FROM VEDAS:
    {context_str}
    
    INSTRUCTIONS:
    - Answer the user's question using the context provided above.
    - **CRITICAL**: Always include a section called "Modern Scientific Parallel" or "Decoding for the Modern World".
    - Explain how the Vedic concept aligns with modern physics, quantum mechanics, cosmology, or psychology (where applicable).
    - If the connection is metaphorical, state it clearly.
    - Be spiritual, respectful, yet scientific and logical.
    - Decode the ancient wisdom into modern, practical terms.
    - If the context doesn't fully answer it, use your general knowledge but mention that this specific detail wasn't in the retrieved verses.
    - Cite the Vedas (e.g., 'From RigVeda...') when possible.
    """
    
    # 3. Call Groq
    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            # model="llama3-70b-8192", # Decommissioned
            model="llama-3.3-70b-versatile",
        )
        answer = completion.choices[0].message.content
        return {"response": answer, "sources": sources_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
