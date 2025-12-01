from pydantic import BaseModel, Field
from typing import Optional

class CollegeCreate(BaseModel):
    name: str
    code: str
    district: str

class CollegeInDB(CollegeCreate):
    id: str = Field(alias="_id")
    principal_id: Optional[str] = None
    is_active: bool = True

    class Config:
        allow_population_by_field_name = True