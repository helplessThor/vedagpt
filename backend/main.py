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

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: list[Message] = []

@app.get("/")
def read_root():
    return {"status": "VedaGPT API is running"}

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    query = req.message
    history = req.history
    print(f"Received Query: {query}")
    
    # 1. Retrieve Context from Vedas based on CURRENT query
    # (Future improvement: Summarize history + query for better retrieval)
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
    
    CONTEXT FROM VEDAS (Relevant to the user's latest question):
    {context_str}
    
    INSTRUCTIONS:
    - **PRIMARY SOURCE**: Use the 'CONTEXT FROM VEDAS' provided above as your primary source of truth.
    - **FALLBACK**: Only if the provided context does NOT contain the answer, use your general knowledge.
    - **DISCLAIMER**: If you are answering from general knowledge because the context was insufficient, you MUST start your response with: *"The specific verses for this were not found in the current context, but based on general Vedic knowledge..."*
    - Answer the user's question using the context provided above and the conversation history.
    - **CONCISENESS**: Answer the user's question directly and concisely. Do not elaborate unnecessarily.
    - **DETAIL**: Only provide detailed, long, or expansive responses if the user explicitly asks for "details", "elaboration", "explanation", "more info", etc.
    - **CRITICAL**: FOR METAPHYSICAL & PHYSICAL QUESTIONS (e.g. Creation, Cosmology, Time, Atoms, Energy, Consciousness etc): YOU MUST include a section called "Modern Scientific Parallel" in brief explaining how the Vedic concept aligns with modern physics/science.
    - **CRITICAL**: FOR PURELY RELIGIOUS & RITUALISTIC QUESTIONS (e.g. Worship, Deities, Mantras, Ethics, Duties etc): Do NOT include scientific parallels. Keep the answer strictly rooted in the spiritual and philosophical wisdom of the Vedas.
    - If the connection is metaphorical, state it clearly.
    - Be spiritual, respectful, yet scientific and logical where appropriate.
    - Decode the ancient wisdom into modern, practical terms if the relevant to the question.
    - Cite the Vedas (e.g., 'From RigVeda...') when possible.
    """
    
    # 3. Build Message Chain for Groq
    messages = [{"role": "system", "content": system_prompt}]
    
    # Append history (limited to last 10 turns to save tokens/complexity if needed, but sending all for now)
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})
        
    # Append current user query
    messages.append({"role": "user", "content": query})

    # 4. Call Groq
    try:
        completion = groq_client.chat.completions.create(
            messages=messages,
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
