"""
config.py
Configuration, AWS Cloud Credentials, and Environment Management.
Supports Amazon OpenSearch Serverless, AWS RDS pgvector, Pinecone AWS, and Local Simulation.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Attempt loading .env
load_dotenv(BASE_DIR / ".env")

class EnterpriseCloudConfig:
    """Centralized enterprise configuration manager."""
    # AWS Credentials & Region
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN", None)

    # Cloud Vector Database Provider
    # Options: "aws_opensearch", "aws_pgvector", "pinecone_aws", "auto"
    VECTOR_STORE_PROVIDER = os.getenv("CLOUD_VECTOR_STORE_PROVIDER", "auto").lower()

    # Amazon OpenSearch Serverless
    AOSS_ENDPOINT = os.getenv("AOSS_ENDPOINT", "")
    AOSS_INDEX_NAME = os.getenv("AOSS_INDEX_NAME", "aurabio-abx702-colpali")

    # AWS RDS PostgreSQL + pgvector
    PGVECTOR_CONNECTION_STRING = os.getenv("PGVECTOR_CONNECTION_STRING", "")

    # Pinecone Serverless (AWS us-east-1)
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "aurabio-clinical-rag")

    # Foundation Models & Inference
    AWS_BEDROCK_MODEL_ID = os.getenv("AWS_BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # ColPali Architecture
    COLPALI_MODEL_NAME = os.getenv("COLPALI_MODEL_NAME", "vidore/colpali-v1.2")
    COLPALI_DIMENSION = 128
    COLPALI_DEVICE = os.getenv("COLPALI_DEVICE", "cuda" if os.getenv("USE_CUDA", "0") == "1" else "cpu")

    # Audit & Quality Thresholds
    MIN_CITATION_CONFIDENCE = 0.85
    MAX_STOPPING_RULE_GRADE4_THRESHOLD = 0.15 # 15% Grade 4 toxicity triggers clinical hold
