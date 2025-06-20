# ======= FastAPI Server =======

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # ✅ Added for request body model

from backend.agents import (
    logger_agent,
    scorer_agent,
    quiz_agent,
    recommend_agent,
    mentor_summary_agent,
    coursegen_agent
)
from backend.db.mongodb import reports_col

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request Model for Course Generation
class CourseRequest(BaseModel):
    course_name: str

# ========== Agent APIs ==========

@app.post("/log-event/")
async def log_event_api(request: Request):
    data = await request.json()
    return logger_agent.log_event(data["user_id"], data["event_type"], data["resource"])

@app.get("/score-engagement/{user_id}")
def score_engagement_api(user_id: str):
    return scorer_agent.score_engagement(user_id)

@app.post("/analyze-quiz/")
async def analyze_quiz_api(request: Request):
    data = await request.json()
    return quiz_agent.analyze_quiz(data)

@app.post("/recommend/")
async def recommend_api(request: Request):
    data = await request.json()
    return recommend_agent.recommend_content(data["weak_concepts"])

@app.post("/mentor-summary/")
async def mentor_summary_api(request: Request):
    data = await request.json()
    report = mentor_summary_agent.generate_summary(
        data["user_id"], data["engagement"], data["quiz"]
    )
    reports_col.insert_one(report)
    return report

# ========== ✅ New CourseGen API with input field ==========
@app.post("/generate-course")
async def generate_course_api(request: CourseRequest):
    result = coursegen_agent.coursegen_executor.invoke({"input": request.course_name})
    return {"generated_course": result}
