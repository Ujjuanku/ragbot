# Acme Tech RAG Chatbot

## Setup and Run

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ingest Data** (Only needs to be run once to populate the database)
   ```bash
   python ingest.py
   ```
   *Note: Ensure your .env file has valid API keys before running.*

3. **Start the API Server**
   ```bash
   uvicorn main:app --reload
   ```

4. **Test the Chatbot**
   Open a new terminal and send a test query:
   ```bash
   curl -X POST "http://127.0.0.1:8000/api/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "What is AcmeFlow?"}'
   ```

## Project Structure
- `data/`: Contains source documents (History, Products, HR Policy).
- `ingest.py`: Reads data, creates embeddings, and uploads to Pinecone.
- `rag.py`: Handling retrieval and GPT-3.5 response generation.
- `main.py`: FastAPI server definitions.
