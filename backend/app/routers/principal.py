from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from typing import List
from app.db.database import db
from app.models.user import UserInDB

router = APIRouter()

@router.get("/hod/pending", response_model=List[UserInDB])
async def get_pending_hods():
    # Fetch all users with role 'HOD' and status 'Pending'
    hods = await db.users.find({"role": "HOD", "approval_status": "Pending"}).to_list(100)
    
    # Fix ID format for JSON response
    for hod in hods:
        hod["_id"] = str(hod["_id"])
    return hods

@router.patch("/hod/approve/{user_id}")
async def approve_hod(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    result = await db.users.update_one(
        {"_id": ObjectId(user_id), "role": "HOD"},
        {"$set": {"approval_status": "Approved"}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="HOD not found or already approved")
        
    return {"message": "HOD Approved Successfully"}