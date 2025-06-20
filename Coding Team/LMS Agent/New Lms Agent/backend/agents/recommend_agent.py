# backend/agents/recommend_agent.py

# ======= Imports =======
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from dotenv import load_dotenv
import os

from backend.rag.retriever import retrieve_content

# ======= Load environment variables =======
load_dotenv()

# ======= LLM Initialization =======
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.4
)

# ======= Recommendation Tool =======
@tool
def recommend_by_weak_concepts(concepts: list) -> str:
    """Returns content suggestions using weak concepts."""
    prompt = "Suggest lessons for: " + ", ".join(concepts)
    results = retrieve_content(prompt)
    return results

# ======= Tool Configuration =======
tools = [
    Tool(
        name="RecommendByWeakConcepts",
        func=recommend_by_weak_concepts,
        description="Suggests content based on weak learning areas or concepts"
    )
]

# ======= Agent Executor Setup =======
recommend_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-zero-shot-react-description",
    verbose=True
)
