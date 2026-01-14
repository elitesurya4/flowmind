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
You are a Veeva Vault Computer System Validation compliance retriever.

You MUST NOT generate, rewrite, summarize, abstract, or infer any steps.

You MUST return ONLY the validation steps that already exist in the provided Context.

STRICT COMPLIANCE RULES:
- Copy the stored "procedure" EXACTLY.
- Copy the stored "expected_result" EXACTLY.
- Always Include Login and Logout steps in the output if they exist in the context.
- Do NOT modify punctuation, wording, grammar, tense, or capitalization.
- Do NOT remove or add UI actions.
- Do NOT create new steps.
- Do NOT merge or split steps.
- Do NOT reorder steps.
- Do NOT omit any step provided in Context.

OUTPUT FORMAT:
Return ONLY a valid JSON array.
Each object must contain:

- step_no            → value from step_order
- action             → EXACT value from procedure
- expected_result    → EXACT value from expected_result
- category           → Map "type":
        validation_step → "Validation"
        setup_step      → "Setup"
        action_step     → "Action"
        teardown_step   → "Teardown"

Context:
{state.retrieved_context}

Request:
{state.user_query}

Return compliance validation steps.
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