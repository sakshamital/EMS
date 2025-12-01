from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from app.db.database import db
from app.models.user import UserInDB
from app.models.event import EventInDB

router = APIRouter()

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
        
    result = await db.events.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": {"approval_status": status}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": f"Event {status}"}
from app.models.event import EventCreate
from datetime import datetime

# ... existing imports ...

@router.post("/create-event")
async def create_direct_event(event: EventCreate):
    event_dict = event.dict()
    
    # CRITICAL: HOD events are automatically approved!
    event_dict['approval_status'] = 'Approved'
    
    # In real app, get these from the logged-in HOD's token
    event_dict['creator_id'] = "hod_user_id" 
    event_dict['college_id'] = "hod_college_id"
    
    new_event = await db.events.insert_one(event_dict)
    return {"message": "Event Created and Published Successfully", "id": str(new_event.inserted_id)}