# Display components
"""
UI Components Module
Reusable Streamlit UI components
"""

import streamlit as st
from typing import Optional, List


def display_header():
    """Display the app header"""
    st.set_page_config(
        page_title="RAG Chatbot with Pinecone",
        page_icon="📄",
        layout="centered"
    )
    
    st.title("📄🧠 RAG Chatbot with Pinecone + LLaMA")
    st.markdown("""
    Upload a PDF document and ask questions based on its content.
    Powered by LangChain, Pinecone, and LLaMA.
    """)
    st.divider()


def display_pdf_uploader():
    """
    Display PDF file uploader
    
    Returns:
        Uploaded file object or None
    """
    st.subheader("📤 Upload Your Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload a PDF document to analyze"
    )
    return uploaded_file


def display_question_input() -> Optional[str]:
    """
    Display question input field
    
    Returns:
        User question or None
    """
    st.subheader("❓ Ask a Question")
    question = st.text_input(
        "Enter your question about the document:",
        placeholder="e.g., What is the main topic of this document?",
        key="question_input"
    )
    return question if question else None


def display_answer(answer: str):
    """
    Display the answer in a styled container
    
    Args:
        answer: Answer text to display
    """
    st.subheader("💬 Answer")
    st.success(answer)


def display_source_documents(source_docs: list):
    """
    Display source documents in an expander
    
    Args:
        source_docs: List of source document objects
    """
    if not source_docs:
        return
    
    with st.expander(f"📚 View Source Context ({len(source_docs)} chunks)", expanded=False):
        for i, doc in enumerate(source_docs, 1):
            st.markdown(f"**Chunk {i}**")
            
            # Display content
            st.text_area(
                "Content",
                doc.page_content,
                height=100,
                key=f"chunk_{i}",
                disabled=True
            )
            
            # Display metadata
            if hasattr(doc, 'metadata'):
                st.json(doc.metadata)
            
            if i < len(source_docs):
                st.divider()


def display_sidebar_info(pdf_name: Optional[str] = None, pdf_id: Optional[str] = None):
    """
    Display information in the sidebar
    
    Args:
        pdf_name: Current PDF name
        pdf_id: Current PDF ID
    """
    with st.sidebar:
        st.header("ℹ️ Information")
        
        if pdf_name and pdf_id:
            st.markdown("### 📄 Current Document")
            st.write(f"**Name:** {pdf_name}")
            st.write(f"**ID:** {pdf_id[:8]}...")
            st.divider()
        
        st.markdown("### 🔧 Configuration")
        st.write("**Model:** LLaMA 3 Instruct")
        st.write("**Embeddings:** MiniLM-L6-v2")
        st.write("**Vector DB:** Pinecone")
        st.divider()
        
        st.markdown("### 💡 Tips")
        st.info("""
        - Ask specific questions
        - Questions should be about document content
        - Check source chunks for verification
        """)


def display_processing_status(status: str):
    """
    Display a processing status message
    
    Args:
        status: Status message
    """
    with st.spinner(status):
        pass


def display_error(error_msg: str):
    """
    Display an error message
    
    Args:
        error_msg: Error message to display
    """
    st.error(f"❌ {error_msg}")


def display_success(success_msg: str):
    """
    Display a success message
    
    Args:
        success_msg: Success message to display
    """
    st.success(f"✅ {success_msg}")


def display_info(info_msg: str):
    """
    Display an info message
    
    Args:
        info_msg: Info message to display
    """
    st.info(f"💡 {info_msg}")


def display_warning(warning_msg: str):
    """
    Display a warning message
    
    Args:
        warning_msg: Warning message to display
    """
    st.warning(f"⚠️ {warning_msg}")


def display_chat_history(chat_history: List[dict]):
    """
    Display chat history
    
    Args:
        chat_history: List of Q&A dictionaries
    """
    if not chat_history:
        return
    
    st.subheader("💬 Chat History")
    
    for i, chat in enumerate(reversed(chat_history), 1):
        with st.expander(f"Q{len(chat_history) - i + 1}: {chat['question'][:50]}...", expanded=False):
            st.markdown("**Question:**")
            st.write(chat['question'])
            st.markdown("**Answer:**")
            st.write(chat['answer'])