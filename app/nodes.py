# app/nodes.py
from app.main import agent
from app.state import AgentState

def agent_node(state: AgentState) -> AgentState:
    history_text = "\n".join(state.get("history", []))

    enriched_input = f"""
Historial de la conversación:
{history_text}

Usuario:
{state["input"]}
"""

    result = agent.invoke({"input": enriched_input})
    output = result["output"]

    return {
        "input": state["input"],
        "output": output,
        "history": state.get("history", []) + [
            state["input"],
            output
        ],
    }