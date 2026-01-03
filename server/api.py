from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from agent.agent import flowmind_agent
from agent.models import AgentState
from rag.vectorstore import FlowMindVectorStore
from config.config import FlowmindConfig
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["/*", "http://localhost", "http://localhost:3000", "http://localhost:5173/", "flowmind-sigma.vercel.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ValidationStep(BaseModel):
    step_name: str
    description: str
    procedure: str
    expected_result: str
    embedding_text: str

@app.post("/chat")
def chat(state: AgentState):
    return flowmind_agent.invoke(state)

@app.post("/insert_validation_steps")
def insert_validation_steps(steps: List[ValidationStep]):
    vectorstore = FlowMindVectorStore()
    FlowMindVectorStore.insert_validation_step(
        qdrant_client=vectorstore.client,
        openai_client=vectorstore.embeddings,
        collection_name=FlowmindConfig.QDRANT_COLLECTION_NAME,
        steps_data=[step.model_dump() for step in steps]
    )
    return {"status": "success", "inserted": len(steps)}


@app.get("/health")
def health_check():
    return {"status": "Flowmind Backend server is running."}