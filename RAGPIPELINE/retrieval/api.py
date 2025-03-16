import os
import openai
import supabase
from fastapi import FastAPI, Query
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Supabase client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPI app
app = FastAPI(title="RAG API", description="Retrieve context from vector database")

@app.get("/search")
def search_documents(query: str, top_k: int = 5):
    """Search Supabase vector DB for relevant documents."""
    
    # Generate query embedding
    query_embedding = openai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )["data"][0]["embedding"]

    # Search in Supabase using cosine similarity
    query_sql = """
    SELECT content, metadata,
    1 - (embedding <=> ARRAY_PARSE(%s)) AS similarity
    FROM documents
    ORDER BY similarity DESC
    LIMIT %s;
    """

    response = supabase_client.rpc("documents_search", params={"query_embedding": query_embedding, "limit": top_k}).execute()
    
    results = [
        {"content": doc["content"], "metadata": doc["metadata"], "similarity": doc["similarity"]}
        for doc in response.data
    ]

    return {"query": query, "results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
