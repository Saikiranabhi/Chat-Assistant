# Store/search vectors
"""
Vector Store Module
Handles storing and searching vectors in Pinecone
"""


from langchain_pinecone import PineconeVectorStore
from typing import List, Dict, Any
from datetime import datetime
import config
from utils.embeddings import get_embedding_model


def store_embeddings(
    texts: List[str],
    pdf_id: str,
    pdf_name: str
) -> PineconeVectorStore:
    """
    Store text chunks as embeddings in Pinecone with metadata
    
    Args:
        texts: List of text chunks
        pdf_id: Unique PDF identifier
        pdf_name: Name of the PDF file
        
    Returns:
        PineconeVectorStore: Vector store instance
    """
    try:
        # Get embedding model
        embeddings = get_embedding_model()
        
        # Prepare metadata for each chunk
        metadatas = [
            {
                "pdf_id": pdf_id,
                "pdf_name": pdf_name,
                "chunk_index": i,
                "upload_date": datetime.now().isoformat(),
                "total_chunks": len(texts),
                "chunk_length": len(text)
            }
            for i, text in enumerate(texts)
        ]
        
        # Create vector store and store embeddings
        vector_store = PineconeVectorStore.from_texts(
            texts=texts,
            embedding=embeddings,
            index_name=config.INDEX_NAME,
            metadatas=metadatas,
            namespace=pdf_id  # Isolate each PDF in its own namespace
        )
        
        print(f"Stored {len(texts)} chunks for PDF: {pdf_name} (ID: {pdf_id})")
        return vector_store
    
    except Exception as e:
        raise Exception(f"Error storing embeddings: {str(e)}")


def get_vector_store(pdf_id: str) -> PineconeVectorStore:
    """
    Get vector store instance for a specific PDF
    
    Args:
        pdf_id: PDF identifier
        
    Returns:
        PineconeVectorStore: Vector store for the PDF
    """
    try:
        embeddings = get_embedding_model()
        
        vector_store = PineconeVectorStore(
            index_name=config.INDEX_NAME,
            embedding=embeddings,
            namespace=pdf_id
        )
        
        return vector_store
    
    except Exception as e:
        raise Exception(f"Error getting vector store: {str(e)}")


def search_similar_chunks(
    query: str,
    pdf_id: str,
    top_k: int = None
) -> List[Dict[str, Any]]:
    """
    Search for similar chunks for a query
    
    Args:
        query: Query text
        pdf_id: PDF identifier to search within
        top_k: Number of results to return (default from config)
        
    Returns:
        List of dicts with 'content', 'metadata', and 'score'
    """
    try:
        if top_k is None:
            top_k = config.TOP_K_RESULTS
        
        vector_store = get_vector_store(pdf_id)
        
        # Search with metadata filter
        results = vector_store.similarity_search_with_score(
            query=query,
            k=top_k,
            filter={"pdf_id": pdf_id}
        )
        
        # Format results
        formatted_results = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            }
            for doc, score in results
        ]
        
        return formatted_results
    
    except Exception as e:
        raise Exception(f"Error searching chunks: {str(e)}")