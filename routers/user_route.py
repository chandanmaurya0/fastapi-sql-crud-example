from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel

from models.user_model import User
from db import engine

# Import helper methods
from services import user_service
from sqlmodel import SQLModel


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/signup", tags=["users"])
async def create_new_user_account(user_data: User):
    user_data_dict = user_data.dict()

    # hash the password before storing in db
    user_data_dict["password"] = user_service.hash_password(user_data_dict["password"])

    user_1 = User(
        name=user_data_dict["name"],
        email=user_data_dict["email"],
        mobile_number=user_data_dict["mobile_number"],
        password=user_data_dict["password"],
    )
    with Session(engine) as session:
        session.add(user_1)
        session.commit()
        session.refresh(user_1)
    return user_1


class UserLogin(BaseModel):
    email: str
    password: str


# create login route
@router.post("/login", tags=["users"])
async def login(login_detail: UserLogin):

    with Session(engine) as session:
        statement = select(User).where(User.email == login_detail.email)
        results = session.exec(statement)
        user_detail = results.first()

        print("user_detail - ", user_detail)
        if user_detail is None:
            return {"message": "Login failed. Email or password is incorrect."}

        # Match password
        if user_service.verify_password(login_detail.password, user_detail.password):

            # Generate token
            access_token = user_service.create_access_token(
                data={"email": user_detail.email, "userId": str(user_detail.id)}
            )
            refresh_token = user_service.create_refresh_token(
                data={"email": user_detail.email, "userId": str(user_detail.id)}
            )
            return {
                "message": "Login successful",
                "user_detail": {
                    "userId": str(user_detail.id),
                    "name": user_detail.name,
                    "email": user_detail.email,
                    "mobile_number": user_detail.mobile_number,
                },
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        else:
            return {"message": "Login failed. Email or password is incorrect."}


class DeleteAccountReqBody(BaseModel):
    user_id: str
    password: str


# Create an route to delete user
@router.delete("/delete_account", tags=["users"])
async def delete_user(reqBody: DeleteAccountReqBody):
    with Session(engine) as session:
        statement = select(User).where(User.id == reqBody.user_id)
        results = session.exec(statement)
        user_detail = results.one()

        # Match password
        if not user_service.verify_password(reqBody.password, user_detail.password):
            return {"message": "Password is incorrect."}

        session.delete(user_detail)
        session.commit()
        return {"message": "User deleted successfully"}


# get user detail
@router.get("/get_user_detail", tags=["users"])
async def get_user_detail(user_id: str):

    with Session(engine) as session:
        statement = select(User).where(User.id == user_id)
        results = session.exec(statement)
        user_detail = results.first()

        if user_detail is None:
            return HTTPException(status_code=404, detail="User not found")

        user_data = {
            "userId": str(user_detail.id),
            "name": user_detail.name,
            "email": user_detail.email,
            "mobile_number": user_detail.mobile_number,
        }

        return {
            "message": "User found",
            "user_detail": user_data,
        }
