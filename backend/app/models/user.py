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
    college_code: Optional[str] = None # Required for non-Developers
    branch: Optional[str] = None       # Required for HOD/Student
    year: Optional[str] = None         # Required for Student
    section: Optional[str] = None      # Required for Student

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(UserBase):
    id: str = Field(alias="_id")
    approval_status: str = "Pending"
    college_id: Optional[str] = None

    class Config:
        allow_population_by_field_name = True