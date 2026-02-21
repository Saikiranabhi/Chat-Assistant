# FROM python:3.10-slim

# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# # Copy and install requirements FIRST (cached layer)
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Pre-download the embedding model (cached in image)
# RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# # Copy app code LAST (only this layer rebuilds on code changes)
# COPY . .

# EXPOSE 8501

# CMD ["streamlit", "run", "app_modular.py", \
#      "--server.port=8501", \
#      "--server.address=0.0.0.0", \
#      "--server.headless=true"]
# ```


FROM python:3.10-slim

WORKDIR /app

# Install uv (fast resolver, replaces pip)
RUN pip install uv

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Use uv instead of pip
RUN uv pip install --system -r requirements.txt

# Pre-download embedding model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_modular.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]