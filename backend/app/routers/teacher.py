from fastapi import APIRouter, HTTPException, Depends, Header
from typing import List
from app.db.database import db
from app.models.user import UserInDB
from app.core.config import settings
from jose import jwt, JWTError

router = APIRouter()

# --- Helper: Get Current Teacher ---
async def get_current_teacher(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await db["users"].find_one({"email": email, "role": "Teacher"})
    if not user:
        raise HTTPException(status_code=403, detail="Access denied: Teachers only")
    return user

# --- 1. View My Class (Dynamic Linking) ---
@router.get("/my-students", response_model=List[UserInDB])
async def get_my_students(teacher: dict = Depends(get_current_teacher)):
    # LOGIC: Find students who match THIS teacher's Branch, Year, and Section
    query = {
        "role": "Student",
        "branch": teacher.get("branch"),
        "year": teacher.get("year"),
        "section": teacher.get("section"),
        "college_id": teacher.get("college_id")
    }
    
    students = await db["users"].find(query).to_list(100)
    
    # Fix ID format
    for s in students:
        s["_id"] = str(s["_id"])
        
    return students

# --- 2. Broadcast Message (Optional Feature) ---
# Teacher can send a notice to their entire class
@router.post("/broadcast")
async def send_class_notice(message: str, teacher: dict = Depends(get_current_teacher)):
    # Placeholder: In real app, this calls the NotificationService
    # notifier.send_sms_to_batch(...)
    return {"message": f"Notice sent to {teacher['year']} - Sec {teacher['section']}"}