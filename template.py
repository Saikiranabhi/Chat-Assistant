import os

# -----------------------------
# Project Structure Definition
# -----------------------------

project_structure = {
    "config.py": "# All configurations\n",
    "app_modular.py": "# Main orchestrator\n",
    "utils": {
        "__init__.py": "",
        "pdf_processor.py": "# PDF → Text → Chunks\n",
        "embeddings.py": "# Text → Vectors\n",
        "prompts.py": "# Prompt templates\n",
    },
    "database": {
        "__init__.py": "",
        "pinecone_manager.py": "# Pinecone setup\n",
        "vector_store.py": "# Store/search vectors\n",
    },
    "retrieval": {
        "__init__.py": "",
        "retriever.py": "# Document retrieval\n",
        "qa_chain.py": "# Question answering\n",
    },
    "frontend": {
        "__init__.py": "",
        "ui_components.py": "# Display components\n",
        "session_manager.py": "# State management\n",
    }
}


# -----------------------------
# Directory Creation Logic
# -----------------------------

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            # Create directory
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # Create file with boilerplate content
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


# -----------------------------
# Run Script
# -----------------------------

if __name__ == "__main__":
    project_name = "rag_modular_project"  # Change if needed
    os.makedirs(project_name, exist_ok=True)
    create_structure(project_name, project_structure)

    print(f"\n✅ Project '{project_name}' structure created successfully!")
