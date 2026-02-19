import os
import glob
from typing import List
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
import config

# Initialize Clients
openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
pc = Pinecone(api_key=config.PINECONE_API_KEY)

def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """Split text into chunks of approximately chunk_size words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def get_embedding(text: str) -> List[float]:
    """Generate embedding for a given text using OpenAI."""
    response = openai_client.embeddings.create(
        input=text,
        model=config.EMBEDDING_MODEL
    )
    return response.data[0].embedding

def ingest_data():
    """Main ingestion function."""
    print("Starting ingestion process...")
    
    # Check if index exists, create if not
    existing_indexes = [index.name for index in pc.list_indexes()]
    if config.PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Creating Pinecone index: {config.PINECONE_INDEX_NAME}")
        pc.create_index(
            name=config.PINECONE_INDEX_NAME,
            dimension=1536, # Dimension for text-embedding-3-small
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    
    index = pc.Index(config.PINECONE_INDEX_NAME)
    
    # Load and process files
    data_path = os.path.join(os.path.dirname(__file__), "data", "*.txt")
    files = glob.glob(data_path)
    
    if not files:
        print("No text files found in data/ folder!")
        return

    vectors = []
    
    for file_path in files:
        filename = os.path.basename(file_path)
        print(f"Processing {filename}...")
        
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            
        chunks = chunk_text(text)
        
        for i, chunk in enumerate(chunks):
            file_id = f"{filename}_chunk_{i}"
            embedding = get_embedding(chunk)
            
            # Upsert format: (id, values, metadata)
            vectors.append({
                "id": file_id,
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "source": filename
                }
            })
            
    # Batch upsert to Pinecone
    if vectors:
        print(f"Upserting {len(vectors)} content chunks to Pinecone...")
        # Upsert in batches of 100 to be safe
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            index.upsert(vectors=batch)
            
    print("Ingestion complete!")

if __name__ == "__main__":
    ingest_data()
