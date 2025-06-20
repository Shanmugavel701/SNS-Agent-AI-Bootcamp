from langgraph.graph import StateGraph, END
from langchain.agents import AgentExecutor

# Example dummy agent
def dummy_agent(state):
    print("Agent invoked")
    return {"output": "Agent processed the input"}

# Define graph
graph = StateGraph()
graph.add_node("agent", dummy_agent)
graph.set_entry_point("agent")
graph.set_finish_point(END)
graph = graph.compile()
