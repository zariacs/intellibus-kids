import requests
import time
import openai
import supabase
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Supabase client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

PUBMED_URL = "https://pubmed.ncbi.nlm.nih.gov/rss/search?q=AI+in+medicine&format=xml"

# Function to get latest articles
def fetch_articles():
    response = requests.get(PUBMED_URL)
    soup = BeautifulSoup(response.text, "xml")
    articles = soup.find_all("item")

    for article in articles:
        title = article.title.text
        link = article.link.text
        summary = article.description.text if article.description else "No summary available."
        
        print(f"📄 New Article: {title}")

        # Generate embeddings
        embedding = openai.Embedding.create(input=summary, model="text-embedding-ada-002")["data"][0]["embedding"]

        # Store in Supabase
        supabase_client.table("documents").insert({
            "content": summary,
            "metadata": {"title": title, "link": link},
            "embedding": embedding
        }).execute()

        print(f"✅ Stored article: {title}")

# Run every 6 hours
while True:
    fetch_articles()
    print("⏳ Waiting 6 hours before next check...")
    time.sleep(21600)  # 6 hours
