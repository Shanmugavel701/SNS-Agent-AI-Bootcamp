# backend/agents/quiz_agent.py

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

# ======= Quiz Analysis Tool =======
@tool
def analyze_quiz_results(concept_data: dict) -> dict:
    """Analyze quiz results tagged by concept and return accuracy per concept."""
    report = {}
    for concept, answers in concept_data.items():
        correct = sum(answers)
        total = len(answers)
        percentage = (correct / total) * 100
        report[concept] = f"{percentage:.2f}% accuracy"
    return report

# ======= Tool Registration =======
tools = [
    Tool(
        name="AnalyzeQuizResults",
        func=analyze_quiz_results,
        description="Analyzes quiz results and returns concept-wise accuracy"
    )
]

# ======= Agent Setup =======
quiz_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-zero-shot-react-description",
    verbose=True
)
