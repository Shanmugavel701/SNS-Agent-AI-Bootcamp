# backend/langgraph/workflow.py

from langgraph.graph import StateGraph
from backend.agents.logger_agent import logger_executor
from backend.agents.scorer_agent import scorer_executor
from backend.agents.quiz_agent import quiz_executor
from backend.agents.recommend_agent import recommend_executor
from backend.agents.mentor_summary_agent import mentor_executor

builder = StateGraph()
builder.add_node("Logger", logger_executor)
builder.add_node("Scorer", scorer_executor)
builder.add_node("Quiz", quiz_executor)
builder.add_node("Recommend", recommend_executor)
builder.add_node("MentorSummary", mentor_executor)

# Connect flow
builder.set_entry_point("Logger")
builder.add_edge("Logger", "Scorer")
builder.add_edge("Scorer", "Quiz")
builder.add_edge("Quiz", "Recommend")
builder.add_edge("Recommend", "MentorSummary")

graph = builder.compile()
