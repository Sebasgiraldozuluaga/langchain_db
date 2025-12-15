# app/state.py
from typing import TypedDict, List

class AgentState(TypedDict):
    input: str
    output: str
    history: List[str]
    
