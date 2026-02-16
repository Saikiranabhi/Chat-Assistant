# Main orchestrator
"""
Main Application File
Orchestrates all modules and handles user interactions
"""

import uuid
from io import BytesIO

# Import custom modules
import config
from database import initialize_pinecone, store_embeddings
from utils import extract_text_from_pdf, chunk_text
from retrieval import build_qa_chain, ask_question
from frontend import (
    display_header,
    display_pdf_uploader,
    display_question_input,
    display_answer,
    display_source_documents,
    display_sidebar_info,
    display_error,
    display_success,
    display_info,
    initialize_session_state,
    update_pdf_session,
    is_pdf_loaded,
    get_current_pdf_id,
    get_current_pdf_name,
    get_qa_chain,
    add_to_chat_history,
    display_chat_history,
    get_chat_history
)


def process_pdf_upload(uploaded_file):
    """
    Process uploaded PDF file
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        tuple: (pdf_id, pdf_name, qa_chain) or (None, None, None) on error
    """
    try:
        # Generate unique ID for this PDF
        pdf_id = str(uuid.uuid4())
        pdf_name = uploaded_file.name
        
        # Read file from memory
        pdf_bytes = uploaded_file.read()
        pdf_buffer = BytesIO(pdf_bytes)
        
        # Extract text
        display_info("📖 Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_buffer)
        
        if len(text.strip()) < 100:
            display_error("PDF appears to be empty or has no extractable text")
            return None, None, None
        
        # Chunk text
        display_info("✂️ Splitting text into chunks...")
        chunks = chunk_text(text)
        
        # Create embeddings and store in Pinecone
        display_info(f"🔍 Creating embeddings for {len(chunks)} chunks...")
        store_embeddings(chunks, pdf_id, pdf_name)
        
        # Build QA chain
        display_info("🤖 Initializing QA system...")
        qa_chain = build_qa_chain(pdf_id)
        
        return pdf_id, pdf_name, qa_chain
    
    except Exception as e:
        display_error(f"Error processing PDF: {str(e)}")
        return None, None, None


def handle_question(question: str):
    """
    Handle user question
    
    Args:
        question: User question text
    """
    try:
        qa_chain = get_qa_chain()
        
        if not qa_chain:
            display_error("Please upload a PDF first")
            return
        
        # Process question
        display_info("🔍 Searching for answer...")
        result = ask_question(qa_chain, question)
        
        # Display answer
        display_answer(result['answer'])
        
        # Display source documents
        if result.get('source_documents'):
            display_source_documents(result['source_documents'])
        
        # Add to chat history
        add_to_chat_history(question, result['answer'])
    
    except Exception as e:
        display_error(f"Error processing question: {str(e)}")


def main():
    """Main application function"""
    
    # Display header
    display_header()
    
    # Initialize session state
    initialize_session_state()
    
    # Check Pinecone connection
    try:
        initialize_pinecone()
        display_success("Connected to Pinecone")
    except Exception as e:
        display_error(f"Failed to connect to Pinecone: {str(e)}")
        display_info("Please check your PINECONE_API_KEY environment variable")
        return
    
    # Display sidebar
    display_sidebar_info(
        pdf_name=get_current_pdf_name(),
        pdf_id=get_current_pdf_id()
    )
    
    # PDF Upload Section
    uploaded_file = display_pdf_uploader()
    
    if uploaded_file is not None:
        # Process PDF
        pdf_id, pdf_name, qa_chain = process_pdf_upload(uploaded_file)
        
        if pdf_id and pdf_name and qa_chain:
            # Update session
            update_pdf_session(pdf_id, pdf_name, qa_chain)
            display_success(f"PDF '{pdf_name}' processed successfully!")
            display_info("You can now ask questions about the document below")
    
    # Question Section (only show if PDF is loaded)
    if is_pdf_loaded():
        question = display_question_input()
        
        if question:
            handle_question(question)
        
        # Display chat history
        chat_history = get_chat_history()
        if chat_history:
            display_chat_history(chat_history)
    else:
        display_info("👆 Please upload a PDF document to get started")


if __name__ == "__main__":
    main()