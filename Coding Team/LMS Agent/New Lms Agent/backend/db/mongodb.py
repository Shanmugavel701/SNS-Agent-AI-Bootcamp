# ======= MongoDB Connection =======

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["agentic_lms"]

users_col = db["users"]
courses_col = db["courses"]
events_col = db["events"]
reports_col = db["reports"]
