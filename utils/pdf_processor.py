# PDF → Text → Chunks
"""
PDF Processing Module
Handles PDfromF text extraction and chunking
"""

from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
import config


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from PDF file
    
    Args:
        pdf_file: File object or path to PDF
        
    Returns:
        str: Extracted text from all pages
    """
    try:
        reader = PdfReader(pdf_file)
        text = ""
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        return text.strip()
    
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def chunk_text(text: str) -> List[str]:
    """
    Split text into chunks for embedding
    
    Args:
        text: Input text to chunk
        
    Returns:
        List[str]: List of text chunks
    """
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        chunks = splitter.split_text(text)
        return chunks
    
    except Exception as e:
        raise Exception(f"Error chunking text: {str(e)}")


def validate_pdf_content(text: str) -> bool:
    """
    Validate that PDF has extractable text
    
    Args:
        text: Extracted text
        
    Returns:
        bool: True if valid, False otherwise
    """
    return len(text.strip()) > 100  # At least 100 characters