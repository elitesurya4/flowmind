from dotenv import load_dotenv
import os

load_dotenv()

class FlowmindConfig:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_BASE_URL = os.getenv("QDRANT_BASE_URL")
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")