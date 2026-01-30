# VedaGPT Zero-Cost Deployment Guide

Here is how to deploy VedaGPT for free so your friends can use it.

## 1. Backend (Render.com) - The Brain
This will host the Python API and the AI Logic.

1.  Create an account on [Render.com](https://render.com/).
2.  Click **"New +"** -> **"Web Service"**.
3.  Connect your GitHub repository (`helplessThor/VedaGPT`).
4.  Configure the settings:
    *   **Name**: `vedagpt-backend`
    *   **Root Directory**: `backend`
    *   **Environment**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt && python ingest.py`
        *   *(This installs dependencies and downloads/builds the Veda database)*
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
5.  **Environment Variables** (Scroll down):
    *   Key: `GROQ_API_KEY`
    *   Value: `your_groq_api_key_paste_here`
    *   *(Also add `PYTHON_VERSION`: `3.11.0` if prompted, but usually auto-detected)*
6.  Click **"Create Web Service"**.
    *   *Wait about 5-10 minutes. The logs will show the Vedas being downloaded. Once it says "Ingestion Complete" and "Uvicorn running", copy the URL (e.g., `https://vedagpt-backend.onrender.com`).*

## 2. Frontend (Vercel) - The Interface
This will host the React website.

1.  Create an account on [Vercel.com](https://vercel.com/).
2.  Click **"Add New..."** -> **"Project"**.
3.  Import your `VedaGPT` repository.
4.  Configure the settings:
    *   **Framework Preset**: `Vite` (Should auto-detect).
    *   **Root Directory**: Click "Edit" and select `frontend`.
5.  **Environment Variables**:
    *   Key: `VITE_API_URL`
    *   Value: `https://vedagpt-backend.onrender.com` 
        *   *(Paste the exact URL from Step 1, NO trailing slash)*
6.  Click **"Deploy"**.

## 3. Share!
Once Vercel finishes, it will give you a link (e.g., `https://vedagpt.vercel.app`).
**Send this link to your friends!** 🕉️
