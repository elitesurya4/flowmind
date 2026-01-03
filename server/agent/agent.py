from langgraph.graph import StateGraph, END
from agent.models import AgentState
from agent.nodes import *

g = StateGraph(AgentState)
g.add_node("memory", memory_node)
g.add_node("rag", rag_node)
g.add_node("planner", planner_node)
g.add_node("confidence", confidence_node)
g.add_node("store", store_node)

g.set_entry_point("memory")
g.add_edge("memory","rag")
g.add_edge("rag","planner")
g.add_edge("planner","confidence")
g.add_edge("confidence","store")
g.add_edge("store", END)

flowmind_agent = g.compile()