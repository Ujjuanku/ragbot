# 🤖 Acme Tech RAG Chatbot - Backend API

The backend API for the Acme Tech RAG Chatbot, built with FastAPI, Pinecone, and OpenAI. This service handles document ingestion, vector retrieval, and answer generation.

![Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20Pinecone%20%7C%20OpenAI-blue)

## 🎯 Objective
Provide a robust API endpoint (`/api/chat`) that:
1.  Receives user queries.
2.  Converts queries to embeddings.
3.  Searches Pinecone for relevant company context (History, Products, HR Policy).
4.  Generates an AI response using the retrieved context.

## 📂 Project Structure
```bash
backend/
├── data/               # Source text files (Knowledge Base)
├── main.py             # FastAPI application entry point
├── rag.py              # Core RAG logic & Pinecone integration
├── ingest.py           # Script to chunk & upload data to Vector DB
├── config.py           # Configuration & Environment variables
├── debug_rag.py        # Helper script to test RAG logic locally
└── requirements.txt    # Python dependencies
```

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- OpenAI API Key
- Pinecone API Key & Index Name

### 1. Installation
Clone the repository and navigate to the folder:
```bash
git clone https://github.com/Ujjuanku/ragbot.git
cd ragbot
```

Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=acme-rag
```

### 3. Data Ingestion
Run the ingestion script to populate your Pinecone vector database (only needs to be run once):
```bash
python ingest.py
```

### 4. Running the Server
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

## 📡 API Endpoints

### `POST /api/chat`
**Description**: Interact with the RAG chatbot.

**Request Body**:
```json
{
  "message": "What is the leave policy?"
}
```

**Response**:
```json
{
  "response": "The leave policy includes..."
}
```

### `GET /`
**Description**: Health check endpoint.

## 🛠 Tech Stack
- **Framework**: FastAPI
- **Vector Database**: Pinecone
- **LLM**: OpenAI GPT-3.5 Turbo
- **Embeddings**: OpenAI text-embedding-3-small
