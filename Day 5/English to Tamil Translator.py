# app.py

import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema.runnable import Runnable
from langchain.schema.output_parser import StrOutputParser

# ---- 1. Set Gemini API Key ----
GOOGLE_API_KEY = "AIzaSyD-q5-mcoLn6Horgx-tPD_q4V5N_GV7uQE"  # Replace with your real key
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# ---- 2. Initialize Gemini Chat Model ----
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# ---- 3. Create Prompt for English to Tamil ----
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful assistant that translates English sentences to Tamil."
    ),
    HumanMessagePromptTemplate.from_template("{input}")
])

# ---- 4. Chain: prompt -> LLM -> Output parser ----
chain: Runnable = prompt | llm | StrOutputParser()

# ---- 5. Streamlit UI ----
st.set_page_config(page_title="English to Tamil Translator", page_icon="🌐")
st.title("🌐 English to Tamil Translator")

with st.form("translator_form"):
    english_input = st.text_input("Enter an English sentence:")
    submitted = st.form_submit_button("Translate")

    if submitted:
        if english_input.strip() == "":
            st.warning("⚠️ Please enter a sentence.")
        else:
            try:
                tamil_output = chain.invoke({"input": english_input})
                st.success("✅ Translation successful!")
                st.markdown(f"**Tamil Translation:** {tamil_output}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
