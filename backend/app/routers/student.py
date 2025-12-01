from fastapi import APIRouter, HTTPException, status, Header, Depends
from typing import List
from app.db.database import db
from app.models.event import EventCreate, EventInDB
from app.core.config import settings
from jose import jwt, JWTError
from bson import ObjectId
from datetime import datetime

router = APIRouter()

# --- Helper: Get Current User from Token ---
async def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await db["users"].find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# --- 1. Create Event ---
@router.post("/create-event", status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate, user: dict = Depends(get_current_user)):
    event_dict = event.dict()
    event_dict['approval_status'] = 'Pending'
    event_dict['creator_id'] = str(user["_id"])
    event_dict['college_id'] = str(user.get("college_id"))
    
    new_event = await db["events"].insert_one(event_dict)
    return {"message": "Event submitted for approval", "id": str(new_event.inserted_id)}

# --- 2. Get Upcoming Events ---
@router.get("/events")
async def get_upcoming_events():
    events = await db["events"].find({"approval_status": "Approved"}).to_list(100)
    for e in events:
        e["_id"] = str(e["_id"])
    return events

# --- 3. Register for Event (THE MISSING FEATURE) ---
@router.post("/register/{event_id}")
async def register_for_event(event_id: str, user: dict = Depends(get_current_user)):
    # 1. Check if event exists
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid Event ID")
        
    event = await db["events"].find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # 2. Check if already registered
    existing = await db["registrations"].find_one({
        "event_id": event_id,
        "student_id": str(user["_id"])
    })
    
    if existing:
        raise HTTPException(status_code=400, detail="You are already registered for this event")

    # 3. Create Registration
    registration = {
        "event_id": event_id,
        "event_name": event["name"],
        "event_date": event["date"],
        "student_id": str(user["_id"]),
        "student_name": user["name"],
        "student_email": user["email"],
        "status": "Pending Payment" if event.get("is_paid") else "Confirmed",
        "registered_at": datetime.utcnow()
    }
    
    await db["registrations"].insert_one(registration)
    return {"message": "Registration Successful", "status": registration["status"]}

# --- 4. Get My Registrations ---
@router.get("/my-registrations")
async def get_my_registrations(user: dict = Depends(get_current_user)):
    registrations = await db["registrations"].find({"student_id": str(user["_id"])}).to_list(100)
    for r in registrations:
        r["_id"] = str(r["_id"])
    return registrations