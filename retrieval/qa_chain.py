# Question answering
"""
QA Chain Module
Handles question answering chain construction and execution
"""

# from langchain.chains import RetrievalQA
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.llms import Ollama

try:
    from langchain.chains import RetrievalQA
except ImportError:
    from langchain_community.chains import RetrievalQA
    
from typing import Dict, Any
import config
from utils.prompts import get_qa_prompt_template
from retrieval.retriever import create_retriever


def build_qa_chain(pdf_id: str) -> RetrievalQA:
    """
    Build a question answering chain for a specific PDF
    
    Args:
        pdf_id: PDF identifier
        
    Returns:
        RetrievalQA: Configured QA chain
    """
    try:
        # Create retriever for this PDF
        retriever = create_retriever(pdf_id)
        
        # Initialize LLM
        llm = Ollama(
            model=config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE
        )
        
        # Get custom prompt template
        prompt = get_qa_prompt_template()
        
        # Build QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",  # Stuff all retrieved docs into context
            retriever=retriever,
            return_source_documents=True,  # Return source chunks for transparency
            chain_type_kwargs={
                "prompt": prompt
            }
        )
        
        return qa_chain
    
    except Exception as e:
        raise Exception(f"Error building QA chain: {str(e)}")


def ask_question(qa_chain: RetrievalQA, question: str) -> Dict[str, Any]:
    """
    Ask a question using the QA chain
    
    Args:
        qa_chain: Configured QA chain
        question: User question
        
    Returns:
        Dict with 'answer', 'source_documents', and 'metadata'
    """
    try:
        # Invoke the QA chain
        response = qa_chain.invoke({"query": question})
        
        # Format response
        result = {
            "answer": response.get("result", ""),
            "source_documents": response.get("source_documents", []),
            "query": question
        }
        
        # Extract metadata from source documents
        if result["source_documents"]:
            result["metadata"] = [
                doc.metadata for doc in result["source_documents"]
            ]
        else:
            result["metadata"] = []
        
        return result
    
    except Exception as e:
        raise Exception(f"Error processing question: {str(e)}")


def format_source_documents(source_docs: list) -> str:
    """
    Format source documents for display
    
    Args:
        source_docs: List of source documents
        
    Returns:
        str: Formatted string representation
    """
    formatted = []
    
    for i, doc in enumerate(source_docs, 1):
        chunk_info = f"\n--- Chunk {i} ---\n"
        chunk_info += f"Content: {doc.page_content[:200]}...\n"
        chunk_info += f"Metadata: {doc.metadata}\n"
        formatted.append(chunk_info)
    
    return "\n".join(formatted)