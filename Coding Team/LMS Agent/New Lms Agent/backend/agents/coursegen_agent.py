from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from backend.agents.base import llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# === Tool ===
@tool
def generate_course_outline(course_title: str) -> str:
    """Creates 10 lesson titles and 10 quizzes based on the course topic."""
    prompt = f"""
    You are an expert course designer.

    Design a structured course outline titled: "{course_title}"

    Provide 10 Modules.
    For each module:
    - Give a Lesson Title
    - Provide 2–3 lines of lesson content
    - Add 1 Quiz Question with 4 options and the correct answer

    Use this format:

    Module {{number}}:
      Lesson Title: ...
      Content: ...
      Quiz:
        Q: ...
        A. ...
        B. ...
        C. ...
        D. ...
        Answer: ...

    Make sure all modules follow this format clearly.
    """
    chain = llm | StrOutputParser()
    return chain.invoke(prompt)
tools = [generate_course_outline]


# === REQUIRED ReAct prompt structure ===
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful course designer agent that uses tools to generate lesson modules and quizzes."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
]).partial(
    tools=str([tool.name for tool in tools]), 
    tool_names=", ".join([tool.name for tool in tools])
)

# === Create agent and executor ===
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

coursegen_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
