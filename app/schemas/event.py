from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional, List

class Place(BaseModel):
    id: str
    name: str
    city: str
    address: str
    seats_pattern: str | None = None
    changed_at: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class EventSchema(BaseModel):
    id: str
    name: str
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int
    changed_at: datetime
    created_at: datetime
    status_changed_at: datetime
    place: Place
    
    model_config = ConfigDict(from_attributes=True)
    
class PlaceResponse(BaseModel):
    id: str
    name: str
    city: str
    address: str
    
class EventResponse(BaseModel):
    id: str
    name: str
    place: PlaceResponse
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int
    
class EventsListResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[EventResponse]
    
class RegisterRequest(BaseModel):
    event_id: str
    first_name: str
    last_name: str
    seat: str
    email: EmailStr
    
class RegisterResponse(BaseModel):
    ticket_id: str