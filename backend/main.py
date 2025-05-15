from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from docx import Document
from docx.shared import Pt
import oracledb
import os
from datetime import datetime
import tempfile
import asyncio
import threading

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly allow OPTIONS
    allow_headers=["*"],  # Allow all headers
)

# Oracle DB connection parameters
DB_USER = "MIS_DL"  # Replace with your Oracle username
DB_PASSWORD = "0MISDxe34fI7h8=#Y1"  # Replace with your Oracle password
DB_DSN = "10.0.175.156:1531/DLDBDEV"  # Replace with your Oracle DSN

# Initialize Oracle connection pool
pool = oracledb.create_pool(
    user=DB_USER,
    password=DB_PASSWORD,
    dsn=DB_DSN,
    min=1,
    max=5,
    increment=1
)

# Define model for input data
class LeaveRequest(BaseModel):
    name: str
    position: str
    department: str
    used_days: int
    requested_days: int
    start_date: str
    end_date: str
    reason: str
    location: str

# Function to save data to Oracle DB (synchronous)
def save_to_oracle_sync(data: dict):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO LEAVE_REQUESTS (
                    name, position, department, used_days, requested_days,
                    start_date, end_date, reason, location, request_date
                ) VALUES (:name, :position, :department, :used_days, :requested_days,
                        :start_date, :end_date, :reason, :location, :request_date)
            """, {
                "name": data["name"],
                "position": data["position"],
                "department": data["department"],
                "used_days": data["used_days"],
                "requested_days": data["requested_days"],
                "start_date": data["start_date"],
                "end_date": data["end_date"],
                "reason": data["reason"],
                "location": data["location"],
                "request_date": data["current_date"]
            })
            connection.commit()

# Async wrapper for synchronous DB operation
async def save_to_oracle(data: dict):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, save_to_oracle_sync, data)

# Function to fill Word template
def fill_word_template(template_path: str, data: dict) -> str:
    doc = Document(template_path)
    
    for paragraph in doc.paragraphs:
        for key, value in data.items():
            placeholder = f"[{key.upper()}]"
            if placeholder in paragraph.text:
                for run in paragraph.runs:
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, str(value))
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(14)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        doc.save(tmp.name)
        return tmp.name

@app.post("/fill-leave-request")
async def fill_leave_request(request: LeaveRequest):
    template_path = "templates/don_xin_nghi_phep.docx"
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template file not found")
    
    current_date = datetime.now().strftime("%d tháng %m năm %Y")
    data = {
        "name": request.name,
        "position": request.position,
        "department": request.department,
        "used_days": request.used_days,
        "requested_days": request.requested_days,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "reason": request.reason,
        "location": request.location,
        "current_date": current_date,
        "remaining_days": 12 - request.used_days - request.requested_days
    }
    
    # Save to Oracle DB
    try:
        await save_to_oracle(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    # Generate Word file
    output_path = fill_word_template(template_path, data)
    
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="don_xin_nghi_phep_filled.docx"
    )