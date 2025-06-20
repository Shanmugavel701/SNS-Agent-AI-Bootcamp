# backend/agents/scorer_agent.py

# ======= Imports =======
from backend.db.mongodb import events_col
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.tools import tool
from dotenv import load_dotenv
import os

# ======= Load Env =======
load_dotenv()

# ======= LLM Init =======
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.4
)

# ======= Engagement Tool =======
@tool
def calculate_engagement(user_id: str) -> str:
    """Calculates learner engagement score based on frequency, recency, and diversity of events."""
    now = datetime.utcnow()
    events = list(events_col.find({"user_id": user_id}))
    if not events:
        return "No engagement found."

    freq = len(events)
    recency = (now - max(e["timestamp"] for e in events)).days
    diversity = len(set(e["event_type"] for e in events))
    score = (freq * 2 + max(0, 10 - recency) + diversity * 3)

    return f"Engagement score: {score}, Frequency: {freq}, Recency: {recency}, Diversity: {diversity}"

# ======= Tool Setup =======
tools = [
    Tool(
        name="CalculateEngagement",
        func=calculate_engagement,
        description="Calculates engagement score from user's event logs"
    )
]

# ======= Agent Init =======
scorer_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-zero-shot-react-description",
    verbose=True
)
