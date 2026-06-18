RAG-based Document Q&A System

This project is a Retrieval-Augmented Generation (RAG) based Document Question Answering System built using FastAPI, Streamlit, FAISS, Sentence Transformers, and Ollama.
The application allows a user to upload a PDF document, generate embeddings, store them in a FAISS vector database, and ask questions that are answered only using the uploaded document.

Technologies Used:
* Python
* FastAPI
* Streamlit
* FAISS
* Sentence Transformers
* Ollama
* SQLite
* Pydantic
* NumPy
* PyPDF

Project Structure:
VeStaff/
│
├── backend/
│   ├── data/
│   ├── database/
│   ├── rag/
│   ├── routers/
│   ├── services/
│   ├── vectorstore/
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   └── schemas.py
│
├── frontend/
│   └── app.py
│
├── tests/
│
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore

Setup:
1. Clone the repository.
git clone <repository_url>
cd VeStaff

2. Create a virtual environment.
Windows
python -m venv venv
venv\Scripts\activate

Linux / macOS
python3 -m venv venv
source venv/bin/activate

3. Install the required packages.
pip install -r requirements.txt

4. Install Ollama.
Download and install Ollama from:
https://ollama.com

5. Pull the language model.
ollama pull qwen2.5:1.5b

6. Copy the environment file.
copy .env.example .env
The default configuration uses:
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5:1.5b
OLLAMA_URL=http://localhost:11434/api/generate

Running the Application:
1. Start Ollama.
ollama serve

2. Start the FastAPI backend.
uvicorn backend.main:app --reload (or uvicorn backend.main:app)
The backend will run at:
http://localhost:8000

3. Start the Streamlit frontend.
Open another terminal.
streamlit run frontend/app.py
The frontend will open at:
http://localhost:8501

How to Use:
1. Open the Streamlit application.
2. Upload a PDF document.
3. Click *Ingest*.
4. Wait until the ingestion process completes successfully.
5. Enter a question related to the uploaded document.
6. View the generated answer along with the retrieved source chunks.
7. Open the Analytics tab to view query statistics.

Pipeline:
Document Upload
↓
PDF Text Extraction
↓
Text Chunking
↓
Embedding Generation
↓
FAISS Index Creation
↓
Question Embedding
↓
Similarity Search
↓
Context Retrieval
↓
Answer Generation using Ollama
↓
Response with Source Chunks

Features:
* PDF document ingestion
* Automatic text chunking
* Sentence Transformer embeddings
* FAISS vector search
* Local LLM inference using Ollama
* Source attribution for every answer
* Analytics dashboard
* SQLite query logging
* FastAPI backend
* Streamlit frontend

API Endpoints:
Health Check
GET /health

Upload Document
POST /ingest

Ask Question
POST /ask

Analytics
GET /analytics

Notes:
* The backend must be running before starting the frontend.
* Ollama must be running before asking questions.
* A document must be ingested before any questions can be answered.
* The FAISS index and metadata are generated after a successful ingestion.
* The application answers only from the uploaded document and does not use external knowledge.