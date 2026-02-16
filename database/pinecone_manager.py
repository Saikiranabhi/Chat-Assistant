# Pinecone setup
"""
Pinecone Manager Module
Handles Pinecone client initialization and index management
"""

from pinecone import Pinecone, ServerlessSpec
import config


_pinecone_client = None  # Singleton pattern


def initialize_pinecone() -> Pinecone:
    """
    Initialize Pinecone client and create index if needed
    
    Returns:
        Pinecone: Initialized Pinecone client
    """
    global _pinecone_client
    
    if _pinecone_client is None:
        try:
            # Validate configuration
            config.validate_config()
            
            # Initialize Pinecone
            _pinecone_client = Pinecone(api_key=config.PINECONE_API_KEY)
            
            # Check if index exists
            existing_indexes = _pinecone_client.list_indexes().names()
            
            if config.INDEX_NAME not in existing_indexes:
                # Create new index
                _pinecone_client.create_index(
                    name=config.INDEX_NAME,
                    dimension=config.EMBEDDING_DIMENSION,
                    metric=config.SIMILARITY_METRIC,
                    spec=ServerlessSpec(
                        cloud=config.PINECONE_CLOUD,
                        region=config.PINECONE_ENVIRONMENT
                    )
                )
                print(f"Created new Pinecone index: {config.INDEX_NAME}")
            else:
                print(f"Using existing Pinecone index: {config.INDEX_NAME}")
        
        except Exception as e:
            raise Exception(f"Failed to initialize Pinecone: {str(e)}")
    
    return _pinecone_client


def get_pinecone_client() -> Pinecone:
    """
    Get the initialized Pinecone client
    
    Returns:
        Pinecone: Pinecone client instance
    """
    if _pinecone_client is None:
        return initialize_pinecone()
    return _pinecone_client


def get_index():
    """
    Get the Pinecone index object
    
    Returns:
        Index: Pinecone index instance
    """
    client = get_pinecone_client()
    return client.Index(config.INDEX_NAME)


def delete_namespace(pdf_id: str):
    """
    Delete all vectors in a namespace (useful for cleanup)
    
    Args:
        pdf_id: PDF ID (namespace) to delete
    """
    try:
        index = get_index()
        index.delete(namespace=pdf_id, delete_all=True)
        print(f"Deleted namespace: {pdf_id}")
    
    except Exception as e:
        raise Exception(f"Error deleting namespace: {str(e)}")