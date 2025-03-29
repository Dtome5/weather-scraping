FROM python:3.12-alpine

# Set up environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apk add --no-cache \
    build-base \
    curl \
    git \
    rust \
    cargo \
    libffi-dev \
    openssl-dev \
    hdf5-dev \
    cmake \
    uv


# Create and set working directory
WORKDIR /app

# Copy requirements file
COPY ./requirements.txt .

# Install dependencies using UV
RUN uv pip install -r requirements.txt

# Copy script files
COPY extract.py .
COPY websites.csv .

# Create a volume for persistent storage
VOLUME /app/data

# Command to run the script
CMD ["python", "extract.py"]
