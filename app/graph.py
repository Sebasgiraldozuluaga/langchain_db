# app/graph.py
from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.nodes import agent_node

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.set_entry_point("agent")
    graph.add_edge("agent", END)

    return graph.compile()
