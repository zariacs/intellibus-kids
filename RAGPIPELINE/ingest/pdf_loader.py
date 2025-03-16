import os
import pdfplumber
import openai
import supabase
import tiktoken
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Supabase client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to generate embeddings using OpenAI
def generate_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]

# Function to process PDFs and store in Supabase
def ingest_pdfs(directory="books/"):
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(directory, file)
            print(f"📘 Processing {file}...")
            
            text = extract_text_from_pdf(pdf_path)
            embedding = generate_embedding(text)

            # Insert into Supabase
            supabase_client.table("documents").insert({
                "content": text,
                "metadata": {"filename": file},
                "embedding": embedding
            }).execute()

            print(f"✅ {file} stored in Supabase")

if __name__ == "__main__":
    ingest_pdfs()
