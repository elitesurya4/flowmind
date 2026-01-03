from fastapi import FastAPI
from agent.agent import flowmind_agent
from agent.models import AgentState

app = FastAPI()

@app.post("/chat")
def chat(state: AgentState):
    return flowmind_agent.invoke(state)