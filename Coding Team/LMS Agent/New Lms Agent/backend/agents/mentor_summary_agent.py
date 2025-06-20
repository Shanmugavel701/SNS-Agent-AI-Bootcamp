# backend/agents/mentor_summary_agent.py

# ======= Imports =======
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from dotenv import load_dotenv
import os

# ======= Load Env =======
load_dotenv()

# ======= Initialize Gemini LLM =======
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.4
)

# ======= Mentor Summary Tool =======
@tool
def generate_summary(data: dict) -> dict:
    """Generate structured mentor report from learner data."""
    return {
        "highlights": data.get("engagement"),
        "weaknesses": data.get("quiz"),
        "recommendations": data.get("recommendations")
    }

# ======= Tool Configuration =======
tools = [
    Tool(
        name="GenerateMentorSummary",
        func=generate_summary,
        description="Generates a mentor summary report from engagement, quiz, and recommendations"
    )
]

# ======= Agent Setup =======
mentor_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-zero-shot-react-description",
    verbose=True
)
