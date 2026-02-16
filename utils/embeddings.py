# Text → Vectors
"""
Embeddings Module
Handles embedding model initialization and text-to-vector conversion
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List
import config


_embedding_model = None  # Singleton pattern for efficiency


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Get or initialize the embedding model (singleton)
    
    Returns:
        HuggingFaceEmbeddings: Initialized embedding model
    """
    global _embedding_model
    
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL_NAME,
            model_kwargs={'device': 'cpu'},  # Use 'cuda' if GPU available
            encode_kwargs={'normalize_embeddings': True}
        )
    
    return _embedding_model


def create_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Create embeddings for a list of texts
    
    Args:
        texts: List of text strings to embed
        
    Returns:
        List[List[float]]: List of embedding vectors
    """
    try:
        embedding_model = get_embedding_model()
        embeddings = embedding_model.embed_documents(texts)
        return embeddings
    
    except Exception as e:
        raise Exception(f"Error creating embeddings: {str(e)}")


def embed_query(query: str) -> List[float]:
    """
    Create embedding for a single query
    
    Args:
        query: Query text
        
    Returns:
        List[float]: Query embedding vector
    """
    try:
        embedding_model = get_embedding_model()
        query_embedding = embedding_model.embed_query(query)
        return query_embedding
    
    except Exception as e:
        raise Exception(f"Error embedding query: {str(e)}")