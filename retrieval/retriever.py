# Document retrieval
"""
Retriever Module
Handles document retrieval logic
"""

# from langchain.schema.retriever import BaseRetriever
from langchain_core.retrievers import BaseRetriever
from database.vector_store import get_vector_store
import config


def create_retriever(pdf_id: str, top_k: int = None) -> BaseRetriever:
    """
    Create a retriever for a specific PDF
    
    Args:
        pdf_id: PDF identifier
        top_k: Number of chunks to retrieve (default from config)
        
    Returns:
        BaseRetriever: Configured retriever
    """
    try:
        if top_k is None:
            top_k = config.TOP_K_RESULTS
        
        # Get vector store for this PDF
        vector_store = get_vector_store(pdf_id)
        
        # Create retriever with search configuration
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": top_k,
                "filter": {"pdf_id": pdf_id}  # Ensure we only get this PDF's chunks
            }
        )
        
        return retriever
    
    except Exception as e:
        raise Exception(f"Error creating retriever: {str(e)}")


def get_relevant_context(query: str, pdf_id: str, top_k: int = None) -> list:
    """
    Get relevant context chunks for a query
    
    Args:
        query: User question
        pdf_id: PDF identifier
        top_k: Number of chunks to retrieve
        
    Returns:
        List of relevant documents
    """
    try:
        retriever = create_retriever(pdf_id, top_k)
        documents = retriever.get_relevant_documents(query)
        return documents
    
    except Exception as e:
        raise Exception(f"Error retrieving context: {str(e)}")