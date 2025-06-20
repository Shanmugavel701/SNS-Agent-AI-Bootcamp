# backend/rag/retriever.py

# ======= Imports =======
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv

# ======= Load Env =======
load_dotenv()

# ======= Embeddings Setup =======
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# ======= Sample Retriever Function =======
def retrieve_content(query: str):
    """Retrieve content matching the weak concepts using FAISS vector search"""

    # Load & prepare documents (you can later switch to MongoDB or static text)
    docs = [
        Document(page_content="Introduction to OOP in Python"),
        Document(page_content="Basics of SQL Joins and Keys"),
        Document(page_content="What is Recursion in Programming?")
    ]

    # Create vector DB
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Perform retrieval
    retriever = vectorstore.as_retriever()
    return retriever.get_relevant_documents(query)
