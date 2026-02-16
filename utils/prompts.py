# Prompt templates
"""
Prompts Module
Contains prompt templates for QA system
"""

# from langchain.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate


def get_qa_prompt_template() -> PromptTemplate:
    """
    Get the QA prompt template for document-based question answering
    
    Returns:
        PromptTemplate: Configured prompt template
    """
    
    template = """You are a helpful AI assistant analyzing a document. Use the following context from the document to answer the question accurately and concisely.

Context from document:
{context}

Question: {question}

Instructions:
- Answer ONLY based on the provided context above
- If the answer is not found in the context, clearly state "I cannot find this information in the provided document"
- Be specific and cite relevant parts of the context when appropriate
- Keep your answer clear, concise, and factual
- Do not make up information or use external knowledge

Answer:"""

    return PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )


def get_system_prompt() -> str:
    """
    Get system-level instructions for the LLM
    
    Returns:
        str: System prompt
    """
    return """You are a precise document analysis assistant. Your role is to:
1. Only use information from the provided context
2. Be accurate and cite sources when possible
3. Admit when information is not available
4. Provide clear, well-structured answers"""