from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.4
)

# ====== Tool Function ======
def log_event(input: str) -> str:
    return f"Event logged: {input}"

# ====== Langchain Tool ======
tools = [
    Tool(
        name="LoggerTool",
        func=log_event,
        description="Logs learning-related events"
    )
]

# ====== Create AgentExecutor ======
logger_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-zero-shot-react-description",
    verbose=True
)
