import os
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from rag.vectorstore import FlowMindVectorStore

openai_client = OpenAIEmbeddings(model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_BASE_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

step_data = {
    "step_name": "Login to Vault",
    "description": "This step verifies that an authorized user can successfully log in to the Vault application using valid credentials.",
    "procedure": "Log into the Vault application using the <<AUTHORIZED_USER>> account by entering the correct username and password on the login screen.",
    "expected_result": "The user is successfully authenticated, and the Vault home page is displayed without any errors.",
    "embedding_text": "Login to Vault validation step. Procedure: Log into the Vault application using an authorized user account with valid credentials. Expected Result: User is successfully authenticated and the Vault home page is displayed."
}

FlowMindVectorStore.insert_validation_step(
    qdrant_client=qdrant_client,
    openai_client=openai_client,
    collection_name="flowmind_high_level_knowledge_base",
    step_data=step_data
)
