from typing import Annotated
import jwt
import os

from fastapi import Header, HTTPException, Request


# Define constant
ALGORITHM = "HS256"

async def validate_access_token(Authorization: Annotated[str, Header()], request: Request):
    if Authorization is not None:
        access_toekn = Authorization.split(" ")[1]
        try:
            payload = jwt.decode(access_toekn, os.getenv("ACCESS_TOEKN_SECRET_KEY"), algorithms=[ALGORITHM])
            request.state.current_user = payload
            return
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    else:
        raise HTTPException(status_code=400, detail="Authorization header invalid")
    