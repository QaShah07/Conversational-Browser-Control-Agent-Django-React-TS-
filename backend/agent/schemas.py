from pydantic import BaseModel
from typing import Optional, List, Literal

class EmailSlots(BaseModel):
    recipient: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    reason: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class Intent(BaseModel):
    name: Literal['send_email','other']
    slots: EmailSlots
    needs: List[str] = []