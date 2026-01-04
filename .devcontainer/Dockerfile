FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    gnupg \
    lsb-release \
    build-essential \
    ca-certificates \
    && curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
    && apt-get update && apt-get install -y git-lfs \
    && git lfs install --system \
    && rm -rf /var/lib/apt/lists/*

# Install Google Cloud SDK
RUN curl https://sdk.cloud.google.com | bash
ENV PATH=$PATH:/root/google-cloud-sdk/bin

# Install Node.js (for ADK DevTools if needed)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Install Python dependencies
RUN pip install --no-cache-dir \
    google-adk \
    agent-starter-pack \
    langgraph \
    langchain \
    langchain-google-genai \
    litellm \
    fastapi \
    uvicorn[standard] \
    httpx \
    pydantic \
    openai \
    streamlit \
    uv \
    google-cloud-trace \
    google-cloud-logging \
    google-cloud-bigquery \
    pytest \
    pytest-asyncio

# Install optional ADK DevTools (JavaScript/TypeScript support)
RUN npm install -g @google/adk @google/adk-devtools

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_CLOUD_PROJECT=""

# Create directories for agent development
RUN mkdir -p /workspace/agents /workspace/configs

CMD ["sleep", "infinity"]
