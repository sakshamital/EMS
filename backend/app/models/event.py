from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EventCreate(BaseModel):
    name: str
    date: datetime
    registration_deadline: datetime
    description: str
    poster_url: str
    requirements: Optional[str] = None
    is_paid: bool = False
    fee: int = 0
    payment_qr_url: Optional[str] = None

class EventInDB(EventCreate):
    id: str = Field(alias="_id")
    college_id: str
    creator_id: str
    approval_status: str = "Pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True