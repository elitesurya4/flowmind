from memory.memory import FlowMindShortTermMemory
from rag.retriever import FlowMindRetriever
from rag.vectorstore import FlowMindVectorStore
from langchain_openai import ChatOpenAI
from agent.models import AgentState, ValidationPlan
import re

llm = ChatOpenAI(model="gpt-4.1", temperature=0)
memory = FlowMindShortTermMemory()
        
def memory_node(state: AgentState):
    state.chat_history = memory.recall(state.session_id)
    return state

def rag_node(state: AgentState):
    vectorstore = FlowMindVectorStore()
    retriever = FlowMindRetriever(vectorstore)
    state.retrieved_context = retriever.retrieve(state.user_query)
    return state

def planner_node(state: AgentState):
    prompt = f"""
Conversation:
{state.chat_history}

Use ONLY the provided context to generate the output. Do not add extra steps or information. Format the output as JSON with the following fields: step_name, description, procedure, expected_result, type.
Context: {state.retrieved_context}

Request: {state.user_query}

Generate CSV validation steps.
"""
    state.plan = llm.with_structured_output(ValidationPlan).invoke(prompt)
    return state

def confidence_node(state):
    response = llm.invoke(
        f"Give confidence score 0-1 for:\n{state.plan.json()}"
    ).content
    # Extract the first float between 0 and 1 (e.g., 0.95, 1.0)
    match = re.search(r"\b0\.\d+\b|\b1\.0\b", response)
    if match:
        state.confidence = float(match.group())
    else:
        state.confidence = 0.0  # fallback or handle as needed
    return state

def store_node(state: AgentState):
    memory.store(state.session_id, state.user_query, state.plan.json())
    return state