# utils/prompts.py

from langchain.prompts import ChatPromptTemplate

# ======= Prompt: Logger Agent =======
logger_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a learning activity logger. Return structured summaries of user interactions."),
    ("human", "{input}")
])

# ======= Prompt: Engagement Scorer Agent =======
scorer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an engagement analyzer. Calculate learner score based on user activity log."),
    ("human", "{input}")
])

# ======= Prompt: Quiz Analyzer Agent =======
quiz_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a quiz analyzer. Return concept-wise strengths based on performance data."),
    ("human", "{input}")
])

# ======= Prompt: Recommendation Generator Agent =======
recommend_prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a smart tutor. Recommend content based on weak areas or quiz gaps."),
    ("human", "{input}")
])

# ======= Prompt: Mentor Summary Composer Agent =======
mentor_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a mentor dashboard generator. Convert data into an insightful summary."),
    ("human", "{input}")
])
