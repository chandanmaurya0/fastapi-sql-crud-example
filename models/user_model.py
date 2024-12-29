from sqlmodel import Field, SQLModel
import uuid
from datetime import datetime

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: str = Field(unique=True)
    mobile_number: str
    password: str
    lastUpdatedDtm: datetime = Field(default_factory=datetime.utcnow)