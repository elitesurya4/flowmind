from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from config import FlowmindConfig
from typing import List
from uuid import uuid4
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

class FlowMindVectorStore:
    def __init__(self):
        self.client = QdrantClient(
            url=FlowmindConfig.QDRANT_BASE_URL,
            api_key=FlowmindConfig.QDRANT_API_KEY       
        )

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=FlowmindConfig.OPENAI_API_KEY
        )

    def similarity_search(self, query: str, k: int = 5) -> List:
        """
        Perform a similarity search in Qdrant for the given query.
        """
        query_vector = self.embeddings.embed_query(query)
        search_result = self.client.search(
            collection_name=FlowmindConfig.QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=k
        )
        # Assuming each result has a 'payload' with 'page_content'
        return [
            type("Doc", (), {"page_content": str(hit.payload)})()
            for hit in search_result
        ]
        
    @staticmethod 
    def insert_validation_step(
        qdrant_client: QdrantClient,
        openai_client: OpenAIEmbeddings,
        collection_name: str,
        steps_data: List[dict]
    ):
        """
        Embed and insert validation steps into Qdrant.
        """
        # Generate embedding
        points = []
        for step_data in steps_data:
            vector = openai_client.embed_query(step_data["embedding_text"])
            payload = {
                "step_name": step_data["step_name"],
                "description": step_data["description"],
                "procedure": step_data["procedure"],
                "expected_result": step_data["expected_result"],
                "embedding_text": step_data["embedding_text"],
                "type": "validation_step"
            }
            point = PointStruct(
                id=str(uuid4()),
                vector=vector,
                payload=payload
            )
            points.append(point)
        qdrant_client.upsert(
            collection_name=collection_name,
            points=points
        )
