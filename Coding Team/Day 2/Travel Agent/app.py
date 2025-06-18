import os
import streamlit as st
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from duckduckgo_search import DDGS

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "your_gemini_api_key_here")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "your_weatherapi_key_here")

# Set up Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY
)

# Weather Tool
@tool
def get_weather(location: str) -> str:
    """Get current weather for a location."""
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
    response = requests.get(url)
    if response.status_code != 200:
        return f"❌ Couldn't fetch weather data for {location}."
    data = response.json()
    return f"🌤️ **Weather in {location}:** {data['current']['condition']['text']}, {data['current']['temp_c']}°C"

# Tourist Attraction Tool
@tool
def get_attractions(location: str) -> str:
    """Get top tourist attractions in a location."""
    with DDGS() as ddgs:
        results = ddgs.text(f"top tourist attractions in {location}")
        top = [res["body"] for res in results[:5]]
    return f"🏛️ **Top Attractions in {location}:**\n- " + "\n- ".join(top)

# Define system prompt to guide tool usage
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a smart travel agent. Always do the following for any input city:\n"
     "- First, fetch the current weather using the weather tool.\n"
     "- Then, fetch the top 5 tourist attractions using the attraction tool.\n"
     "- Combine both results into a friendly travel summary.\n"
     "Do not ask the user what they want. Just respond with the information."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create LangChain agent
tools = [get_weather, get_attractions]
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

# Streamlit UI
st.set_page_config(page_title="🧠 Travel Assistant", layout="centered")
st.title("🌍 Intelligent Travel Assistant")
st.markdown("Plan your trip with real-time **weather updates** and **local attraction suggestions** powered by AI!")

city = st.text_input("✈️ Enter your destination city")

if st.button("Get Travel Info") and city:
    with st.spinner("🤖 Gathering your travel info..."):
        try:
            result = agent_executor.invoke({"input": city})
            st.success("✅ Here's your travel summary:")
            st.markdown(result['output'])
        except Exception as e:
            st.error(f"🚨 Error: {e}")
