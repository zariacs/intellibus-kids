import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
RAG_API_URL = os.getenv("RAG_API_URL", "http://rag-pipeline:8005/search")  # Use service name inside Docker

def get_rag_context(query, top_k=5):
    """Send query to RAG API and retrieve contextual documents."""
    response = requests.get(RAG_API_URL, params={"query": query, "top_k": top_k})
    data = response.json()
    
    if "results" in data:
        context = "\n".join([doc["content"][:500] for doc in data["results"]])  # Limit length
        return context
    return "No relevant context found."

def generate_answer(query):
    """Generate an AI response with retrieved context."""
    context = get_rag_context(query)
    
    if context:
        prompt = f"Using the following research context, answer the query:\n\n{context}\n\nQuery: {query}"
    else:
        prompt = query  # Fallback to original query

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI researcher."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    user_query = input("Ask a question: ")
    print(generate_answer(user_query))
