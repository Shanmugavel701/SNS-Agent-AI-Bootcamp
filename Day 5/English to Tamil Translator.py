import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableMap, RunnableLambda
from langchain.chains import RetrievalQA
import tempfile
import os

# Set your Google API Key
GOOGLE_API_KEY = "AIzaSyD-q5-mcoLn6Horgx-tPD_q4V5N_GV7uQE"

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-latest",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2
)

st.set_page_config(page_title="RAG PDF QA App", layout="centered")
st.title("📄 RAG-powered PDF Q&A App with Gemini 2.0")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_pdf_path = tmp_file.name

    st.success("PDF Uploaded Successfully!")

    # Step 1: Load PDF
    loader = PyPDFLoader(tmp_pdf_path)
    pages = loader.load()

    # Step 2: Split text into chunks
    splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(pages)

    # Step 3: Embed using HuggingFace and store in FAISS
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    retriever = vectorstore.as_retriever()

    # Step 4: Custom prompt
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("Answer the question based only on the following context:\n\n{context}"),
        HumanMessagePromptTemplate.from_template("Question: {question}")
    ])

    # Step 5: Define final chain using Runnable components
    chain = (
        {"context": retriever | RunnableLambda(lambda docs: "\n\n".join([doc.page_content for doc in docs])),
         "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    # Step 6: Ask a question
    user_question = st.text_input("Ask a question about your PDF")

    if user_question:
        with st.spinner("Thinking..."):
            answer = chain.invoke(user_question)
            st.markdown("### ✨ Answer")
            st.write(answer.content)

        with st.expander("🔍 Retrieved Context"):
            context_docs = retriever.get_relevant_documents(user_question)
            for i, doc in enumerate(context_docs):
                st.markdown(f"**Chunk {i+1}**\n\n{doc.page_content[:500]}...")

# Clean up temporary file
if 'tmp_pdf_path' in locals():
    os.remove(tmp_pdf_path)
