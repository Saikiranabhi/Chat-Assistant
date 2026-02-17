from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Delete the existing index
try:
    pc.delete_index("chat-assistant")
    print("✅ Index 'chat-assistant' deleted!")
except Exception as e:
    print(f"Error: {e}")

# List remaining indexes
print("Remaining indexes:", pc.list_indexes().names())