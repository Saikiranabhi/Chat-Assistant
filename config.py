"""
Configuration file for RAG Chatbot
Contains all environment variables and constants
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================== PINECONE CONFIGURATION ====================
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
INDEX_NAME = "chat-assistant"
PINECONE_CLOUD = "aws"

# ==================== EMBEDDING CONFIGURATION ====================
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# ==================== TEXT PROCESSING CONFIGURATION ====================
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ==================== RETRIEVAL CONFIGURATION ====================
TOP_K_RESULTS = 5
SIMILARITY_METRIC = "cosine"

# ==================== LLM CONFIGURATION ====================
LLM_MODEL = "llama3:instruct"
LLM_TEMPERATURE = 0.2

# ==================== VALIDATION ====================
def validate_config():
    """Validate that all required configurations are set"""
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY environment variable is not set")
    return True


EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"  # 1024 dimensions
EMBEDDING_DIMENSION = 1024