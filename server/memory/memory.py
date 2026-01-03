"""_summary_
1. Embed and Store Memory Data
2. For embedings use OpenAI's text-embedding-3-small
3. Store embeddings in a vector database using Qdrant
4. Use the qdrant-client library to interact with Qdrant
"""



import redis, json
from agent.models import ChatTurn
from uuid import uuid4
from typing import List
from rag.vectorstore import FlowMindVectorStore
from config.config import FlowmindConfig

class FlowMindLongTermMemory:
    def __init__(self):
        self.vs = FlowMindVectorStore().vectorstore

    def store_conversation(self, session_id: str, user: str, assistant: str):
        """
        Store a conversation turn in long-term memory.
        """
        text = f"""
SESSION: {session_id}

USER:
{user}

ASSISTANT:
{assistant}
"""
        self.vs.add_texts(
            texts=[text],
            metadatas=[
                {
                    "session_id": session_id,
                    "memory_id": str(uuid4()),
                    "type": "conversation"
                }
            ]
        )

    def recall_similar(self, query: str, k: int = 4) -> str:
        """
        Recall similar memories using semantic search.
        """
        docs = self.vs.similarity_search(query, k=k)
        return "\n\n".join(doc.page_content for doc in docs)

    def recall_with_metadata(self, query: str, k: int = 4):
        """
        Recall similar memories with metadata.
        """
        docs = self.vs.similarity_search(query, k=k)
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in docs
        ]

    def recall_by_session(self, session_id: str, k: int = 10) -> str:
        """
        Recall memories for a specific session.
        """
        docs = self.vs.similarity_search(
            query=session_id,
            k=k,
            filter={"session_id": session_id}
        )
        return "\n\n".join(doc.page_content for doc in docs)

    def clear_all(self):
        """
        Delete all stored memories.
        """
        self.vs.client.delete_collection(
            collection_name=self.vs.collection_name
        )








class FlowMindShortTermMemory:
    def __init__(self):
        self.r = redis.Redis(host=FlowmindConfig.REDIS_HOST, port=FlowmindConfig.REDIS_PORT, password=FlowmindConfig.REDIS_PASSWORD, decode_responses=True)
    
    def recall(self, session_id):
        data = self.r.lrange(session_id, 0, 10)
        return [ChatTurn(**json.loads(x)) for x in data]

    def store(self, session_id, user, assistant):
        self.r.lpush(session_id, json.dumps({"role":"user","content":user}))
        self.r.lpush(session_id, json.dumps({"role":"assistant","content":assistant}))