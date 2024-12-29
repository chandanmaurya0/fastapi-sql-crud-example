from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from dependencies import validate_access_token
from db import engine

# Import models
from models.flight_model import Flight_detail, Flight_booking

router = APIRouter(
    prefix="/flight", tags=["flights"], dependencies=[Depends(validate_access_token)]
)


# Add Flight data
@router.post("/add_flight")
async def add_flight(flight_detail: Flight_detail, request: Request):
    current_user = request.state.current_user
    with Session(engine) as session:
        session.add(flight_detail)
        session.commit()
        return {"message": "Flight added successfully"}


# Get flight data with few filters
@router.get("/get_flight")
async def get_flight(
    flight_source: Optional[str] = None,
    flight_destination: Optional[str] = None,
    flight_date: Optional[str] = None,
):

    query_dict = {}
    # create query statement
    # create a dict of key and value where value is not none for all the query params
    if flight_source is not None:
        query_dict["flight_source"] = flight_source

    if flight_destination is not None:
        query_dict["flight_destination"] = flight_destination

    if flight_date is not None:
        query_dict["flight_date"] = flight_date

    with Session(engine) as session:
        # Create the base statement
        statement = select(Flight_detail)
        # Add filters dynamically
        for key, value in query_dict.items():
            statement = statement.where(getattr(Flight_detail, key) == value)

        # Execute the query
        flight_list = session.exec(statement).all()
        return flight_list


class FlightBookingReqBody(BaseModel):
    flight_id: str
    no_of_tickets: int


# Route for flight booking
@router.post("/book_flight")
async def book_flight(reqBody: FlightBookingReqBody, request: Request):
    current_user = request.state.current_user
    with Session(engine) as session:
        # Get flight detail
        statement = select(Flight_detail).where(Flight_detail.id == reqBody.flight_id)
        flight_detail = session.exec(statement).first()

        # Check if flight is available
        if flight_detail is None:
            return HTTPException(status_code=404, detail="Flight not found")

        # Check if seat is available
        if flight_detail.available_seat_count < int(reqBody.no_of_tickets):
            return HTTPException(status_code=400, detail="Seat not available")

        # check flight status, it should not be CANCELLED
        if flight_detail.flight_status == "CANCELLED":
            return HTTPException(status_code=404, detail="Flight is cancelled")

        # Create booking
        flight_booking = Flight_booking(
            flight_id=reqBody.flight_id,
            user_id=current_user["userId"],
            no_of_tickets=reqBody.no_of_tickets,
            booking_price=flight_detail.flight_price,
            flight_date=flight_detail.flight_date,
            flight_time=flight_detail.flight_time,
            flight_duration=flight_detail.flight_duration,
            flight_source=flight_detail.flight_source,
            flight_destination=flight_detail.flight_destination,
            booking_date_time=datetime.now(),
        )
        session.add(flight_booking)
        session.commit()

        # Update available seat count
        flight_detail.available_seat_count = flight_detail.available_seat_count - int(
            reqBody.no_of_tickets
        )
        session.add(flight_detail)
        session.commit()

        return {"message": "Flight booked successfully"}
