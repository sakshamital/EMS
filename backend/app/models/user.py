from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    role: str  # Developer, Principal, HOD, Student

class UserCreate(UserBase):
    password: str
    college_code: Optional[str] = None 
    college_name: Optional[str] = None # Added College Name
    college_id_number: Optional[str] = None # Added Student/Staff ID (Roll No)
    branch: Optional[str] = None
    year: Optional[str] = None
    section: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(UserBase):
    id: str = Field(alias="_id")
    approval_status: str = "Pending"
    college_id: Optional[str] = None
    college_id_number: Optional[str] = None # Show in DB response

    class Config:
        populate_by_name = True