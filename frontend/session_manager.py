# State management
"""
Session Manager Module
Handles Streamlit session state management
"""

import streamlit as st
from typing import Optional


def initialize_session_state():
    """Initialize all session state variables"""
    
    if 'pdf_id' not in st.session_state:
        st.session_state.pdf_id = None
    
    if 'pdf_name' not in st.session_state:
        st.session_state.pdf_name = None
    
    if 'qa_chain' not in st.session_state:
        st.session_state.qa_chain = None
    
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []


def update_pdf_session(pdf_id: str, pdf_name: str, qa_chain):
    """
    Update session state with new PDF information
    
    Args:
        pdf_id: Unique PDF identifier
        pdf_name: Name of the PDF file
        qa_chain: Configured QA chain
    """
    st.session_state.pdf_id = pdf_id
    st.session_state.pdf_name = pdf_name
    st.session_state.qa_chain = qa_chain
    st.session_state.chat_history = []  # Reset chat history for new PDF


def get_current_pdf_id() -> Optional[str]:
    """
    Get the current PDF ID from session
    
    Returns:
        str or None: Current PDF ID
    """
    return st.session_state.get('pdf_id', None)


def get_current_pdf_name() -> Optional[str]:
    """
    Get the current PDF name from session
    
    Returns:
        str or None: Current PDF name
    """
    return st.session_state.get('pdf_name', None)


def get_qa_chain():
    """
    Get the current QA chain from session
    
    Returns:
        QA chain or None
    """
    return st.session_state.get('qa_chain', None)


def is_pdf_loaded() -> bool:
    """
    Check if a PDF is currently loaded
    
    Returns:
        bool: True if PDF is loaded
    """
    return (
        st.session_state.get('pdf_id') is not None and
        st.session_state.get('qa_chain') is not None
    )


def add_to_chat_history(question: str, answer: str):
    """
    Add Q&A to chat history
    
    Args:
        question: User question
        answer: Bot answer
    """
    st.session_state.chat_history.append({
        'question': question,
        'answer': answer
    })


def get_chat_history() -> list:
    """
    Get chat history
    
    Returns:
        List of Q&A pairs
    """
    return st.session_state.get('chat_history', [])


def clear_session():
    """Clear all session state"""
    st.session_state.pdf_id = None
    st.session_state.pdf_name = None
    st.session_state.qa_chain = None
    st.session_state.chat_history = []
    st.session_state.processing = False