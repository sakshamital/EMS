from fastapi import APIRouter, HTTPException, status
from app.models.college import CollegeCreate
from app.db.database import db
from bson import ObjectId
import traceback # Helps print the error

router = APIRouter()

@router.post("/college", status_code=status.HTTP_201_CREATED)
async def create_college(college: CollegeCreate):
    print(f"Attempting to create college: {college}") # Debug print
    
    try:
        # 1. Check if college code already exists
        print("Checking if college exists...")
        existing = await db["colleges"].find_one({"code": college.code})
        if existing:
            print("College code duplicate found.")
            raise HTTPException(status_code=400, detail="College code already exists")

        # 2. Prepare Data
        print("Preparing data...")
        try:
            college_data = college.model_dump() # Pydantic V2
        except AttributeError:
            college_data = college.dict() # Pydantic V1 fallback

        # 3. Create College
        print("Inserting into database...")
        new_college = await db["colleges"].insert_one(college_data)
        print(f"College created with ID: {new_college.inserted_id}")
        
        return {"message": "College module created successfully", "id": str(new_college.inserted_id)}

    except Exception as e:
        # This will print the REAL error to your terminal
        print("CRITICAL ERROR IN CREATE COLLEGE:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

@router.get("/colleges")
async def get_all_colleges():
    try:
        colleges = await db["colleges"].find().to_list(100)
        for college in colleges:
            college["_id"] = str(college["_id"])
            if college.get("principal_id"):
                college["principal_id"] = str(college["principal_id"])
        return colleges
    except Exception as e:
        print("Error fetching colleges:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/approve/principal/{user_id}")
async def approve_principal(user_id: str, college_id: str):
    try:
        try:
            c_oid = ObjectId(college_id)
            u_oid = ObjectId(user_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        college = await db["colleges"].find_one({"_id": c_oid})
        if not college:
            raise HTTPException(status_code=404, detail="College not found")

        update_result = await db["users"].update_one(
            {"_id": u_oid, "role": "Principal"},
            {"$set": {"approval_status": "Approved", "college_id": college_id}}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found or already approved")

        await db["colleges"].update_one(
            {"_id": c_oid},
            {"$set": {"principal_id": str(u_oid)}}
        )

        return {"message": "Principal approved and linked to college"}
    except Exception as e:
        print("Error approving principal:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    # ... existing imports ...

@router.get("/principals/pending")
async def get_pending_principals():
    # Find all users with role 'Principal' and status 'Pending'
    users = await db["users"].find({"role": "Principal", "approval_status": "Pending"}).to_list(100)
    
    # Fix ID format for JSON
    for user in users:
        user["_id"] = str(user["_id"])
        
    return users