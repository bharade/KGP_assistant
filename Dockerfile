FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for chromadb & scientific libs
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    libsqlite3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project files
COPY app/ ./app
COPY app/vectorized_db/ ./vectorized_db
COPY vectorized_db/ ./vectorized_db
COPY app/vectorstore/ ./vectorstore


# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
