from sqlmodel import SQLModel, Field
import uuid
from datetime import date, time, datetime

class Flight_detail(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    flight_number: str
    flight_name: str
    flight_source: str
    flight_destination: str
    flight_date: date
    flight_time: time
    flight_duration: str
    flight_price: int
    total_seats: int
    flight_status: str
    flight_airline: str
    available_seat_count: int
   

class Flight_booking(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    flight_id: uuid.UUID = Field(foreign_key="flight_detail.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    no_of_tickets: int
    booking_price: int
    flight_date: date
    flight_time: time
    flight_duration: str
    flight_source: str
    flight_destination: str
    booking_date_time: datetime = Field(default_factory=datetime.utcnow)