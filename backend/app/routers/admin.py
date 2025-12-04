# ...existing code...
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from typing import List
from pydantic import BaseModel
from app.db.database import db
from app.models.user import UserInDB
from app.models.event import EventInDB, EventCreate
from datetime import datetime

router = APIRouter()

# fallback HOD-like stub for dev/testing
async def get_current_user():
    # TODO: replace with real auth dependency when available
    return {"college_id": "hod_college_id", "branch": "CSE", "user_id": "hod_user_id"}

# --- STUDENT MANAGEMENT ---

@router.get("/students/pending", response_model=List[UserInDB])
async def get_pending_students():
    students = await db.users.find({"role": "Student", "approval_status": "Pending"}).to_list(100)
    for s in students:
        s["_id"] = str(s["_id"])
    return students

@router.patch("/students/approve/{user_id}")
async def approve_student(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = await db.users.update_one(
        {"_id": ObjectId(user_id), "role": "Student"},
        {"$set": {"approval_status": "Approved"}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student Approved"}

# --- EVENT MANAGEMENT ---

@router.get("/events/pending", response_model=List[EventInDB])
async def get_pending_events():
    events = await db.events.find({"approval_status": "Pending"}).to_list(100)
    for e in events:
        e["_id"] = str(e["_id"])
    return events

@router.patch("/events/status/{event_id}")
async def update_event_status(event_id: str, status: str):
    if status not in ["Approved", "Rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    result = await db.events.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": {"approval_status": status}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": f"Event {status}"}

# HOD creates an event directly (auto-approved)
@router.post("/create-event")
async def create_direct_event(event: EventCreate, hod: dict = Depends(get_current_user)):
    event_dict = event.dict()
    
    # CRITICAL: HOD events are automatically approved
    event_dict['approval_status'] = 'Approved'
    
    # In real app, use hod from dependency
    event_dict['creator_id'] = hod.get("user_id", "hod_user_id")
    event_dict['college_id'] = hod.get("college_id", "hod_college_id")
    event_dict['created_at'] = datetime.utcnow()
    
    new_event = await db.events.insert_one(event_dict)
    return {"message": "Event Created and Published Successfully", "id": str(new_event.inserted_id)}

# --- Promotion helper and endpoint ---

def get_next_level(current_year: str, current_sem: str):
    progression = {
        "1st Sem": ("1st Year", "2nd Sem"),
        "2nd Sem": ("2nd Year", "3rd Sem"),
        "3rd Sem": ("2nd Year", "4th Sem"),
        "4th Sem": ("3rd Year", "5th Sem"),
        "5th Sem": ("3rd Year", "6th Sem"),
        "6th Sem": ("4th Year", "7th Sem"),
        "7th Sem": ("4th Year", "8th Sem"),
        "8th Sem": ("Graduated", "Alumni"),
    }
    return progression.get(current_sem)

class PromoteBatchSchema(BaseModel):
    target_year: str
    target_sem: str

@router.post("/promote-batch")
async def promote_batch(data: PromoteBatchSchema, hod: dict = Depends(get_current_user)):
    filter_query = {
        "college_id": hod["college_id"],
        "branch": hod["branch"],
        "year": data.target_year,
        "section": {"$exists": True}
    }
    
    next_level = get_next_level(data.target_year, data.target_sem)
    if not next_level:
        raise HTTPException(status_code=400, detail="Invalid Semester/Year combination for promotion")
        
    new_year, new_sem = next_level
    
    if new_year == "Graduated":
        update_query = {"$set": {"role": "Alumni", "approval_status": "Graduated"}}
    else:
        update_query = {"$set": {"year": new_year, "current_semester": new_sem}}

    result = await db["users"].update_many(filter_query, update_query)
    
    if result.modified_count == 0:
        return {"message": "No eligible students found to promote."}

    return {
        "message": f"Successfully promoted {result.modified_count} students.",
        "from": f"{data.target_year} - {data.target_sem}",
        "to": f"{new_year} - {new_sem}"
    }
# ...existing code...
# ... existing imports ...

@router.get("/students/active", response_model=List[UserInDB])
async def get_active_students(hod: dict = Depends(get_current_user)):
    # Filter by HOD's college and branch
    query = {
        "role": "Student",
        "approval_status": "Approved", # Only active students
        "college_id": hod["college_id"],
        "branch": hod["branch"]
    }
    
    # IF the HOD is assigned to a specific year (e.g., 2nd Year HOD), filter by that too
    if hod.get("year"):
        query["year"] = hod["year"]

    students = await db["users"].find(query).to_list(1000) # Fetch up to 1000
    
    for s in students:
        s["_id"] = str(s["_id"])
        
    return students