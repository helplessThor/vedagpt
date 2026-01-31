# VedaGPT

**VedaGPT** is an AI-powered spiritual assistant deeply rooted in the wisdom of the four Vedas (Rig, Sama, Yajur, and Atharva). It uses RAG (Retrieval-Augmented Generation) to provide answers strictly based on Vedic scripture, while bridging the gap between ancient wisdom and modern scientific concepts where applicable.

## 🌟 Features

*   **Dharmic UI**: A visually immersive "Cosmic" interface with deep indigo backgrounds (`Cosmic Void`), saffron (`Agni`) and gold (`Suvarna`) accents, and subtle breathing mandala animations.
*   **Context Aware**: Remembers the flow of conversation (multi-turn dialogue support).
*   **Scientific Parallels**: Automatically providing "Modern Scientific Parallels" for metaphysical questions (Cosmology, Atoms, Time), while keeping ritualistic answers strictly traditional.
*   **Source Citation**: Cites the specific verses or sources used to generate the answer.
*   **Strict RAG Prioritization**: Falls back to general knowledge only when specific verses are not found, with an explicit disclaimer.

## 🛠️ Tech Stack

*   **Backend**: Python, FastAPI, ChromaDB (Vector Store), Groq API (Llama 3 70b).
*   **Frontend**: React (Vite), Tailwind CSS, Framer Motion, Lucide React.
*   **Fonts**: *Cormorant Garamond* (Serif) & *Outfit* (Sans).

## 🚀 Setup Instructions

### Prerequisites
- Node.js & npm
- Python 3.10+
- A Groq API Key

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Activate venv (Windows: venv\Scripts\activate, Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
```
Create a `.env` file in `backend/` and add:
```env
GROQ_API_KEY=your_groq_api_key_here
```
Run the server:
```bash
uvicorn main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📜 License
MIT
